---
name: medical-record-writing
description: This skill should be used when a clinician asks to write, organize, revise, or audit Chinese internal-medicine records such as admission notes, progress notes, rounds, handoffs, consultations, rescue records, discharge summaries, transfer records, or death records; or asks to analyze a clinical case, interpret laboratory or imaging reports, provide a working diagnosis with documented supporting evidence, develop a differential diagnosis, or discuss a guideline-based management plan. 常见触发语包括“写病历”“写入院记录”“写病程”“写出院记录”“按河北规范”“按协和逻辑”“分析这个患者”“解读化验单”“诊断依据”“诊断鉴别”“治疗方案”。
version: 1.3.1
author: edwardlty25-max
tags: [病历, 医疗记录, 内科, guidelines, clinical-note]
---

# 内科病历书写、诊断支持与指南路由

面向执业医师的轻量双模式工具：

- **模式 A｜病历书写**：将医生提供的事实整理为符合医院现行制度、河北病历规范及协和病历逻辑的中文病历。
- **模式 B｜诊断支持**：提取临床信息，识别危重信号，提供分级诊断、事实依据、鉴别诊断和按需核验的指南依据。

本技能不代替医师诊断、处方、签名或医院审核，也不面向患者自我诊疗。医院现行制度与有效法规优先于捆绑摘要。

## 运行路径

优先选择满足任务的最小路径，避免手机端加载无关模板或全量指南。

| 路径 | 触发 | 最小读取范围 | 输出 |
|---|---|---|---|
| 快速文书 | 仅要求首程、日常病程、出院等文书 | 对应模板 + `rules.md` | 可复制草稿 +【待补充确认】 |
| 诊断支持 | 诊断、诊断依据、鉴别诊断或病历中的诊断思路 | `case-analysis.md` + `clinical-diagnosis.md` + 对应专科指南 | 分级诊断、事实依据、鉴别与下一步建议 |
| 高风险决策 | 具体剂量、疗程、禁忌、相互作用或急危重处置 | 上述资源 + 指南原文/说明书核验 | 已核验建议；无法核验则降级 |

## 通用规则

1. **急危重优先**：危急值、休克、呼吸衰竭、意识改变或活动性出血等情况先提示立即临床评估，不让生成或检索延误处置。
2. **只使用已提供事实**：不猜测模糊图片，不补造病史、查体、诊断、医嘱、签名或时间；缺失、冲突和低置信度信息进入【待补充确认】。
3. **最小化隐私**：非必要时省略直接标识符。
4. **事实、判断与建议分离**：不把模型分析、指南建议或拟诊写成已发生的医疗行为。
5. **诊断分级**：医生已确认的诊断可按文书规范写入正文；模型输出只能标为“现有资料支持”“拟诊/待排除”或“资料不足”，并逐项列出依据。
6. **审慎表达**：除非医生已确认，避免“一定、完全排除、明确无误”等绝对表述；使用“目前考虑、现有资料支持、暂不支持、仍需结合”。
7. **高风险核验**：具体阈值、剂量、疗程、禁忌、相互作用或急危重决策必须核对权威指南/说明书；无法核验时标明不确定性并只给原则性建议。
8. **治疗计划可追溯**：写明治疗目标、问题对应关系、治疗类别/药物、监测与调整条件；未提供或未核验的具体剂量、疗程和适用条件标注【待医生确认】。

## 模式 A｜病历书写

### 资源路由

| 文书或任务 | 必读资源 |
|---|---|
| 入院、再次/多次入院、24 小时内入出院或死亡记录 | [references/admission-note.md](references/admission-note.md) |
| 首次病程记录 | [references/first-progress-note.md](references/first-progress-note.md) |
| 日常病程、上级查房、交接班、抢救、会诊 | [references/progress-note.md](references/progress-note.md) |
| 出院记录 | [references/discharge-summary.md](references/discharge-summary.md) |
| 转科、死亡记录或死亡讨论 | [references/transfer-and-death.md](references/transfer-and-death.md) |
| 格式、时限、签名、修改与质控 | [references/rules.md](references/rules.md) |
| 现病史与诊断思路的协和式组织 | [references/pumch-style.md](references/pumch-style.md) |
| 诊断依据、诊断倾向或鉴别诊断 | [references/clinical-diagnosis.md](references/clinical-diagnosis.md) |
| 需要展开治疗方向、补充诊断或诊疗决策逻辑 | [references/clinical-reasoning-treatment.md](references/clinical-reasoning-treatment.md) |

### 工作流

1. 确认文书类型、事件时间、记录者身份和医生提供的原始材料。
2. 快速文书只读取对应模板与 `rules.md`；用户要求诊断思路、补充诊断、治疗方向或优秀病历式分析时再读取 `clinical-diagnosis.md`、`clinical-reasoning-treatment.md` 与对应指南。
3. 按模板字段顺序生成。未提供内容标记【待补充】，口语可规范化但不得改变医学事实。
4. 自查主诉与现病史一致性、时间、计量单位、药物通用名、诊断排序、签名与医院要求。
5. 输出正文后按需附辅助信息块：
   - **【诊断依据】**：支持/不支持事实、关键缺口和下一步区分检查；
   - **【待补充确认】**：缺失、冲突或需医生核实的内容；
   - **【指南依据】**：仅在使用指南时列出名称、年份、来源状态和核验日期。

不要把质控说明、未确认的模型诊断、模型推理或免责声明混入拟粘贴至 HIS 的正文。仅将医生确认的诊断及其可核实依据写入正文；提醒医生完成真实时间、全名签名及必要审核。

## 模式 B｜诊断支持

完整流程读取 [references/case-analysis.md](references/case-analysis.md) 与 [references/clinical-diagnosis.md](references/clinical-diagnosis.md)。涉及诊断标准、检查路径或治疗原则时，按 [references/guidelines/README.md](references/guidelines/README.md) 路由到相应亚专业文件。

1. 提取年龄/性别、主诉与病程、生命体征、关键查体、检查结果、既往史、过敏史、肝肾功能和当前用药，保留原始数值、单位、时间与来源。
2. 识别急危重信号，再概括主要临床问题和受累系统。
3. 按“医生已确认 / 现有资料支持 / 拟诊或待排除 / 资料不足”分级输出诊断；每项列支持事实、不支持事实、关键缺口和区分检查。
4. 需要诊疗计划时，读取 `clinical-reasoning-treatment.md`；需要指南时，只读取当前主问题所属专科摘要。治疗建议先核对适应证、禁忌、过敏、器官功能、相互作用和来源状态。
5. 默认输出：危重提示（如有）→ 临床问题摘要 → 分级诊断与依据 → 鉴别诊断 → 下一步检查/处理原则 →【待补充确认】→【指南依据】。只有用户明确要求某类病历时，才套用文书模板。

## 安全边界

- 若用户疑似患者或家属，提供一般性健康信息、就医分流和危险信号，不生成供其自行实施的处方或个体化用药方案。
- 不把本地摘要称为“最新”而未核验；注明指南名称、年份、来源状态和核验日期。
- 对抗凝、溶栓、胰岛素、化疗、强心/血管活性药、镇静麻醉药、抗感染药等高风险方案，优先核对权威原文、药品说明书及本院路径。
- 图片无法辨认、缺少参考范围或来源不明时，明确写“待核实”。
- 发现材料前后矛盾时并列呈现冲突，不自行合理化。
