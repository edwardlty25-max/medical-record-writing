#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仓库自检：Markdown 链接完整性 + SKILL.md frontmatter 规范。

用法：
    python scripts/check_links.py

退出码：0 = 通过；1 = 存在问题。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\]\(([^)]+)\)")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKIP_PREFIX = ("http://", "https://", "mailto:", "#", "www.")


def check_links() -> list[str]:
    problems = []
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if target.startswith(SKIP_PREFIX):
                continue
            target = target.split("#", 1)[0].strip()
            if not target:
                continue
            if not (md.parent / target).exists():
                problems.append(f"{md.relative_to(ROOT)} -> 链接目标不存在：{target}")
    return problems


def parse_frontmatter(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.startswith((" ", "\t", "-", "#")):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def check_frontmatter() -> list[str]:
    problems = []
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        return ["SKILL.md 不存在"]
    text = skill.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return ["SKILL.md 缺少 YAML frontmatter"]
    end = text.find("\n---", 3)
    if end == -1:
        return ["SKILL.md frontmatter 未闭合"]
    fields = parse_frontmatter(text[3:end])

    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not name:
        problems.append("frontmatter 缺少 name")
    elif not NAME_RE.match(name) or len(name) > 64:
        problems.append(f"name 不符合规范（小写字母/数字/连字符，≤64 字符）：{name}")
    if not desc:
        problems.append("frontmatter 缺少 description")
    elif len(desc) > 1024:
        problems.append(f"description 超过 1024 字符（现 {len(desc)}）")
    if desc and not any(word in desc for word in ("不用于", "不得用于", "仅供")):
        problems.append("description 建议写明不适用场景（如“不用于患者自我诊疗”）")
    return problems


def main() -> int:
    problems = check_links() + check_frontmatter()
    if problems:
        print(f"检查未通过（{len(problems)} 项）：")
        for item in problems:
            print(" -", item)
        return 1
    print("检查通过：Markdown 链接完整，SKILL.md frontmatter 合规。")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
