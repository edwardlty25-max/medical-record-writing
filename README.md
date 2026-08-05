# medical-record-writing — 内科病历书写与病情分析助手

> **⚠ 免责声明**：本工具为**执业医师**的文书书写与临床决策支持辅助，输出不构成医学建议，不替代主治医师的独立判断；**不得用于患者自我诊疗**。用药须核对禁忌、过敏史、肝肾功能与药物相互作用；指南摘要基于公开资料，请以最新指南原文为准。

本地 Claude Code / Codex 插件（Codex 侧以 `~/.codex/skills` 目录加载），面向执业医师，提供**双模式**：

- **模式 A · 病历书写**：把口述、草稿笔记、检查结果整理成标准病历文书。规范基准为**《河北省病历书写规范细则（2013年版）》（冀卫办医政〔2013〕30号）**为主体、**2023 修订要点**为补充，书写逻辑参考**协和优秀病历标准**。
- **模式 B · 病情分析与治疗方案指导**：在已有**文字或图片**（化验单、检查报告照片等）基础上，分析病情、鉴别诊断、给出**符合最新内科指南**的治疗方案建议。

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
- 指南：references/guidelines/ —— 覆盖 10 个亚专业、80+ 病种要点（2026-08-06 二次核对扩充，优先中华医学会系列指南）。

## 使用方式

对话中直接说触发短语即可自动进入对应模式（无需前缀命令）：

| 触发短语（示例） | 模式 |
|---|---|
| 「帮我写一份入院记录」「写首次病程」「写日常病程」「写出院记录」「按河北规范写病程」「按协和标准」 | 模式 A |
| 「帮我分析这个患者」「解读这张化验单/检查报告」「给出治疗方案」「诊断鉴别」「病情分析」 | 模式 B |

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

- **指南使用**：捆绑摘要为基础，采用"先输出、后核对、按需深挖"策略——常见病用捆绑摘要直接作答，版本做轻量核对，高危/未覆盖病种才联网深挖，检索失败以"版本待核实"标注兜底（见 references/guidelines/README.md）。捆绑摘要已按 2026-08-06 二次核对扩充。
- **安全边界**：模式 B 为临床决策支持，不替代主治医师判断；不虚构数据；危重征象优先警示；不面向患者使用。

## 开发说明

- 结构：`.claude-plugin/plugin.json` 与 `marketplace.json` 为 Claude 插件清单；`SKILL.md` 为主指令（双模式速览）；`references/` 为模板、规范与指南。Codex 侧无需 `.claude-plugin/`，直接以目录形式加载 `SKILL.md`。
- 版本：v1.0.0 · 作者 edwardlty25-max（MIT License）
- 卸载：删除本地安装目录即卸载（Marketplace 安装者使用 claude plugin 对应命令）。
