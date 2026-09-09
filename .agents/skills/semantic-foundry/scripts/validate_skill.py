#!/usr/bin/env python3
"""检查技能身份、必要交付物、受控来源快照和本地文档链接；不是模型行为评测。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

import yaml

from workspace_files import PackageError, read_json


REQUIRED = [
    "SKILL.md", "README.md", "manifest.json", "agents/interface.yaml", "THIRD_PARTY_NOTICES.md",
    "references/source-manifest.json", "references/handbook-index.md",
    "references/ontology-engineering-method.md", "references/modeling-patterns.md",
    "references/output-contract.md", "references/interaction-policy.md",
    "references/source-intake.md", "references/ecp-adaptation.md", "references/ecp-asset-playbook.md",
    "references/ecp-kit-1.7/manifest.json", "assets/domain-review.template.md",
    "reports/prior-art-research.md", "reports/creation-handoff.md", "reports/skill-ir.json",
    "scripts/validate_skill.py", "scripts/trigger_eval.py", "scripts/run_verification.py",
    "scripts/validate_design.py", "scripts/scaffold_design.py", "scripts/validate_ecp_assets.py",
    "scripts/workspace_files.py", "scripts/package_workspace.py", "scripts/refresh_workspace_digests.py",
    "scripts/validate_shacl_instance.py", "assets/design-contract.schema.json",
    "assets/design-contract.template.json", "requirements.txt", "requirements-shacl.txt",
    "evals/trigger_cases.json", "evals/model-generation/tasks.json",
    "evals/model-generation/result-template.json", "evals/model-generation/README.md",
    "examples/ownership-slice/run.py", "examples/ownership-slice/design/contract.json",
    "examples/handbook-reference/run.py",
]

AUTHORED_MARKDOWN = [
    "SKILL.md", "README.md", "THIRD_PARTY_NOTICES.md", "assets/domain-review.template.md",
    "references/handbook-index.md", "reports/prior-art-research.md", "reports/creation-handoff.md",
    "references/ontology-engineering-method.md", "references/modeling-patterns.md",
    "references/output-contract.md", "references/interaction-policy.md",
    "references/source-intake.md", "references/ecp-adaptation.md", "references/ecp-asset-playbook.md",
]

INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
REFERENCE_LINK = re.compile(r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))")


def has_forbidden_component(path: Path | PurePosixPath) -> bool:
    return any("trash" in part.casefold() for part in path.parts)


def safe_member(root: Path, relative: str) -> Path:
    """Return a regular in-package file without following links or reading trash paths."""
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not rel.parts or any(part in {"", ".", ".."} for part in rel.parts):
        raise PackageError("UNSAFE_PATH", f"路径不是规范相对路径: {relative}")
    if has_forbidden_component(rel):
        raise PackageError("FORBIDDEN_PATH", f"不读取含 trash 的路径: {relative}")
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise PackageError("SYMLINK", f"不允许符号链接: {relative}")
    if not current.is_file():
        raise PackageError("MEMBER_MISSING", f"文件不存在或不是普通文件: {relative}")
    return current


def relative_path(root: Path, source: Path, raw_target: str) -> str:
    parsed = urlsplit(raw_target)
    if parsed.scheme or parsed.netloc:
        raise PackageError("NONLOCAL_LINK", "外部链接不进入本地链接检查")
    target = unquote(parsed.path)
    if not target:
        return source.relative_to(root).as_posix()
    candidate = PurePosixPath(target)
    if candidate.is_absolute():
        raise PackageError("UNSAFE_PATH", f"本地链接不得使用绝对路径: {raw_target}")
    parts = list(source.relative_to(root).parent.parts)
    for part in candidate.parts:
        if part == ".":
            continue
        if part == "..":
            if not parts:
                raise PackageError("UNSAFE_PATH", f"本地链接越出技能目录: {raw_target}")
            parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def local_links(root: Path, source_rel: str, text: str) -> list[str]:
    source = safe_member(root, source_rel)
    links = []
    for match in [*INLINE_LINK.finditer(text), *REFERENCE_LINK.finditer(text)]:
        raw = match.group(1) or match.group(2)
        if raw:
            links.append(raw)
    failures = []
    for raw in links:
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or raw.startswith("#"):
            continue
        try:
            safe_member(root, relative_path(root, source, raw))
        except PackageError as exc:
            failures.append(f"本地链接无效: {source_rel} -> {raw}: {exc}")
    return failures


def load_frontmatter(text: str) -> dict:
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("入口缺少完整元数据")
    value = yaml.safe_load(parts[1])
    if not isinstance(value, dict):
        raise ValueError("入口元数据必须是对象")
    return value


def validate(root: Path) -> dict:
    root = root.absolute()
    failures: list[str] = []
    warnings: list[str] = []
    verified: list[str] = []
    if has_forbidden_component(root):
        return {"ok": False, "status": "FAIL", "failures": ["工作区路径包含禁止读取的目录"],
                "warnings": [], "verifiedAuthorityFiles": [], "modelBehavior": "NOT_EXECUTED"}
    if root.is_symlink():
        failures.append(f"不允许符号链接工作区: {root}")
        return {"ok": False, "status": "FAIL", "failures": failures, "warnings": warnings,
                "verifiedAuthorityFiles": verified, "modelBehavior": "NOT_EXECUTED",
                "note": "这是制品与规范快照检查；公开许可和业务批准需独立确认"}
    for rel in REQUIRED:
        try:
            safe_member(root, rel)
        except PackageError as exc:
            failures.append(f"缺少或不安全的制品: {rel}: {exc}")
    for directory, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = [name for name in directories if "trash" not in name.casefold()
                          and name not in {".git", "__pycache__", "node_modules"}]
        if Path(directory) != root and "SKILL.md" in filenames:
            failures.append("存在嵌套技能入口: " + (Path(directory) / "SKILL.md").relative_to(root).as_posix())
    try:
        skill_text = safe_member(root, "SKILL.md").read_text(encoding="utf-8")
        frontmatter = load_frontmatter(skill_text)
        manifest = read_json(safe_member(root, "manifest.json"))
        interface = yaml.safe_load(safe_member(root, "agents/interface.yaml").read_text(encoding="utf-8"))
        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict):
            failures.append("技能 metadata 必须是对象")
        if not isinstance(interface, dict):
            failures.append("接口合同必须是对象")
        if (metadata.get("author") if isinstance(metadata, dict) else None) != "Hovo" or (manifest.get("owner") if isinstance(manifest, dict) else None) != "Hovo":
            failures.append("技能作者和包所有者必须保持为 Hovo")
        expected_name = root.name
        expected_version = metadata.get("version") if isinstance(metadata, dict) else None
        identities = {
            "root.name": expected_name, "frontmatter.name": frontmatter.get("name"),
            "manifest.name": manifest.get("name") if isinstance(manifest, dict) else None,
            "interface.name": interface.get("name") if isinstance(interface, dict) else None,
        }
        versions = {
            "frontmatter.metadata.version": expected_version,
            "manifest.version": manifest.get("version") if isinstance(manifest, dict) else None,
            "interface.version": interface.get("version") if isinstance(interface, dict) else None,
        }
        if any(not isinstance(value, str) or not value for value in identities.values()):
            failures.append("技能身份字段必须是非空字符串")
        elif len(set(identities.values())) != 1:
            failures.append("技能名称不一致: " + ", ".join(f"{key}={value}" for key, value in identities.items()))
        if any(not isinstance(value, str) or not value for value in versions.values()):
            failures.append("技能版本字段必须是非空字符串")
        elif len(set(versions.values())) != 1:
            failures.append("技能版本不一致: " + ", ".join(f"{key}={value}" for key, value in versions.items()))
        if not isinstance(frontmatter.get("description"), str) or not 1 <= len(frontmatter["description"]) <= 1024:
            failures.append("描述长度或类型不合格")
        if isinstance(metadata, dict) and any(not isinstance(value, str) for value in metadata.values()):
            failures.append("技能 metadata 必须使用字符串值")
        if len(skill_text.splitlines()) > 500:
            failures.append("入口超过500行，应移至按需材料")
        for token in ["能力问题", "不得伪造", "最多 1 轮", "最多 5 个", "BLOCKED", "INFERRED", "ASSUMED"]:
            if token not in skill_text:
                failures.append("缺少执行边界: " + token)
        output_contract = safe_member(root, "references/output-contract.md").read_text(encoding="utf-8")
        if "NOT_EXECUTED" not in output_contract:
            failures.append("缺少执行边界: NOT_EXECUTED")
        for rel in AUTHORED_MARKDOWN:
            document = safe_member(root, rel)
            failures.extend(local_links(root, rel, document.read_text(encoding="utf-8")))
        source_manifest = read_json(safe_member(root, "references/source-manifest.json"))
        if not isinstance(source_manifest, dict):
            failures.append("手册来源摘要必须是对象")
            books = None
        else:
            if source_manifest.get("source") != "金融语义工程手册" or source_manifest.get("version") != "V2.1":
                failures.append("手册来源摘要缺少来源或固定版本")
            books = source_manifest.get("files")
        if not isinstance(books, list) or len(books) != 4:
            failures.append("手册来源摘要必须准确列出四册原文")
        else:
            handbook_paths = set()
            for book in books:
                if not isinstance(book, dict) or not isinstance(book.get("path"), str) or not isinstance(book.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", book["sha256"]) or not isinstance(book.get("byteLength"), int) or book["byteLength"] <= 0:
                    failures.append("手册来源摘要条目格式不合格")
                    continue
                try:
                    handbook_paths.add(book["path"])
                    path = safe_member(root, book["path"])
                    data = path.read_bytes()
                    if hashlib.sha256(data).hexdigest() != book["sha256"] or len(data) != book["byteLength"]:
                        failures.append("手册原文摘要不一致: " + book["path"])
                    else:
                        verified.append(book["path"])
                except PackageError as exc:
                    failures.append(f"手册原文不可安全读取: {book.get('path')}: {exc}")
            if len(handbook_paths) != 4 or any(not path.startswith("references/金融语义工程手册_V2.1/") for path in handbook_paths):
                failures.append("手册来源摘要必须列出四册 V2.1 原文的精确相对路径")
        kit = root / "references/ecp-kit-1.7"
        kit_manifest = read_json(safe_member(root, "references/ecp-kit-1.7/manifest.json"))
        if not isinstance(kit_manifest, dict) or kit_manifest.get("kitVersion") != "1.7.0":
            failures.append("ECP 工具箱必须为 1.7.0")
        else:
            for item in kit_manifest.get("files", []):
                if not isinstance(item, dict):
                    failures.append("ECP 工具箱摘要条目格式不合格")
                    continue
                try:
                    path = safe_member(root, "references/ecp-kit-1.7/" + item["path"])
                    data = path.read_bytes()
                    if "sha256:" + hashlib.sha256(data).hexdigest() != item.get("contentDigest") or len(data) != item.get("byteLength"):
                        failures.append("工具箱摘要不一致: " + str(item.get("path")))
                    else:
                        verified.append("references/ecp-kit-1.7/" + item["path"])
                except (KeyError, PackageError) as exc:
                    failures.append(f"工具箱原文不可安全读取: {item.get('path') if isinstance(item, dict) else None}: {exc}")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError, json.JSONDecodeError, PackageError) as exc:
        failures.append(f"包检查未完成: {exc}")
    return {"ok": not failures, "status": "FAIL" if failures else "PASS", "failures": failures,
            "warnings": warnings, "verifiedAuthorityFiles": verified, "modelBehavior": "NOT_EXECUTED",
            "note": "这是制品与规范快照检查；公开许可和业务批准需独立确认"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", nargs="?", default=".")
    args = parser.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
