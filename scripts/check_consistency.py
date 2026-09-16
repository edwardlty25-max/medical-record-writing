#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一致性检查：版本号、模板结构、时限三处、文件可达性、YAML 字段块、指南时效。

用法：
    python scripts/check_consistency.py

退出码：存在 ERROR → 1；仅有 WARN 或全部通过 → 0。
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = [
    "admission-note.md",
    "first-progress-note.md",
    "progress-note.md",
    "discharge-summary.md",
    "transfer-and-death.md",
]
MAX_GUIDELINE_AGE_DAYS = 90

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def headings(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("## ")]


def has_heading(text: str, keyword: str) -> bool:
    return any(keyword in h for h in headings(text))


# ---------------------------------------------------------------- 1 版本号

def check_versions() -> None:
    try:
        plugin = json.loads(read(ROOT / ".claude-plugin" / "plugin.json"))
    except json.JSONDecodeError as exc:
        err(f"plugin.json 无法解析：{exc}")
        return
    version = plugin.get("version", "")
    if not version:
        err(".claude-plugin/plugin.json 缺少 version")
        return

    m = re.search(r"(?m)^version:\s*([\d.]+)", read(ROOT / "SKILL.md"))
    if not m:
        err("SKILL.md frontmatter 缺少 version")
    elif m.group(1) != version:
        err(f"版本不一致：SKILL.md={m.group(1)} vs plugin.json={version}")

    m = re.search(r"- 版本：v?([\d.]+)", read(ROOT / "README.md"))
    if not m:
        warn("README.md 未找到「- 版本：vX.Y.Z」行")
    elif m.group(1) != version:
        err(f"版本不一致：README.md={m.group(1)} vs plugin.json={version}")

    for name in TEMPLATES:
        text = read(ROOT / "references" / name)
        m = re.search(r"版本 v([\d.]+)", text)
        if not m:
            err(f"{name} 缺少版本标注")
        elif m.group(1) != version:
            err(f"版本不一致：{name}={m.group(1)} vs plugin.json={version}")

    if f"## [{version}]" not in read(ROOT / "CHANGELOG.md"):
        err(f"CHANGELOG.md 缺少 [{version}] 条目")


# ---------------------------------------------------------------- 2 模板结构

def check_template_structure() -> None:
    for name in TEMPLATES:
        text = read(ROOT / "references" / name)
        for keyword in ("书写", "模板", "自检"):
            if not has_heading(text, keyword):
                err(f"{name} 缺少含「{keyword}」的二级章节")
        if "常见缺陷" not in text and "-checklist.md" not in text:
            warn(f"{name} 既无「常见缺陷」章节，也未指向复核清单")


# ---------------------------------------------------------------- 3 时限一致性

# 人类可读来源 = references/rules.md；机器来源 = scripts/validate_note.py 的 KINDS
DEADLINE_PAIRS = [
    ("入院记录", "admission"),
    ("首次病程记录", "first-progress"),
    ("新入院危重患者上级医师查房记录", "rounds-critical"),
    ("主治医师首次查房记录", "rounds-attending"),
    ("科主任或副高以上医师首次查房记录", "rounds-director"),
    ("抢救记录", "rescue"),
    ("出院记录", "discharge"),
    ("死亡记录", "death"),
]


def parse_kinds() -> dict[str, int]:
    out: dict[str, int] = {}
    text = read(ROOT / "scripts" / "validate_note.py")
    for m in re.finditer(r'(?m)^\s*"([a-z\-]+)":\s*\("[^"]*",\s*(None|\d+)', text):
        if m.group(2) != "None":
            out[m.group(1)] = int(m.group(2))
    return out


def parse_rules_hours() -> dict[str, int]:
    out: dict[str, int] = {}
    for line in read(ROOT / "references" / "rules.md").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = re.search(r"(\d+)\s*小时", cells[1])
        if m:
            out[cells[0].replace("**", "")] = int(m.group(1))
    return out


def check_deadlines() -> None:
    kinds = parse_kinds()
    rules = parse_rules_hours()
    for label, key in DEADLINE_PAIRS:
        doc = next((v for k, v in rules.items() if label in k), None)
        if doc is None:
            err(f"rules.md 未找到时限行：{label}")
            continue
        if key not in kinds:
            err(f"validate_note.py KINDS 缺少：{key}")
            continue
        if doc * 60 != kinds[key]:
            err(f"时限不一致：{label} 文档={doc}h，代码={kinds[key]}min")

    # 注意：frontmatter description 里也含「单项否决时限」，需取极值表所在行（含小时数）
    lines = [l for l in read(ROOT / "SKILL.md").splitlines() if "单项否决时限" in l]
    if not lines:
        warn("SKILL.md 未找到「单项否决时限」行")
    else:
        hours_set = sorted(set(rules.values()))
        missing = [h for h in hours_set
                   if not any(f"{h}h" in l or f"{h} 小时" in l for l in lines)]
        if missing:
            err("SKILL.md 硬红线表未包含时限：" + "、".join(f"{h} 小时" for h in missing))


# ---------------------------------------------------------------- 4 可达性

def check_reachability() -> None:
    texts = {p: read(p) for p in ROOT.rglob("*.md") if ".git" not in p.parts}
    for base in (ROOT / "references", ROOT / "assets"):
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if not any(path.name in t for p, t in texts.items() if p != path):
                err(f"文件未被任何文档引用（不可达）：{path.relative_to(ROOT)}")


# ---------------------------------------------------------------- 5 YAML 字段块

def check_yaml_blocks() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        for block in re.finditer(r"```yaml\n(.*?)```", read(path), re.S):
            for i, line in enumerate(block.group(1).splitlines(), 1):
                if not line.strip() or line.strip().startswith("#"):
                    continue
                if "\t" in line:
                    err(f"{path.name} YAML 第 {i} 行含 TAB")
                    continue
                if ":" not in line:
                    err(f"{path.name} YAML 第 {i} 行缺少键值分隔：{line.strip()[:40]}")
                    continue
                key = line.split(":", 1)[0].strip()
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                    err(f"{path.name} YAML 第 {i} 行键名不合法：{key[:40]}")


# ---------------------------------------------------------------- 6 指南时效

def check_guideline_freshness() -> None:
    found: list[tuple[date, str]] = []
    for path in sorted((ROOT / "references" / "guidelines").glob("*.md")):
        for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})", read(path)):
            try:
                found.append((date(int(m.group(1)), int(m.group(2)), int(m.group(3))), path.name))
            except ValueError:
                continue
    if not found:
        warn("未在指南文件中找到核验日期")
        return
    newest, source = max(found)
    age = (date.today() - newest).days
    if age > MAX_GUIDELINE_AGE_DAYS:
        warn(f"指南核验日期最新为 {newest}（{age} 天前，见 {source}），超过 {MAX_GUIDELINE_AGE_DAYS} 天，建议复核")


def main() -> int:
    check_versions()
    check_template_structure()
    check_deadlines()
    check_reachability()
    check_yaml_blocks()
    check_guideline_freshness()
    for item in warnings:
        print("WARN  " + item)
    for item in errors:
        print("ERROR " + item)
    print(f"\n一致性检查：{len(errors)} ERROR / {len(warnings)} WARN")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
