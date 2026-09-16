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

## 二、常见缺陷（真实病历高频出现）

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

## 三、输出字段清单（供结构化 / 对接 HIS）

```yaml
kind: discharge
discharge_time: ""; admission_date: ""; discharge_date: ""
patient: {name: "", sex: "", age: "", inpatient_no: ""}
admission_status: {chief_complaint: "", present_illness: "", past_history: "", allergy: "", exam: "", aux_exams: []}
admission_diagnosis: []
course:
  diagnostic_basis: ""; senior_opinion: ""
  inpatient_exams: [{date: "", item: "", result: "", unit: "", ref: ""}]
  diagnosis_evolution: [{type: "supplement|correction", name: "", basis: "", found_at: "", impact: ""}]
  problems: [{problem: "", basis: "", treatment: "", response: "", monitoring: "", refusal: ""}]
  transfusion: {product: "", amount: "", time: "", reaction: "", consent: ""}
  special_events: ""        # 抢救/ICU/转科/非医嘱出院/转院/死亡衔接；无则“无”
  consultations: [{department: "", opinion: "", adopted: ""}]
  summary: ""; pre_discharge_review: ""; outcome: ""
discharge_diagnosis: []
discharge_status: {symptoms: "", vitals: {}, exam: "", function: "", diet_sleep: ""}
discharge_orders:
  medications: [{group: "", generic: "", dose: "", frequency: "", route: "", course: "", stop_when: "", monitor: ""}]
  follow_up: ""; lifestyle: ""; precautions: ""
signature: {physician: "", date: ""}
```
