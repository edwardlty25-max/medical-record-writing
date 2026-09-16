#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""隐私扫描：防止真实病历 / 患者标识符被提交进仓库。

用法：
    python scripts/check_privacy.py
    python scripts/check_privacy.py --self-test    # 验证检测器本身有效（CI 会跑）

判定：命中身份证 / 手机号 / 住院号 / 真实姓名样式时，若同行含明显合成标记
（××、__、连续 0、【待补充】、示例、虚构 等）则放行；否则报 ERROR。

退出码：0 = 通过；1 = 发现疑似真实患者数据。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_FILES = {"scripts/check_privacy.py"}  # 本文件含用于自检的样例串
BINARY_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".woff", ".woff2", ".ttf"}

PATTERNS = [
    ("身份证号", re.compile(r"\b\d{17}[\dXx]\b")),
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("住院号/病案号", re.compile(r"(?:住院号|病案号|门诊号)\s*[:：]\s*[A-Za-z0-9\-]{4,}")),
    ("真实姓名样式", re.compile(r"姓名\s*[:：]\s*[\u4e00-\u9fa5]{2,4}(?![\u4e00-\u9fa5])")),
]
SYNTHETIC = re.compile(r"[×Xx*]{2,}|_{2,}|0{4,}|【|待补充|待核实|示例|虚构|\{|\$")


def scan_text(name: str, text: str) -> list[str]:
    hits: list[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in PATTERNS:
            for m in pattern.finditer(line):
                if SYNTHETIC.search(m.group(0)) or SYNTHETIC.search(line):
                    continue
                hits.append(f"{name}:{lineno} 疑似{label}：{m.group(0)[:24]}")
    return hits


def self_test() -> int:
    sample = (
        "姓名：王建国\n"
        "身份证号：11010119900307551X\n"
        "住院号：A123456\n"
        "联系电话：13800138000\n"
    )
    labels = {h.split("疑似")[1].split("：")[0] for h in scan_text("self-test", sample)}
    need = {"身份证号", "手机号", "住院号/病案号", "真实姓名样式"}
    missing = need - labels
    if missing:
        print("自检失败：未检出 " + "、".join(sorted(missing)))
        return 1
    print("自检通过：四类模式均可检出")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    hits: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if str(path.relative_to(ROOT)).replace("\\", "/") in SKIP_FILES:
            continue
        if path.suffix.lower() in BINARY_SUFFIX:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits.extend(scan_text(str(path.relative_to(ROOT)), text))

    for item in hits:
        print("ERROR " + item)
    print(f"\n隐私扫描：{len(hits)} 处疑似真实患者数据")
    return 1 if hits else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
