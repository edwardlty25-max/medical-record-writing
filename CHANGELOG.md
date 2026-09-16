# Changelog

本文件记录 medical-record-writing 的重要变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [Unreleased]

## [1.5.0] - 2026-09-16

### Added
- `references/safety-boundaries.md`：允许/禁止对照表、底线话术、急危重信号、隐私与职责边界。
- `references/examples/first-progress-example.md`、`references/examples/discharge-example.md`：虚构数据的成稿示例。
- `scripts/check_links.py`：Markdown 链接完整性与 SKILL.md frontmatter 检查。
- `scripts/run_tests.py` + `tests/cases/`：校验器回归测试（示例稿必须通过、故障稿必须被拦截）。
- `.github/workflows/validate.yml`：CI 自动执行上述检查。
- `AGENTS.md`、`CONTRIBUTING.md`、`.github/ISSUE_TEMPLATE/`：协作与规范纠错入口。

### Changed
- 规范名称修正为**《河北省病历书写规范（2013年版）》（冀卫办医政〔2013〕30号）**（此前误写为“细则”），并同步 5 个模板文件。
- `references/rules.md` 新增「来源与核验状态」；对“2023 补充/修订”条目标注【来源待核验】。
- `scripts/validate_note.py`：`公斤` 由警告升级为**错误**（统一写 kg）。

## [1.4.0] - 2026-09-16

### Added
- `assets/intake-form.md`：按文书类型的最小输入字段清单（缺字段最多追问 1 轮、最多 3 问）。
- `scripts/validate_note.py`：确定性机检（主诉字数、单项否决时限、计量单位、商品名、签名、占位符等）。
- `references/examples/daily-progress-example.md`：日常病程成稿示例。

### Changed
- `SKILL.md` 重写：默认快路径（定文书 → 取事实 → 出稿自检）、输出契约（默认只输出可粘贴正文）、10 条规范硬红线；原“模式 A/B”改为「默认路径 / 可选旁路」。
- 修复 `references/case-analysis.md` 的失效引用（「安全与边界」→「安全边界」）。
- `README.md`、`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json` 同步 v1.4.0。

## [1.3.1] 及更早
- 历史版本见 git 提交记录。
