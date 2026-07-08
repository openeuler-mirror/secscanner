#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print a compact explanation of CVSS vector components."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', help='Optional files or directories to inspect')
    args = parser.parse_args()
    for raw_path in args.paths:
        path = Path(raw_path)
        state = 'present' if path.exists() else 'missing'
        print(f'{path}: {state}')
    if not args.paths:
        print(__doc__.strip())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())