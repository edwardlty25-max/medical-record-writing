# medical-record-writing — 内科病历书写与病情分析助手

> **⚠ 免责声明**：本工具为**执业医师**的文书书写与临床决策支持辅助，输出不构成医学建议，不替代主治医师的独立判断；**不得用于患者自我诊疗**。用药须核对禁忌、过敏史、肝肾功能与药物相互作用；指南摘要基于公开资料，请以最新指南原文为准。

本地 Claude Code / Codex 插件（Codex 侧以 `~/.codex/skills` 目录加载），面向执业医师，提供**双模式**：

- **模式 A · 病历书写**：把口述、草稿笔记、检查结果整理成标准病历文书。规范基准为**《河北省病历书写规范细则（2013年版）》（冀卫办医政〔2013〕30号）**为主体、**2023 修订要点**为补充，书写逻辑参考优秀内科病历的病例链、诊断层级与决策表达。
- **模式 B · 病情分析与治疗方案指导**：在已有**文字或图片**（化验单、检查报告照片等）基础上，提供分级诊断、事实依据、鉴别诊断，并按风险分层核验指南依据。

## 支持的文书类型（模式 A）

| 文书 | 模板 |
|---|---|
| 入院记录（四类） | references/admission-note.md |
| 首次病程记录 | references/first-progress-note.md |
| 日常病程记录、上级查房、交接班、抢救、会诊 | references/progress-note.md |
| 出院记录 | references/discharge-summary.md |
| 转科记录、死亡记录、死亡讨论 | references/transfer-and-death.md |
| 书写规范（河北细则 + 协和逻辑） | references/rules.md |
| 协和病历书写逻辑专题 | references/pumch-style.md |

## 分析模式（模式 B）

- 流程：references/case-analysis.md
- 诊断依据：references/clinical-diagnosis.md —— 区分医生已确认、支持诊断、拟诊/待排除和资料不足。
- 临床推理与治疗计划：references/clinical-reasoning-treatment.md —— 组织主要诊断、补充诊断、治疗目标、具体处理、监测与调整条件。
- 指南：references/guidelines/ —— 覆盖 10 个亚专业、80+ 病种要点（2026-08-06 二次核对扩充，优先中华医学会系列指南）。

## 使用方式

对话中直接说触发短语即可自动进入对应模式（无需前缀命令）：

| 触发短语（示例） | 模式 |
|---|---|
| 「帮我写一份入院记录」「写首次病程」「写日常病程」「写出院记录」「按河北规范写病程」「按协和标准」 | 模式 A |
| 「帮我分析这个患者」「解读这张化验单/检查报告」「诊断依据」「给出治疗方案」「诊断鉴别」「病情分析」 | 模式 B |

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

### WorkBuddy

WorkBuddy 使用与 Claude Code 相同的标准 `SKILL.md` 技能目录；本仓库无需专用运行时或额外配置。下载仓库 ZIP（解压后的顶层目录须直接包含 `SKILL.md`），然后在 WorkBuddy 的“专家·技能·连接器”中选择“上传技能”并导入该 ZIP。导入后可通过 `/medical-record-writing` 调用，或直接以“写首程”“分析病例诊断依据”等任务触发。

## 重要说明

- **指南使用**：快速文书不加载指南库；诊断、鉴别或治疗请求才按主问题读取相应亚专业摘要。具体诊断阈值、剂量、疗程、禁忌、相互作用及急危重决策须先核对权威来源。核验失败时降级为原则性建议并标注“版本待核实”（见 references/guidelines/README.md）。
- **安全边界**：模式 B 为临床决策支持，不替代主治医师判断；不虚构数据；危重征象优先警示；具体药物剂量、疗程和高风险方案须经指南/说明书核验；不面向患者使用。

## 开发说明

- 结构：`.claude-plugin/plugin.json` 与 `marketplace.json` 为 Claude 插件清单；`SKILL.md` 为主指令（双模式速览）；`references/` 为模板、规范与指南。Codex 侧无需 `.claude-plugin/`，直接以目录形式加载 `SKILL.md`。
- 版本：v1.3.1 · 作者 edwardlty25-max（MIT License）
- 卸载：删除本地安装目录即卸载（Marketplace 安装者使用 claude plugin 对应命令）。
