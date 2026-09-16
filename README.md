# medical-record-writing — 内科病历书写加速器

> **⚠ 免责声明**：本工具为**执业医师**的文书书写与临床决策支持辅助，输出不构成医学建议，不替代主治医师的独立判断；**不得用于患者自我诊疗**。用药须核对禁忌、过敏史、肝肾功能与药物相互作用；指南摘要基于公开资料，请以最新指南原文为准。

本地 Claude Code / Codex 插件（Codex 侧以 `~/.codex/skills` 目录加载），面向执业医师。

**主旨**：把医生给的零散事实（口述、草稿、粘贴的化验与检查结果）在**一次交互内**转成**可直接粘贴进 HIS 的规范病历正文**，并在出稿前跑一遍**确定性规范自检**。

- **默认路径 · 病历书写（加速器）**：口述、草稿笔记、检查结果 → 标准病历文书。规范基准为**《河北省病历书写规范（2013年版）》（冀卫办医政〔2013〕30号）**；标注「2023 补充」的条目**未核实到统一文号**，须与本医院现行版本核对（见 references/rules.md 的「来源与核验状态」）。书写逻辑参考优秀内科病历的病例链、诊断层级与决策表达。
- **可选旁路 · 病情分析与治疗方案**：仅在医生明确要求时启用；在已有**文字或图片**（化验单、检查报告照片等）基础上，提供分级诊断、事实依据、鉴别诊断，并按风险分层核验指南依据。

## 快速开始

> 一屏速查：[assets/quick-card.md](assets/quick-card.md)（最小输入 · 输出约定 · 出稿后自检命令）

1. 直接把口述或草稿发给本技能（例如：「写今天的日常病程，3 床老王……」）。需要哪些字段可参考 [assets/intake-form.md](assets/intake-form.md)，**整段口述即可，无需按格式填写**。
2. 技能输出**可直接粘贴进 HIS 的正文**；缺信息标【待补充】，或在出稿前最多追问 3 个关键问题。可另附一行自检结论，正文之外的辅助块仅在索取时输出。
3. 需要确定性自检时（本仓库自带，无第三方依赖）：

```bash
python scripts/validate_note.py 正文.txt --kind progress --admit "2026-09-16 08:00"
```

`--kind` 取 `admission` / `admission-readmission` / `first-progress` / `progress` / `rounds-critical` / `rounds-attending` / `rounds-director` / `handover` / `rescue` / `consultation` / `discharge` / `death` / `death-discussion` / `transfer`。退出码 `1` 表示存在 ERROR 级问题；`--json` 便于接入脚本。

## 支持的文书类型（默认路径）

| 文书 | 模板 |
|---|---|
| 入院记录（四类） | references/admission-note.md |
| 首次病程记录 | references/first-progress-note.md |
| 日常病程记录、上级查房、交接班、抢救、会诊 | references/progress-note.md |
| 出院记录（书写逻辑 + 两形态模板） | references/discharge-summary.md |
| 出院记录复核清单（易漏要素、常见缺陷、字段） | references/discharge-checklist.md |
| 病程记录复核清单（常见缺陷、字段） | references/progress-checklist.md |
| 转科记录、死亡记录、死亡讨论 | references/transfer-and-death.md |
| 书写规范（2013 年版规范 + 协和逻辑） | references/rules.md |
| 协和病历书写逻辑专题 | references/pumch-style.md |
| 输入字段清单 | assets/intake-form.md |
| 成稿示例（虚构数据） | daily-progress-example.md · first-progress-example.md · discharge-example.md（references/examples/） |

## 可选旁路（分析与治疗）

仅在医生明确要求时启用，且**输出不得混入病历正文**：

- 流程：references/case-analysis.md
- 诊断依据：references/clinical-diagnosis.md —— 区分医生已确认、支持诊断、拟诊/待排除和资料不足。
- 临床推理与治疗计划：references/clinical-reasoning-treatment.md —— 组织主要诊断、补充诊断、治疗目标、具体处理、监测与调整条件。
- 指南：references/guidelines/ —— 覆盖 10 个亚专业、80+ 病种要点（2026-08-06 二次核对扩充，优先中华医学会系列指南）；**不加载整库**，按主问题路由。

