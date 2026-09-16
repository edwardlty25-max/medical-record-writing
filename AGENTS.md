# AGENTS.md

面向 Codex / Cursor 等按目录加载技能的 agent。技能主体见 [SKILL.md](SKILL.md)；**无需** `.claude-plugin/` 清单即可使用。

## 这个仓库是什么

`medical-record-writing`：面向中国执业医师的**内科病历书写加速器**。默认路径是把口述、草稿或检查结果**一次**转成可直接粘贴进 HIS 的规范病历正文，并执行确定性自检；诊断与治疗分析是可选旁路。

## 目录

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主指令：触发、快路径、输出契约、硬红线、安全边界 |
| `assets/intake-form.md` | 输入字段清单（给医生） |
| `references/*.md` | 文书模板与规范 |
| `references/safety-boundaries.md` | 允许/禁止边界与底线话术 |
| `references/examples/` | 虚构数据的成稿示例（同时是回归基线） |
| `references/guidelines/` | 10 个亚专业指南摘要，仅旁路按需读取 |
| `scripts/validate_note.py` | 确定性自检 |
| `scripts/check_links.py`、`scripts/run_tests.py` | 工程校验 |

## 改动约束

1. **不虚构医学与法规内容**；无法核实的来源标【来源待核验】。
2. 默认不动 `references/guidelines/`；更新指南须同步更新其 `README.md` 的核验日期。
3. 修改校验规则必须补测试用例。
4. 提交前运行：

```bash
python scripts/check_links.py && python scripts/check_consistency.py && python scripts/check_privacy.py && python scripts/run_tests.py
```
