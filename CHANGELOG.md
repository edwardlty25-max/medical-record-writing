# 版本记录

## v1.18.0 — 以真实住院病历为参照，补全围术期与病程写作（含边界收窄）

**参照样本**：一份完整的内科住院病历（住院 7 天、行手术治疗、多学科会诊、合并酒精性肝损伤）。
**边界**：手术记录由手术医师书写，本技能**不提供手术记录模板**，也不要求记录术式、入路、器械、用量等技术细节；病程与出院记录写「详见手术记录」+ 术后观察与处置。

### 新增文书模板

- `references/progress-and-first-note-principles.md`：**一页版原则与模板**（五条总原则、病程 9 项数据、首程五部分、术前小结、术后病程、上级查房、四类情形句式、常见错 10 条）——只给能直接用的东西，行政性要求剥离到 `rules.md`。

### 病程与查房

- `references/progress-note.md`：书写要点扩至 9 条（含诊断变更、拒绝留痕、围术期必记）；新增第七节**术前小结/术前病程记录**（指征+准备+风险+同意四要素）、第八节**术后首次病程与连续记录**（术后六要素、围术期用药观察）、第九节**修正/补充诊断五要素**、第十节**患者拒绝六要素**、第十一节**多科会诊就地归位**（含自然写法 vs 台账式对照）；日常病程补 9 项数据清单与自然句式库；上级查房改为"依据→判断→决策→落实"四段结构。
- `references/first-progress-note.md`：新增"病例特点写证据链""有手术者写术前计划""合并症进诊断与计划"；新增**有手术/介入时的首程写法**（术前计划专条 + 三不要）与**诊断链**（首程→病程→出院诊断）；常见缺陷扩至 12 项。

### 出院记录

- `references/discharge-summary.md`：新增第三节**有手术时检查与关键节点写在哪**（位置对照表 + 三段式骨架 + 四条硬规则）、第四节**会诊写在哪**（就地归位、三件套、反面写法）、第五节**围手术期整合**（五要素）、第六节**出院带药核对**；7 步链与模板骨架同步更新。
- `references/discharge-checklist.md`：新增"检查与关键节点写在哪""会诊归位速查"两节；常见缺陷扩至 24 项。

### 其他模板

- `references/rules.md`：补充手术记录、术后首次病程、术前讨论的时限行；知情同意整节展开（签署意见、法定代理人、未签意见即手术）；新增围手术期记录要点一节；常见错误清单扩至 19 项。
- `assets/intake-form.md`：新增"术前讨论/手术介入记录""围术期病程要点"两节与出院带药核对。
- `assets/quick-card.md`：常见现场 5 项、常见坑 5 个。
- `references/pumch-style.md`、`SKILL.md`、`README.md`：路由表、红线表（新增手术记录必备要素、术后病程连续性两条）、示例索引同步。

### 新增示例（全部虚构数据）

`procedure-example.md`（PCI 手术记录）、`postop-progress-example.md`（术后首次病程）、`discharge-with-procedure-example.md`（有手术的出院记录）、`first-progress-with-plan-example.md`（有手术计划的首程）、`preop-summary-and-rounds-example.md`（术前小结 + 主任查房）。

### 自检脚本

- 新增文书类型 `procedure`、`preop-discussion`。
- 新增 26 条规则码：`procedure_name_missing`、`procedure_approach_missing`、`procedure_findings_missing`、`timi_missing`、`complication_unstated`、`procedure_time_missing`、`untreated_lesion_unstated`、`consent_opinion_missing`、`preop_indication_missing`、`preop_alternative_missing`、`preop_risk_missing`、`postop_progress_missing`、`postop_exam_missing`、`postop_recheck_missing`、`perioperative_no_outcome`、`exam_location_missing`、`preop_exam_location_missing`、`exam_in_discharge_status`、`diagnosis_revision_no_basis`、`diagnosis_revision_no_time`、`refusal_unstated`、`consult_no_adoption`、`med_reconciliation_risk`、`preop_summary_incomplete`、`rounds_no_analysis`、`rounds_no_decision`、`rounds_no_followthrough`。
- 修正原有误报：PTCA 全称、手术记录不再要求 T/P/R/BP、会诊采纳的自然表述（"结合会诊意见加用""患者拒绝"）不再误判。

### 质量修复

- 4 份输出字段清单（admission-note、discharge-checklist、first-progress-note、procedure-record）原为 `a: ""; b: ""` 紧凑写法、无法被 YAML 解析，已改为规范缩进并可被脚本读取。
- 修正上一轮补丁引入的 `check_required_elements` 函数误覆盖与一段孤立代码。

### 验收

- 8 份示例文档机检 0 ERROR（仅剩 `--admit` 未传时的时限 INFO 与刻意的【待医生确认】提示）。
- 正反样例逐条验证：写全不报、写错必报。
- 全部 markdown 链接 0 断链；YAML 字段清单 4/4 解析通过。

### 边界收窄：不写手术记录（本次一并落地）

- 删除 `procedure-record.md`、`procedure-checklist.md`、`procedure-example.md`：手术记录由手术医师书写，不属本技能范围。
- 删除示例 `first-progress-with-plan-example.md`、`preop-summary-and-rounds-example.md`（含介入术式细节），改为一般化表述。
- 全部模板、清单、示例去掉术式、入路、鞘管、造影所见、血流分级、支架规格、造影剂与肝素用量等技术细节；出院记录改为「一句术式 + 详见手术记录 + 并发症结论 + 遗留问题与计划」。
- 术后病程与术前小结保留属于我们的部分：症状、生命体征、切口或引流等局部情况、复查结果、用药与观察、评估与计划。
- 自检脚本删除 `procedure`、`preop-discussion` 两类文书与相关规则，泛化围术期标记与检查标记；修正"术后所写病程"的误判。
- `assets/intake-form.md` 删除"术前讨论/手术与介入记录"一节（手术记录不归我们）。
