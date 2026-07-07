#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Count log levels in a secScanner log file."""

from __future__ import annotations

import argparse
import ast
import collections
import configparser
import csv
import json
import re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_lines(paths):
    for raw in paths:
        path = Path(raw)
        for number, line in enumerate(read_text(path).splitlines(), 1):
            yield path, number, line


def emit(value: str) -> None:
    if value:
        print(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Input files or directories")
    parser.add_argument("--limit", type=int, default=100, help="Line length limit")
    parser.add_argument("--shell", default="nologin", help="Shell suffix for shell user filtering")
    args = parser.parse_args()
    mode = "log_levels"
    counter = collections.Counter()

    if mode.startswith("list_prefix_"):
        prefix = mode.rsplit("_", 1)[1]
        for raw in args.paths:
            for path in sorted(Path(raw).glob(f"{prefix}[0-9]*_*.py")):
                emit(str(path))
        return 0

    if mode in {"ini_sections", "ini_keys"}:
        config = configparser.ConfigParser()
        config.read(args.paths, encoding="utf-8")
        for section in config.sections():
            emit(section)
            if mode == "ini_keys":
                for key in config[section]:
                    emit(f"{section}.{key}")
        return 0

    if mode in {"json_keys", "json_count"}:
        for raw in args.paths:
            data = json.loads(read_text(Path(raw)))
            if mode == "json_keys" and isinstance(data, dict):
                for key in data:
                    emit(str(key))
            else:
                emit(f"{raw}: {len(data)}")
        return 0

    if mode in {"py_imports", "py_functions", "py_classes"}:
        for raw in args.paths:
            tree = ast.parse(read_text(Path(raw)), filename=raw)
            for node in ast.walk(tree):
                if mode == "py_imports" and isinstance(node, ast.Import):
                    for alias in node.names:
                        emit(alias.name)
                elif mode == "py_imports" and isinstance(node, ast.ImportFrom):
                    emit(node.module or "")
                elif mode == "py_functions" and isinstance(node, ast.FunctionDef):
                    emit(node.name)
                elif mode == "py_classes" and isinstance(node, ast.ClassDef):
                    emit(node.name)
        return 0

    patterns = {
        "ids": r"WRN_C\d+(?:_\d+)?:",
        "sugs": r"SUG_C\d+(?:_\d+)?:",
        "cve": r"CVE-\d{4}-\d{4,}",
        "unit_timer": r"[A-Za-z0-9_.@-]+\.timer",
        "unit_service": r"[A-Za-z0-9_.@-]+\.service",
        "advisory": r"openEuler-SA-\d{4}-\d{4}|OESA-\d{4}-\d{4}",
        "dates": r"\d{4}-\d{2}-\d{2}",
        "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "hostnames": r"\b[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+\b",
    }

    seen = set()
    for path, number, line in iter_lines(args.paths):
        if mode == "log_levels":
            match = re.search(r"\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]", line)
            if match:
                counter[match.group(1)] += 1
        elif mode in patterns:
            for match in re.findall(patterns[mode], line):
                emit(str(match))
        elif mode == "module_sort":
            match = re.search(r"[CSR](\d+)_", line)
            if match:
                emit(f"{int(match.group(1)):04d} {line}")
        elif mode == "non_empty" and line.strip():
            emit(line)
        elif mode == "duplicates":
            key = line.strip()
            if key in seen:
                emit(key)
            seen.add(key)
        elif mode == "kv_json":
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                counter[key] = value.strip().strip('"\'')
        elif mode == "rpm_names" and line.strip():
            emit(line.rsplit("-", 2)[0])
        elif mode == "rpm_arch":
            arch = line.rsplit(".", 1)[-1] if "." in line else "unknown"
            counter[arch] += 1
        elif mode == "state_summary":
            counter[line.strip()] += 1
        elif mode == "path_check":
            candidate = Path(line.strip())
            emit(f"{candidate}: {'present' if candidate.exists() else 'missing'}")
        elif mode == "html_title":
            match = re.search(r"<title>(.*?)</title>", line, re.I)
            if match:
                emit(match.group(1))
        elif mode == "html_links":
            for match in re.findall(r"href=['\"]([^'\"]+)", line, re.I):
                emit(match)
        elif mode == "md_headings" and line.startswith("#"):
            emit(line)
        elif mode == "md_links":
            for match in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line):
                emit(f"{match[0]} {match[1]}")
        elif mode == "branch_check":
            emit(f"{line}: {'ok' if re.match(r'^[a-z0-9._/-]+$', line) else 'invalid'}")
        elif mode == "ext_summary":
            p = Path(line.strip())
            counter[p.suffix or "<none>"] += 1
        elif mode == "shebang" and number == 1:
            emit(f"{path}: {'yes' if line.startswith('#!') else 'no'}")
        elif mode == "trailing" and line.rstrip() != line:
            emit(f"{path}:{number}")
        elif mode == "tabs" and line.startswith("\t"):
            emit(f"{path}:{number}")
        elif mode == "long_lines" and len(line) > args.limit:
            emit(f"{path}:{number}:{len(line)}")
        elif mode == "utf8":
            emit(f"{path}: ok")
            break
        elif mode == "csv_cols" and number == 1:
            emit(f"{path}: {len(next(csv.reader([line])))}")
        elif mode == "audit_keys":
            match = re.search(r"-k\s+(\S+)", line)
            if match:
                emit(match.group(1))
        elif mode == "ssh_options":
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                emit(stripped.split()[0])
        elif mode == "sysctl_keys" and "=" in line:
            emit(line.split("=", 1)[0].strip())
        elif mode == "passwd_users" and ":" in line:
            emit(line.split(":", 1)[0])
        elif mode == "group_names" and ":" in line:
            emit(line.split(":", 1)[0])
        elif mode == "shadow_empty":
            parts = line.split(":")
            if len(parts) > 1 and parts[1] == "":
                emit(parts[0])
        elif mode == "login_defs":
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                emit(stripped.split()[0])
        elif mode == "shell_users":
            parts = line.split(":")
            if len(parts) >= 7 and parts[-1].endswith(args.shell):
                emit(parts[0])
        elif mode == "home_prefix":
            parts = line.split(":")
            if len(parts) >= 6:
                counter[Path(parts[5]).parts[0] if Path(parts[5]).parts else ""] += 1
        elif mode == "severity":
            for token in re.findall(r"\b(low|medium|high|critical)\b", line, re.I):
                counter[token.lower()] += 1

    if mode == "kv_json":
        print(json.dumps(dict(counter), ensure_ascii=False, sort_keys=True))
    else:
        for key, value in sorted(counter.items()):
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())