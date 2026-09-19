# 出院记录：复核清单（易漏要素 · 常见缺陷 · 输出字段）

> 本页是 [discharge-summary.md](discharge-summary.md) 的**复核附件**：主文件讲“怎么写”，本页讲“哪里容易漏、机器能查什么、字段怎么抽”。写完主文件的成文形态后打开本页逐项核对。

## 一、易漏要素（逐项确认）

| 要素 | 写在哪 | 必须写清 | 机检 |
|---|---|---|---|
| **过敏史** | 入院情况 | 药物、食物过敏史；无则写“无” | `allergy_history_missing` |
| **输血** | 诊疗经过 | 血制品品种、数量、输注时间、**有无输血反应**、知情同意 | `transfusion_reaction_unstated` |
| **上级医师意见** | 诊疗经过 | 关键决策（诊断变更、升级治疗、停药）的上级意见与采纳情况 | 人工 |
| **特殊情况** | 诊疗经过 | 抢救、转入 ICU、转科、非医嘱出院、转院、死亡衔接（无则写“无”） | 人工 |
| **关键阴性结果** | 出院前评估 | 支撑“病情好转、准予出院”的核酸/抗原/培养/影像阴性结果 | 人工 |
| **未解决问题出口** | 出院医嘱—复诊安排 | 患者拒绝或待查项目：建议做什么、何时复查、何情况须就诊 | `no_unsolved_closure` |
| **围术期五要素** | 诊疗经过 | 术前（指征/准备/风险/同意）→ 术中（术式 + 一句经过 + 详见手术记录）→ 术后当日 → 遗留问题与计划 → 出院前评估 | `perioperative_no_outcome` |
| **出院前切口/局部** | 出院前评估 | 有手术者：切口或局部愈合情况、引流情况、相关部位功能状态 | `perioperative_no_outcome` |
| **出院带药核对** | 出院医嘱—药物治疗 | 药名、剂量、频次与病程记录、医嘱单**逐条一致**；新增/停用写理由与时间 | `med_reconciliation_risk` |
| **术中遗留问题出口** | 诊疗经过 + 复诊安排 | 未能一并处理者：原因 + 后续计划与复查时间 | `untreated_lesion_unstated` |

## 二、检查与关键节点写在哪（有手术/介入时必查）

| 内容 | 应写在哪 | 判错信号 |
|---|---|---|
| 入院前检查（外院/门诊） | 入院情况**段末** | 混进诊疗经过；院外项目缺机构/检查号/日期 |
| 术前检查（支持指征与术前准备） | 诊疗经过**第 1 段** 或 入院情况 | 只写"具备手术指征"而无检查依据 |
| 术中关键所见 | 诊疗经过**第 2 段**（手术段） | 写进辅助检查栏；漏血流分级或并发症 |
| 术后 24～72 小时复查 | 诊疗经过**第 3 段**（术后段） | 与术前检查混写；缺与本次手术相关的关键复查 |
| 住院期间新发现（补充诊断） | 诊疗经过独立成段 | 只在出院诊断首次出现 |
| 出院前复查 | 诊疗经过末段或出院前评估 | 缺关键阴性结果；异常无随访出口 |
| 未完成/拒查项目 | 出院医嘱—复诊安排 | 有待查项目但无时间与目的 |
| **会诊**（见下表） | **就地归位**（写进它影响的那一步），不另起清单段 | 照搬会诊单；只写"已请××科会诊"；无采纳情况；清单式罗列（"住院期间多学科会诊及落实情况：××；××"） |

**会诊归位速查**（会诊不单独成段，按发生的时间点写进对应段落）

| 会诊时间点 | 写在 | 示例科室 |
|---|---|---|
| 术前（评估指征/手术耐受） | 诊疗经过第 1 段（术前评估） | 心外科、麻醉科、呼吸科、肾内科 |
| 术后早期（并发症/合并症） | 诊疗经过第 3 段（术后评估） | 中医科、康复科、感染科、营养科 |
| 住院后期新问题 | 诊疗经过独立成段 | 肝病科、血液科、皮肤科 |
| 出院前 | 诊疗经过末段（出院前评估） | 任何科室 |
| 多条会诊 | 首选各按时间点分写进对应段；确有无处安放者，才在诊疗经过末尾一句话带过 | — |

**每条会诊三件套**：`科室 + 会诊时间 + 意见要点 + 本科采纳情况（执行/未执行 + 理由 + 替代方案）`。

> 机检：`exam_location_missing`（有手术却全篇无检查）、`preop_exam_location_missing`（入院情况与诊疗经过前段均无术前检查）、`exam_in_discharge_status`（检查结果写进了"出院情况"段——该段只写症状/体征/功能状态）。
> 完整范例：examples/discharge-with-procedure-example.md。

## 三、常见缺陷（真实病历高频出现）