## 使用方式

对话中直接说触发短语即可（无需前缀命令）：

| 触发短语（示例） | 路径 |
|---|---|
| 「帮我写一份入院记录」「写首次病程」「写日常病程」「写出院记录」「按河北规范写病程」「按协和标准」 | 默认（文书加速） |
| 「帮我分析这个患者」「解读这张化验单/检查报告」「诊断依据」「给出治疗方案」「诊断鉴别」「病情分析」 | 可选旁路（需明确要求） |

完整触发词见 SKILL.md 的 frontmatter description。

## 安装与更新

### Claude Code

**GitHub Marketplace（推荐）：**
```bash
claude plugin marketplace add edwardlty25-max/medical-record-writing
claude plugin install medical-record-writing@medical-record-writing
```

**更新：** 作者推送新版本后，使用者运行：
```bash
claude plugin marketplace update medical-record-writing
claude plugin update medical-record-writing   # 重启后生效
```

### Codex

Codex 从 `$CODEX_HOME/skills/`（默认 `~/.codex/skills/`）加载技能；技能目录只要包含 `SKILL.md` 即可被自动发现，**不需要** `.claude-plugin/` 清单。

**直接安装：**
```powershell
git clone https://github.com/edwardlty25-max/medical-record-writing.git "$env:USERPROFILE\.codex\skills\medical-record-writing"
```
或手动复制本目录到 `~/.codex/skills/medical-record-writing/`。

**Codex 更新：** 在 `~/.codex/skills/medical-record-writing/` 目录执行 `git pull`（或重新克隆/复制）。重启 Codex 会话后生效。

**Codex 卸载：** 删除 `~/.codex/skills/medical-record-writing/` 目录即可。

## 重要说明

- **指南使用**：快速文书不加载指南库；诊断、鉴别或治疗请求才按主问题读取相应亚专业摘要。具体诊断阈值、剂量、疗程、禁忌、相互作用及急危重决策须先核对权威来源。核验失败时降级为原则性建议并标注“版本待核实”（见 references/guidelines/README.md）。
- **安全边界**：可选旁路的分析为临床决策支持，不替代主治医师判断；不虚构数据；危重征象优先警示；具体药物剂量、疗程和高风险方案须经指南/说明书核验；不面向患者使用。
- **自检边界**：`scripts/validate_note.py` 只检查格式与规范中可机检的部分（主诉字数、时限、计量单位、商品名、签名、占位符等），**不判断医学内容正确性**，也不替代医院质控与医师本人签名。
- **规范来源**：基准为《河北省病历书写规范（2013年版）》（冀卫办医政〔2013〕30号）；标注「2023 补充」的条目未核实到统一文号，须与本院现行版本核对。详见 references/rules.md 的「来源与核验状态」。
- **仓库级自检**：`python scripts/check_links.py && python scripts/run_tests.py`，CI 见 `.github/workflows/validate.yml`。

## 开发说明

- 结构：`.claude-plugin/plugin.json` 与 `marketplace.json` 为 Claude 插件清单；`SKILL.md` 为主指令（快路径 + 输出契约 + 硬红线）；`assets/intake-form.md` 为输入字段清单；`references/` 为模板、规范（含「来源与核验状态」）、安全边界、示例与指南；`scripts/` 为确定性自检与工程校验；`tests/` 为回归用例；`.github/workflows/validate.yml` 为 CI。Codex 侧无需 `.claude-plugin/`，直接以目录形式加载 `SKILL.md`（另见 `AGENTS.md`）。
- 协作：贡献前请读 `CONTRIBUTING.md`；变更记录见 `CHANGELOG.md`；规范纠错请用 issue 模板。
- 版本：v1.14.2 · 作者 edwardlty25-max（MIT License）
- 卸载：删除本地安装目录即卸载（Marketplace 安装者使用 claude plugin 对应命令）。