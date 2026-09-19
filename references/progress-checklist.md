# 病程记录：复核清单（常见缺陷 · 输出字段）

> 本页是 [progress-note.md](progress-note.md) 的**复核附件**：主文件讲“怎么写”，本页讲“哪里容易漏、字段怎么抽”。

## 一、常见缺陷

| # | 缺陷 | 正确做法 |
|---|---|---|
| 1 | 频率不足（病危 <1 次/日，病重稳定 <1 次/2 日，普通稳定 <1 次/3 日） | 按规定频率记录 |
| 2 | 只写“病情平稳”“继续原治疗”，无依据与目标 | 写清事实 → 评估 → 处理 → 复评条件 |
| 3 | 会诊意见照抄（含“贵科/我科”） | 整理浓缩，转写为本院叙述 |
| 4 | 上级查房记录只复述下级汇报 | 主体写上级医师的分析与诊疗安排 |
| 5 | 新入院未连续记录 3 天；抢救未在 6 小时内补记 | 遵守时限 |
| 6 | 记录时间未到分、与体温单/医嘱不一致 | 24 小时制并精确到分 |
| 7 | **会诊意见只有结论、无采纳情况** | 写"会诊科室 + 意见 + 本科采纳/不采纳及理由"三件套 |
| 8 | **患者拒绝检查/治疗无记录** | 写建议内容 + 拒绝理由 + 已告知风险与替代方案 + 患者/家属意见（见 [progress-note.md](progress-note.md) 第九节） |
| 9 | **修正/补充诊断被"顺带抛出"** | 五要素齐全：诊断名称 + 依据（具体检查与数值）+ 时间 + 对治疗的影响 + 书写者资质与签名 |
| 10 | 术后病程缺失或只有一句"手术顺利、继续原治疗" | 术后当日写首次病程；术后 1、2、3 天连续记录，且含 6 要素 |
| 11 | 术后未写切口或引流等局部情况、不写并发症相关观察 | 逐项写渗血、渗液、红肿、疼痛、末梢循环与感觉（与术前对比） |
| 13 | 抗凝/抗血小板治疗期间未写出血观察 | 记录皮肤黏膜、牙龈、黑便、血尿、头晕头痛及切口渗血 |
| 14 | 一页内混用多科会诊意见却不区分采纳与否 | 逐条写采纳情况（执行 / 暂不执行 + 原因 / 患者拒绝） |
| 15 | 检验值只写数字、无单位与参考范围 | 结果 + 单位 + 参考范围；多次检测写趋势 |
| 16 | **术前无小结/术前病程记录** | 术前完成术前小结，含指征 + 准备 + 风险 + 同意四件事（见 [progress-note.md](progress-note.md) 第七节） |
| 17 | 术前小结只写"拟行手术"、无指征依据或替代方案 | 写指征依据、术前检查结果、抗凝/抗血小板安排、替代方案与同意情况 |
| 18 | **上级查房记录只复述病情与"继续观察"** | 按"依据 → 判断 → 决策"写，且每次查房要有增量（新检查/新调整/新计划） |
| 19 | 上级查房提出的调整在后续病程中无落实记录 | 当日或次日写"已按查房意见执行××"，形成闭环 |
| 20 | 首程写了"必要时手术"等空泛术前计划 | 写指征、术前检查、抗凝安排、同意安排、替代方案 |
| 21 | 病例特点罗列事实但不成证据链（症状/危险因素/查体/检查各说各的） | 四类事实指向同一结论，关键数值带来源 |
| 22 | 有鉴别意义的阴性结果缺失 | 在病例特点与鉴别诊断中写明关键阴性结果与区分检查 |
| 23 | 合并症只在病例特点出现，诊断与计划中没有 | 合并症同时进入初步诊断与诊疗计划（监测目标、用药注意） |

## 二、输出字段清单（供结构化 / 对接 HIS）

```yaml
kind: progress   # progress | rounds-critical | rounds-attending | rounds-director | handover | rescue | consultation | post-op-progress
record_time: ""
preop_summary: {written: false, indication: "", preparation: "", risk: "", consent_opinion: "", alternatives: ""}   # 术前小结/术前病程专用
post_op: {day: "", procedure_name: "", procedure_date: "", anesthesia: ""}   # 术后病程专用
rounds: {attending: "", analysis: "", decision: "", assignment: "", implemented: false}   # 上级查房：依据-判断-决策-落实
general_condition: ""
treatment: [{generic: "", dose: "", route: "", frequency: "", change_reason: ""}]
exam: ""
post_op_exam: {site: "", drainage: "", local: "", other: ""}   # 切口或引流 + 局部情况（渗血、红肿、末梢循环）
aux_exams: [{date: "", item: "", result: "", unit: "", ref: ""}]
consultations: [{department: "", time: "", opinion: "", adopted: "", reason_if_not: ""}]
diagnosis_change: [{type: "correction|supplement", name: "", basis: "", date: "", impact: "", writer: ""}]
refusal: {content: "", reason: "", risks_informed: "", alternatives: "", patient_opinion: "", signed: false}
assessment: ""    # 分析判断：好转/加重/平稳、诊断是否调整、治疗反应
plan: ""          # 下一步检查与治疗：目标、监测指标、调整/升级条件
communication: ""
signature: ""
```
