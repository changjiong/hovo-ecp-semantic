#!/usr/bin/env python3
"""只读读取清单闭包，在不可变字节快照上校验并打包；不自动刷新摘要。"""
from __future__ import annotations
import argparse
import json
import os
import tempfile
import zipfile
from pathlib import Path
from workspace_files import PackageError, collect_files, snapshot_digest
from validate_ecp_assets import validate_path

def package(root: Path, output: Path) -> dict:
    root=Path(root).absolute();output=Path(output).absolute()
    if output.resolve().is_relative_to(root.resolve()):
        raise PackageError('OUTPUT_INSIDE_WORKSPACE','输出必须在导入工作区之外')
    if output.exists():raise PackageError('OUTPUT_EXISTS','输出已存在；请显式选择新路径，不覆盖旧证据')
    files=collect_files(root)
    with tempfile.TemporaryDirectory() as td:
        snapshot=Path(td)
        for name,data in files.items():
            p=snapshot/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        report=validate_path(snapshot)
        if report['errors']:
            raise PackageError('PACKAGE_VALIDATION_FAILED',json.dumps(report['errors'],ensure_ascii=False))
        if report.get('inputDigest')!=snapshot_digest(files):raise PackageError('SNAPSHOT_MISMATCH','验证快照与打包字节不一致')
        output.parent.mkdir(parents=True,exist_ok=True)
        fd,temp_name=tempfile.mkstemp(prefix='.package-',suffix='.zip',dir=output.parent);os.close(fd)
        try:
            with zipfile.ZipFile(temp_name,'w',compression=zipfile.ZIP_DEFLATED) as z:
                for name in sorted(files):
                    info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                    z.writestr(info,files[name])
            # 独立回读实际归档，验证归档与已验证快照精确相等。
            with zipfile.ZipFile(temp_name) as z:
                if z.namelist()!=sorted(files) or any(z.read(n)!=files[n] for n in files):
                    raise PackageError('ARCHIVE_MISMATCH','归档回读不一致')
            os.replace(temp_name,output)
        finally:
            Path(temp_name).unlink(missing_ok=True)
    return {'output':str(output),'inputDigest':snapshot_digest(files),'fileCount':len(files),'validatedFiles':sorted(files),'localValidationStatus':report['summary']['status'],'ecpCompilation':'NOT_EXECUTED','releaseReady':False,'note':'只形成导入/预检封装，不代表平台已接受、编译或批准发布'}

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('workspace');ap.add_argument('--output',required=True);args=ap.parse_args()
    try:print(json.dumps(package(Path(args.workspace),Path(args.output)),ensure_ascii=False,indent=2));return 0
    except (PackageError,ValueError,OSError) as e:print(json.dumps({'error':getattr(e,'code','PACKAGE_ERROR'),'message':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