| # | 缺陷 | 正确做法 | 机检 |
|---|---|---|---|
| 1 | 诊疗经过一整段、检验值堆砌，读完不知道结论 | 按诊断线/时间线/问题线分段，每段有结论 | 人工 |
| 2 | 检验值只写数字，无单位、无参考范围 | 结果 + 单位 + 参考范围；多次检测写趋势 | 部分 |
| 3 | 会诊意见照录，含“贵科”“我科” | 转写为本科叙述：科室 + 意见 + 采纳情况 | `consult_note_copied` |
| 4 | 部位/侧别前后不一致 | 通篇核对；确有冲突时并列呈现并注明 | 人工 |
| 5 | 出院诊断与入院诊断、补充诊断不对应 | 逐条溯源：何时、因何确认 | 人工 |
| 6 | 患者拒绝或待查项目没有出口 | 写入复诊安排与注意事项 | `no_unsolved_closure` |
| 7 | 出院情况漏生命体征 | 至少写 T/P/R/BP | 人工 |
| 8 | 药物只写商品名或漏剂量/疗程 | 通用名 + 剂量 + 频次 + 疗程 + 监测 | 部分 |
| 9 | 时间写法混用（“上午 8 点”“8 时”） | 统一 24 小时制并尽量到分；采样时点写“（8:00）” | `time_12h`、`time_minute` |
| 10 | 自动出院无患者/家属意见记录 | 写明“患者/家属要求出院并签字” | 人工 |
| 11 | 缺必备段落（如漏“出院情况”） | 六大段齐全 | `discharge_sections_missing` |
| 12 | 骨架标签【】被粘进正文 | 只输出成文形态 | `skeleton_label_leak` |
| 13 | **同一药在两处写法不同**（如他汀在一处写阿托伐他汀、另一处写普伐他汀） | 以医嘱执行记录为准，通篇统一；原始材料冲突时并列呈现并请医生确认 | `med_reconciliation_risk` |
| 14 | **同一药出现两个剂量**（如 20 mg 与 50 mg） | 同上；不得自行取舍 | `med_reconciliation_risk` |
| 15 | 有介入/手术却无术前、术中、术后三段叙述 | 按围术期五要素写全，与手术记录、病程记录一致 | 人工 |
| 16 | 出院前未写切口或局部愈合情况 | 写出院前评估时一并写清 | `perioperative_no_outcome` |
| 17 | 患者拒绝的进一步检查（如肝病科建议的超声/肿瘤标志物）未在复诊安排留出口 | 写入复诊安排：建议项目、时间、何情况须就诊 | `no_unsolved_closure` |
| 18 | **术前检查与术后复查混在一句**（如"复查心电图、心肌三项、术前超声"） | 术前归第 1 段、术后归第 3 段，按"术前 X → 术后 Y"对照写 | 人工 |
| 19 | **检查结果写进出院情况段** | 出院情况只写症状、生命体征、查体、功能状态、待办检查 | `exam_in_discharge_status` |
| 20 | 有手术却全篇没有检查结果（只有"手术顺利"） | 至少写术前指征依据与术后复查结论 | `exam_location_missing` |
| 21 | **会诊只写"已请××科会诊，详见会诊单"** | 出院记录须自行写清科室 + 时间 + 意见 + 采纳情况 | `consult_no_adoption` |
| 22 | **会诊建议未采纳/患者拒绝，但出院医嘱无出口** | 写清理由、替代方案、已告知内容，并在复诊安排给出时间与项目 | `no_unsolved_closure` |
| 23 | 会诊内容与出现阶段不符（术前会诊写到出院前评估里） | 按时间点归位：术前会诊→术前段、术后会诊→术后段、出院前会诊→末段 | 人工 |
| 24 | **会诊写成清单台账**（"住院期间多学科会诊及落实情况：××科……；××科……"） | 改写为诊疗叙述的一部分："因胸痛，结合中医科会诊意见（考虑胸痹）加用××" | 人工 |

## 四、输出字段清单（供结构化 / 对接 HIS）

```yaml
kind: discharge
discharge_time: ""
discharge_date: ""
patient: {name: "", sex: "", age: "", inpatient_no: ""}
admission_status: {chief_complaint: "", present_illness: "", past_history: "", allergy: "", exam: "", aux_exams: []}
admission_diagnosis: []
course:
  diagnostic_basis: ""
  senior_opinion: ""
  inpatient_exams: [{date: "", item: "", result: "", unit: "", ref: ""}]
  diagnosis_evolution: [{type: "supplement|correction", name: "", basis: "", found_at: "", impact: ""}]
  problems: [{problem: "", basis: "", treatment: "", response: "", monitoring: "", refusal: ""}]
  transfusion: {product: "", amount: "", time: "", reaction: "", consent: ""}
  special_events: ""        # 抢救/ICU/转科/非医嘱出院/转院/死亡衔接；无则“无”
  consultations: [{department: "", opinion: "", adopted: ""}]
  summary: ""
  outcome: ""
discharge_diagnosis: []
discharge_status: {symptoms: "", vitals: {}, exam: "", function: "", diet_sleep: ""}
discharge_orders:
  medications: [{group: "", generic: "", dose: "", frequency: "", route: "", course: "", stop_when: "", monitor: ""}]
  follow_up: ""
  precautions: ""
perioperative:                       # 有手术/介入时填写
  done: false
  indication: ""
  consent_opinion: ""
  procedures: [{date: "", name: "", approach: "", findings: "", devices: "", untreated_lesions: "", reason: ""}]
  postop_day1: ""                    # 术后当日要点
  discharge_wound: ""                # 出院前切口或局部愈合情况
  discharge_review: ""               # 出院前复查（心肌损伤标志物/肾功能/电解质等）
  follow_up_plan: ""                 # 分期手术或未处理病变的随访计划
med_reconciliation:
  checked: false
  conflicts: []                      # 原始材料中的不一致项（药名/剂量/频次），须医生确认
signature: {physician: "", date: ""}
```
