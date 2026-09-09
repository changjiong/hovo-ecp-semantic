"""工作区清单闭包与安全读取：校验、摘要刷新和打包共用一份文件集合。

这里只处理文件与结构，不推断平台业务语义。限制值是本工具的安全预算。
"""
from __future__ import annotations
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

MAX_FILE_BYTES = 5_242_880
MAX_TOTAL_BYTES = 104_857_600
MAX_FILES = 1024

class PackageError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code

def _pairs(items):
    obj = {}
    for key, value in items:
        if key in obj:
            raise ValueError(f'重复JSON键: {key}')
        obj[key] = value
    return obj

def json_text(text: str) -> Any:
    def bad_constant(value):
        raise ValueError(f'非有限JSON数值: {value}')
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=bad_constant)

def read_json(path: Path) -> Any:
    return json_text(path.read_text(encoding='utf-8'))

def digest_bytes(data: bytes) -> str:
    return 'sha256:' + hashlib.sha256(data).hexdigest()

def canonical_path(value: Any) -> str:
    if not isinstance(value, str) or not value or len(value)>512:
        raise PackageError('UNSAFE_PATH', '清单路径必须是非空相对路径')
    if '\\' in value or ':' in value or any(ord(c)<32 for c in value):
        raise PackageError('UNSAFE_PATH', f'非法路径字符: {value!r}')
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in {'', '.', '..'} for x in value.split('/')):
        raise PackageError('UNSAFE_PATH', f'路径不是规范相对路径: {value}')
    return value

def safe_path(root: Path, value: Any) -> Path:
    rel = canonical_path(value)
    current = root
    if root.is_symlink():
        raise PackageError('SYMLINK', f'不允许符号链接工作区: {root}')
    for part in PurePosixPath(rel).parts:
        current = current / part
        if current.is_symlink():
            raise PackageError('SYMLINK', f'不允许符号链接: {rel}')
    if not current.is_file():
        raise PackageError('MEMBER_MISSING', f'清单文件不存在或不是普通文件: {rel}')
    if current.stat().st_size > MAX_FILE_BYTES:
        raise PackageError('FILE_LIMIT', f'单文件超过本地安全预算: {rel}')
    return current

def collect_files(root: Path, *, reject_unlisted: bool = True) -> dict[str, bytes]:
    """返回按清单引用闭包读取的字节快照；不刷新摘要、不猜文件类型。"""
    files: dict[str, bytes] = {}
    def add(rel: Any) -> Any:
        name = canonical_path(rel)
        if name in files:
            raise PackageError('DUPLICATE_REFERENCE', f'清单重复引用路径: {name}')
        p = safe_path(root, name)
        files[name] = p.read_bytes()
        if len(files[name]) > MAX_FILE_BYTES:
            raise PackageError('FILE_LIMIT', f'读取后超过单文件预算: {name}')
        if len(files)>MAX_FILES or sum(map(len,files.values()))>MAX_TOTAL_BYTES:
            raise PackageError('PACKAGE_LIMIT','工作区超过本地总文件或字节预算')
        return files[name]
    def obj(data):
        try:
            value=json_text(data.decode('utf-8'))
        except (ValueError,UnicodeError) as e:
            raise PackageError('JSON_PARSE', str(e)) from e
        if not isinstance(value,dict):
            raise PackageError('MANIFEST_TYPE','清单必须是对象')
        return value
    m=obj(add('manifest.json'))
    kind=m.get('kind')
    if kind=='ECP_SEMANTIC_WORKSPACE_PACKAGE':
        try:
            add(m['ontology']['path']); add(m['mapping']['path'])
            rules=obj(add(m['ruleSet']['manifestPath']))
            for group in ['schemas','scopes']:
                for item in m.get(group,[]): add(item['path'])
        except (KeyError,TypeError) as e:
            raise PackageError('MANIFEST_STRUCTURE',f'工作区清单结构不完整: {e}') from e
        if rules.get('kind')!='ECP_RULE_SET_BUNDLE':
            raise PackageError('RULESET_KIND','规则集清单类型不正确')
    elif kind=='ECP_RULE_SET_BUNDLE':
        rules=m
    else:
        raise PackageError('MANIFEST_KIND','目录必须包含工作区或规则集清单；单资产请直接传文件')
    try:
        for member in rules['members']: add(member['path'])
    except (KeyError,TypeError) as e:
        raise PackageError('MANIFEST_STRUCTURE',f'规则集成员结构不完整: {e}') from e
    if reject_unlisted:
        actual=set()
        for p in root.rglob('*'):
            rel=p.relative_to(root).as_posix()
            if p.is_symlink():
                raise PackageError('SYMLINK',f'不允许符号链接: {rel}')
            if p.is_file(): actual.add(rel)
            elif not p.is_dir():
                raise PackageError('NONREGULAR_FILE',f'不允许特殊文件: {rel}')
        extra=sorted(actual-set(files))
        if extra:
            raise PackageError('UNLISTED_FILE','存在未登记文件；移出导入目录后重新校验: '+', '.join(extra))
    return files

def snapshot_digest(files: dict[str,bytes]) -> str:
    records=[{'path':name,'sha256':digest_bytes(files[name])} for name in sorted(files)]
    return digest_bytes(json.dumps(records,sort_keys=True,separators=(',',':')).encode())

def unpack_zip(path: Path, destination: Path) -> None:
    """预先检查所有归档条目；任一不安全项存在时不解压任何文件。"""
    with zipfile.ZipFile(path) as z:
        entries=z.infolist(); names=set(); total=0
        if len(entries)>MAX_FILES: raise PackageError('ZIP_LIMIT','归档条目超限')
        for info in entries:
            raw=info.filename[:-1] if info.is_dir() else info.filename
            canonical_path(raw)
            if raw in names: raise PackageError('ZIP_DUPLICATE',f'归档重复条目: {raw}')
            names.add(raw)
            mode=info.external_attr>>16
            if stat.S_ISLNK(mode): raise PackageError('ZIP_SYMLINK',f'归档符号链接: {raw}')
            if info.flag_bits&1: raise PackageError('ZIP_ENCRYPTED','不接受加密归档')
            if info.file_size>MAX_FILE_BYTES:raise PackageError('ZIP_FILE_LIMIT',f'归档单文件超限: {raw}')
            total+=info.file_size
        if total>MAX_TOTAL_BYTES:raise PackageError('ZIP_LIMIT','归档解压总量超限')
        if 'manifest.json' not in names:raise PackageError('ZIP_MANIFEST','清单必须位于归档根；不自动剥离包装目录')
        for info in entries:
            if info.is_dir():continue
            p=destination/info.filename;p.parent.mkdir(parents=True,exist_ok=True)
            data=z.read(info)
            if len(data)!=info.file_size:raise PackageError('ZIP_SIZE','归档字节数不符')
            p.write_bytes(data)
