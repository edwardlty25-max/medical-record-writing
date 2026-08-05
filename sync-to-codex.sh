#!/usr/bin/env bash
# 将本 skill（Claude 权威副本）同步到 Codex 副本
# 用法：bash sync-to-codex.sh
set -e
SRC="$HOME/.claude/skills/medical-record-writing"
DST="$HOME/.codex/skills/medical-record-writing"
mkdir -p "$DST"
cp "$SRC/SKILL.md" "$DST/SKILL.md"
cp -r "$SRC/references" "$DST/references"
cp "$SRC/README.md" "$DST/README.md"
echo "[OK] 已同步 Claude → Codex：$DST"
