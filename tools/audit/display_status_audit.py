#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Display calls and their status arguments."""

from __future__ import annotations

import argparse
import ast
import configparser
import json
import os
import re
import stat
import xml.etree.ElementTree as ET
from pathlib import Path


def iter_files(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            yield from (item for item in path.rglob("*") if item.is_file())
        elif path.is_file():
            yield path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def emit(path: Path, detail: str) -> None:
    print(f"{path}: {detail}")


def python_files(paths):
    return [path for path in iter_files(paths) if path.suffix == ".py"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    parser.add_argument("--mode", choices=["baseline_map", "module_names", "test_names", "asset_ext", "config_required", "service_sections", "timer_sections", "license_header", "coding_cookie", "main_guard", "import_star", "shell_command", "systemctl", "rpm_command", "yum_dnf", "hardcoded_path", "logger_calls", "display_calls", "gconfig_keys", "result_codes", "security_ids", "placeholders", "html_charset", "json_valid", "xml_valid", "db_files", "empty_files", "large_files", "executable", "readme_headings", "manpage_sections", "spec_fields", "requirements", "dependency_imports", "non_ascii_comments", "doc_links", "relative_links", "images", "css", "js"], default=None, help="Override the audit mode")
    parser.add_argument("--limit", type=int, default=1048576, help="Size limit for large file checks")
    args = parser.parse_args()
    mode = args.mode or "display_calls"

    if mode == "baseline_map":
        for root in args.paths:
            base = Path(root)
            for benchmark in sorted((base / "secScanner" / "enhance").glob("*")):
                if benchmark.is_dir():
                    emit(benchmark, "check=%s set=%s" % ((benchmark / "check").is_dir(), (benchmark / "set").is_dir()))
        return 0

    if mode in {"module_names", "test_names", "asset_ext", "db_files", "empty_files", "large_files", "executable", "images", "css", "js"}:
        for path in iter_files(args.paths):
            name = path.name
            if mode == "module_names" and path.suffix == ".py" and re.match(r"[CSR]\d+_", name):
                emit(path, "module")
            elif mode == "test_names" and path.suffix == ".py" and re.match(r"Test[CS]\d+_", name):
                emit(path, "test")
            elif mode == "asset_ext":
                emit(path, path.suffix or "<none>")
            elif mode == "db_files" and path.suffix in {".db", ".sqlite", ".sqlite3"}:
                emit(path, str(path.stat().st_size))
            elif mode == "empty_files" and path.stat().st_size == 0:
                emit(path, "empty")
            elif mode == "large_files" and path.stat().st_size > args.limit:
                emit(path, str(path.stat().st_size))
            elif mode == "executable" and os.access(path, os.X_OK):
                emit(path, "executable")
            elif mode == "images" and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg"}:
                emit(path, path.suffix.lower())
            elif mode == "css" and path.suffix.lower() == ".css":
                emit(path, str(path.stat().st_size))
            elif mode == "js" and path.suffix.lower() == ".js":
                emit(path, str(path.stat().st_size))
        return 0

    if mode in {"config_required", "service_sections", "timer_sections"}:
        required = {
            "config_required": {"main"},
            "service_sections": {"Unit", "Service", "Install"},
            "timer_sections": {"Unit", "Timer", "Install"},
        }[mode]
        for path in iter_files(args.paths):
            config = configparser.ConfigParser()
            config.read(path, encoding="utf-8")
            missing = sorted(required.difference(config.sections()))
            emit(path, "missing=" + ",".join(missing) if missing else "ok")
        return 0

    if mode in {"json_valid", "xml_valid"}:
        for path in iter_files(args.paths):
            try:
                if mode == "json_valid":
                    json.loads(read_text(path))
                else:
                    ET.fromstring(read_text(path))
                emit(path, "ok")
            except Exception as exc:
                emit(path, f"error={exc}")
        return 0

    patterns = {
        "shell_command": r"getstatusoutput\(|shell=True|os\.system\(",
        "systemctl": r"systemctl\s+",
        "rpm_command": r"\brpm\s+",
        "yum_dnf": r"\b(?:yum|dnf)\s+",
        "hardcoded_path": r"['\"]/(?:etc|var|usr|opt|home|root)/[^'\"]+",
        "logger_calls": r"logger\.(debug|info|warning|error|critical)\(",
        "display_calls": r"Display\((.*?)\)",
        "gconfig_keys": r"(?:set_value|get_value)\(['\"]([^'\"]+)",
        "result_codes": r"(?:WRN|SUG)_C\d+(?:_\d+)?:",
        "security_ids": r"\b[CSR]\d+_",
        "placeholders": r"\{\{.*?\}\}|\$\{.*?\}",
        "spec_fields": r"^(Name|Version|Release|Summary|License|URL|Source\d*):",
        "doc_links": r"https?://[^)\s]+",
        "relative_links": r"\[[^\]]+\]\((?!https?://)([^)]+)\)",
    }

    for path in iter_files(args.paths):
        text = read_text(path)
        if mode == "license_header" and path.suffix == ".py":
            emit(path, "yes" if "Mulan PSL" in text else "no")
        elif mode == "coding_cookie" and path.suffix == ".py":
            first_two = "\n".join(text.splitlines()[:2])
            emit(path, "yes" if "coding" in first_two or "utf-8" in first_two.lower() else "no")
        elif mode == "main_guard" and path.suffix == ".py":
            emit(path, "yes" if "if __name__" in text else "no")
        elif mode == "import_star" and path.suffix == ".py":
            if "import *" in text:
                emit(path, "wildcard import")
        elif mode == "html_charset" and path.suffix.lower() in {".html", ".htm"}:
            emit(path, "yes" if "charset=\"utf-8\"" in text.lower() or "charset=utf-8" in text.lower() else "no")
        elif mode == "readme_headings" and path.name.lower().startswith("readme"):
            for line in text.splitlines():
                if line.startswith("#"):
                    emit(path, line)
        elif mode == "manpage_sections":
            for line in text.splitlines():
                if line.startswith(".") and len(line) > 1:
                    emit(path, line)
        elif mode == "requirements" and path.name == "requirements.txt":
            for line in text.splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    emit(path, "pinned" if "==" in stripped else "unpinned")
        elif mode == "dependency_imports" and path.suffix == ".py":
            try:
                tree = ast.parse(text)
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        emit(path, alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    emit(path, node.module.split(".")[0])
        elif mode == "non_ascii_comments" and path.suffix == ".py":
            for number, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith("#") and any(ord(ch) > 127 for ch in line):
                    emit(path, str(number))
        elif mode in patterns:
            for match in re.findall(patterns[mode], text, re.MULTILINE):
                emit(path, str(match))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())