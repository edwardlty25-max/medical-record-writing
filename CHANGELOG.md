# Changelog

本文件记录 medical-record-writing 的重要变更。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [Unreleased]

## [1.13.0] - 2026-09-16

### Changed
- **指南库第三次联网复核（部分完成）**：10 个专科文件的版本状态改为逐项可审计表述——已复核项写明证据来源，未核实项明确标注「本次未能独立核实，沿用 2026-08-06 结论」。
- `guidelines/README.md` 新增**逐亚专业复核状态表**，并记明本轮检索通道限流的事实；下次复核提醒更新为 2026-12-15。
- 版本号统一至 1.13.0。

### 说明
- 本轮实测已复核 **13 项**：高血压 2024 修订版、心力衰竭 2024、NSTE-ACS 2024、2 型糖尿病 2025 版、血脂管理 2023、高尿酸血症与痛风 2024、GOLD 2026、GINA 2026、急性胰腺炎 2021、KDIGO CKD 2024、急性缺血性卒中 2023、帕金森病第四版、流行性感冒诊疗方案 2025 年版（来源含中华医学会系列期刊、goldcopd.org / gina.org / kdigo.org 官方站点、国家卫健委通知）。


## [1.12.1] - 2026-09-16

### Removed
- **撤回 1.12.0 的试验病例全套**（`references/examples/demo-case-01-*`，入院 + 一二三程 + 出院共 5 份）不再随仓库分发；仓库仅保留 3 份单文书示例，需要完整病例演练时由技能按模板现场生成。
- 同步移除 `SKILL.md` 中的试验病例入口行。

### Changed
- `references/guidelines/README.md` 指南总则更新：补入**下次复核提醒（2026-11-04，90 天）**与「示例不随包分发」说明。
- 版本号统一至 1.12.1。


## [1.12.0] - 2026-09-16

### Added
- `references/examples/demo-case-01-*.md`：**试验病例全套**——入院记录 + 首次病程（一程）+ 日常病程（二程、三程）+ 出院记录，同一患者、时间链与治疗线连贯；5 份均经 `validate_note.py` 校验为 **0 ERROR / 0 WARN**，并自动纳入 `run_tests.py` 回归基线。

### Removed
- `README.md` 删除 WorkBuddy 适配说明章节（不再宣称适配该平台）。


## [1.11.0] - 2026-09-16

### Added
- `scripts/check_consistency.py`：一致性门禁——版本号（以 plugin.json 为准）、模板结构、**单项否决时限三处比对**（rules.md ↔ validate_note.py ↔ SKILL.md）、文件可达性、YAML 字段块 lint、指南核验时效（>90 天提醒）。
- `scripts/check_privacy.py`（含 `--self-test`）：身份证 / 手机号 / 住院号 / 真实姓名样式扫描，合成标记白名单。
- `assets/quick-card.md`：**临床快用卡**——最小输入、输出约定、三个最常用现场、出稿后自检、三个最常见的坑。

### Fixed
- `references/transfer-and-death.md` 补回缺失的「书写要点」章节（v1.8.0 曾静默失败），并统一为「要点 / 模板 / 缺陷 / 自检」结构。
- 版本号统一至 1.11.0（此前 SKILL.md=1.4.0、README=v1.5.0、plugin.json=1.10.0 三处漂移）。
- `references/examples/first-progress-example.md` 由孤儿文件变为可从 SKILL.md / README 直达。
- `references/progress-note.md` 增加 `## 模板（按文书类型）` 分节，与其余模板结构对齐。

### Changed
- CI 增加「一致性与结构检查」「隐私扫描（含检测器自检）」两步。


## [1.10.0] - 2026-09-16

### Added
- `references/discharge-checklist.md`（3.9 KB）：出院记录复核清单——易漏要素、12 条常见缺陷、输出字段清单。
- `references/progress-checklist.md`（1.5 KB）：病程记录复核清单——6 条常见缺陷、输出字段清单。

### Changed
- 按「主文件只讲怎么写、复核内容独立成页」拆分：`discharge-summary.md` → 9.6 KB、`progress-note.md` → 6.3 KB，写文书时按需二次读取复核页。
- `SKILL.md` 与 `README.md` 增加两个复核清单入口；5 个模板版本标注同步至 v1.10.0。

（下次变更写在这里；发布时改为 `## [x.y.z] - YYYY-MM-DD` 并同步 `plugin.json` 版本号。）

## [1.9.0] - 2026-09-16

### Added
- 5 个文书模板新增**输出字段清单**（YAML，供结构化与对接 HIS）。
- 各模板顶部新增**版本与依据标注**，与 `rules.md` 的「来源与核验状态」对齐。
- `.gitattributes`：仓库内文本统一 LF，消除 Windows 端 CRLF 告警与噪音 diff。

### Changed
- `SKILL.md` 路由表中 `pumch-style.md` 的描述修正为「优秀病历标准与内涵质量（逐文书逻辑见对应模板）」。


## [1.8.0] - 2026-09-16

### Added
- 各文书模板统一为**「书写要点 + 模板 + 常见缺陷 + 自检」**四段式：admission-note.md、first-progress-note.md、progress-note.md、transfer-and-death.md、discharge-summary.md。
- `discharge-summary.md` 新增**「易漏要素」**清单（过敏史、输血及输血反应、上级医师意见、特殊情况、关键阴性结果、未解决问题出口），思考骨架同步补 `【上级医师意见】【输血与不良反应】【特殊情况】`。
- `validate_note.py` 新增 `allergy_history_missing`、`transfusion_reaction_unstated`（WARN）。

### Changed
- `pumch-style.md` 的「三、各文书书写逻辑」改为**路由索引**，逐文书逻辑下沉到各自模板文件，消除两处维护同一套逻辑的漂移风险。


## [1.7.0] - 2026-09-16

### Added
- `references/discharge-summary.md` 模板改为**两形态**：A 思考骨架（带【】标签，不得进入正文）+ B 成文形态（连续段落，可粘贴）；新增**取舍三原则**（趋势优先、正常同类合并、支撑诊断的写全）。
- `scripts/validate_note.py` 新增 6 条出院记录专有规则：`discharge_sections_missing`、`skeleton_label_leak`（均 ERROR）、`orders_categories_missing`、`no_recheck_plan`、`no_unsolved_closure`、`consult_note_copied`（WARN）。
- `tests/cases/bad-discharge.txt`：出院记录专有规则回归用例。

### Changed
- 缺陷表与自检清单标注机检覆盖情况，模板要求与规则码一一对应。


## [1.6.0] - 2026-09-16

### Added
- `references/discharge-summary.md` 重写：优秀出院小结 **7 步书写逻辑**（基线→定调→立据→时间线→演变→问题线→收口）、优化模板、出院医嘱四类要素、10 条常见缺陷、人工自检清单。
- `tests/cases/timepoint-false-positive.txt`：回归用例，锁定“采样时点不得判为时间未精确到分”。

### Fixed
- `scripts/validate_note.py`：修正 `HOUR_RE` 误报——“皮质醇（8 点）”等采样时点不再提示“时间未精确到分”。
- `SKILL.md`、`README.md`：出院记录条目注明含书写逻辑与自检清单。


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
