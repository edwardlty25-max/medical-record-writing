#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回归测试：示例稿必须通过、故意出错的用例必须被拦截。

用法：
    python scripts/run_tests.py

退出码：0 = 全部通过；1 = 有失败。

数据来源：
- `references/examples/*.md`：文件内含 `<!-- kind=xxx -->` 标记，取第一个代码块作为正文，要求自检通过（0 ERROR）。
- `tests/cases/*.txt` + `tests/cases/expected.json`：期望退出码与必须命中的规则码。
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = ROOT / "scripts" / "validate_note.py"
FENCE_RE = re.compile(r"```[^\n]*\n(.*?)\n```", re.S)
KIND_RE = re.compile(r"<!--\s*kind=([a-z][a-z0-9\-]*)\s*-->")


def run_validator(text: str, kind: str, admit: str | None = None):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
        fh.write(text)
        tmp = fh.name
    cmd = [sys.executable, str(VALIDATOR), tmp, "--kind", kind, "--json"]
    if admit:
        cmd += ["--admit", admit]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    Path(tmp).unlink(missing_ok=True)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = {"findings": [], "errors": -1, "raw": proc.stdout + proc.stderr}
    return proc.returncode, data


def check_examples() -> list[tuple[bool, str]]:
    results = []
    example_dir = ROOT / "references" / "examples"
    for md in sorted(example_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        kind_match = KIND_RE.search(text)
        fence = FENCE_RE.search(text)
        if not kind_match or not fence:
            results.append((False, f"{md.name}: 缺少 <!-- kind=... --> 标记或代码块"))
            continue
        code, data = run_validator(fence.group(1), kind_match.group(1))
        errors = data.get("errors", -1)
        ok = code == 0 and errors == 0
        results.append((ok, f"{md.name}（kind={kind_match.group(1)}）：exit={code} errors={errors}"))
    return results


def check_cases() -> list[tuple[bool, str]]:
    spec_file = ROOT / "tests" / "cases" / "expected.json"
    if not spec_file.exists():
        return [(False, "tests/cases/expected.json 不存在")]
    spec = json.loads(spec_file.read_text(encoding="utf-8"))
    results = []
    for case in spec.get("cases", []):
        path = ROOT / "tests" / "cases" / case["file"]
        if not path.exists():
            results.append((False, f"tests/cases/{case['file']}: 文件不存在"))
            continue
        code, data = run_validator(path.read_text(encoding="utf-8"), case["kind"], case.get("admit"))
        got = {f["code"] for f in data.get("findings", [])}
        want = set(case.get("expect_codes", []))
        missing = want - got
        ok = code == case["expect_exit"] and not missing
        detail = f"exit={code}（期望 {case['expect_exit']}）"
        if missing:
            detail += f"，未命中规则码：{sorted(missing)}"
        results.append((ok, f"tests/cases/{case['file']}: {detail}"))
    return results


def main() -> int:
    results = check_examples() + check_cases()
    failed = [msg for ok, msg in results if not ok]
    for ok, msg in results:
        print(("PASS  " if ok else "FAIL  ") + msg)
    print(f"\n合计：{len(results) - len(failed)} 通过 / {len(failed)} 失败")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
