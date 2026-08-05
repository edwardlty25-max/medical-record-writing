---
name: medical-record-writing
description: This skill should be used when a clinician asks to write, organize, revise, or audit Chinese internal-medicine records such as admission notes, progress notes, rounds, handoffs, consultations, rescue records, discharge summaries, transfer records, or death records; or asks to analyze a clinical case, interpret laboratory or imaging reports, develop a differential diagnosis, or discuss a guideline-based management plan. 常见触发语包括“写病历”“写入院记录”“写病程”“写出院记录”“按河北规范”“按协和逻辑”“分析这个患者”“解读化验单”“诊断鉴别”“治疗方案”。
version: 1.1.0
author: edwardlty25-max
tags: [病历, 医疗记录, 内科, guidelines, clinical-note]
---

# 内科病历书写与病情分析

面向执业医师的双模式辅助工具：

- **模式 A｜病历书写**：基于医生提供的事实，整理为符合医院现行制度、河北病历规范及协和病历逻辑的中文病历。
- **模式 B｜病情分析**：基于已有文字或图片，提取临床信息、识别危重信号、梳理鉴别诊断并提供可核验的指南依据。

本技能不代替医师诊断、处方、签名或医院审核，也不面向患者自我诊疗。医院现行制度与有效法规优先于捆绑摘要。

## 选择模式

| 用户意图 | 执行方式 |
|---|---|
| 写、整理、修改或审核病历文书 | 模式 A |
| 分析病情、解读检查、鉴别诊断或讨论治疗 | 模式 B |
| 在病历中加入病情分析 | 以模式 A 的文书结构承载模式 B 的分析 |

仅当意图、文书类型或输出用途会实质改变结果时提问；其他情况直接处理并标注待核实项。

## 通用执行规则

1. **先识别急危重信号**：若存在危急值、休克、呼吸衰竭、意识改变、活动性出血等可能危及生命的情况，先提示立即临床评估，不让文书生成或检索延误处置。
2. **只使用已提供事实**：不猜测图片模糊内容，不补造病史、查体、诊断、医嘱、签名或时间；缺失、冲突和低置信度信息进入【待补充确认】。
3. **最小化隐私**：非必要时省略姓名、身份证号、住址、社保号、联系方式等直接标识符。
4. **区分事实与建议**：患者事实、医生既有判断、模型分析和指南建议必须可辨，不把建议写成已执行医嘱。
5. **核验时效**：具体诊断阈值、药物剂量、疗程、禁忌、相互作用或急危重决策须核对当前权威指南/说明书；无法核实时标注版本与不确定性，并降级为原则性建议。

## 模式 A｜病历书写

### 资源路由

按任务读取所需文件，不一次加载全部资源：

| 文书或任务 | 必读资源 |
|---|---|
| 入院、再次/多次入院、24 小时内入出院或死亡记录 | [references/admission-note.md](references/admission-note.md) |
| 首次病程记录 | [references/first-progress-note.md](references/first-progress-note.md) |
| 日常病程、上级查房、交接班、抢救、会诊 | [references/progress-note.md](references/progress-note.md) |
| 出院记录 | [references/discharge-summary.md](references/discharge-summary.md) |
| 转科、死亡记录或死亡讨论 | [references/transfer-and-death.md](references/transfer-and-death.md) |
| 格式、时限、签名、修改与质控 | [references/rules.md](references/rules.md) |
| 现病史与诊断思路的协和式组织 | [references/pumch-style.md](references/pumch-style.md) |

### 工作流

1. 确认文书类型、事件时间、记录者身份和医生提供的原始材料。
2. 读取对应模板；涉及质控、时限或格式时同时读取 `references/rules.md`。
3. 按模板字段顺序生成。未提供内容标记【待补充】，口语可规范化但不得改变医学事实。
4. 自查主诉与现病史一致性、时间、计量单位、药物通用名、诊断排序、签名与医院要求。
5. 先给可复制的文书正文，再给辅助信息块：
   - **【待补充确认】**：缺失、冲突或需医生核实的内容；
   - **【指南依据】**：仅在正文使用指南时列出名称、年份和版本状态。

不要把质控说明、模型推理或免责声明混入拟粘贴至 HIS 的正文。提醒医生核对后完成真实时间、全名签名及必要的上级审核。

## 模式 B｜病情分析

完整流程读取 [references/case-analysis.md](references/case-analysis.md)；涉及疾病指南时，再按 [references/guidelines/README.md](references/guidelines/README.md) 路由到相应亚专业文件。

### 工作流

1. 提取年龄/性别、主诉与病程、生命体征、关键查体、检查结果、既往史、过敏史、肝肾功能和当前用药；保留原始数值、单位、时间与来源。
2. 先识别急危重信号，再概括主要临床问题和受累系统。
3. 对鉴别诊断分别列出支持证据、不支持证据、关键缺口和区分检查；不代替医师下最终诊断。
4. 治疗建议先核对适应证、禁忌、过敏、器官功能、相互作用及可靠指南来源。关键资料不足时，只给原则和需补充信息，不给看似精确的个体化剂量。
5. 默认输出结构：危重提示（如有）→ 临床问题摘要 → 鉴别诊断 → 下一步检查/处理建议 →【待补充确认】→【指南依据】。只有用户明确要求某类病历时，才套用对应文书模板。

## 安全边界

- 若用户疑似患者或家属，提供一般性健康信息、就医分流和危险信号，不生成供其自行实施的处方或个体化用药方案。
- 不把本地指南摘要称为“最新”而未核验；注明指南名称、年份、来源状态和核验日期。
- 对抗凝、溶栓、胰岛素、化疗、强心/血管活性药、镇静麻醉药、抗感染药等高风险方案，必须优先核对权威原文、药品说明书及本院路径。
- 图片仅用于辅助提取；无法辨认、缺少参考范围或来源不明时，明确写“待核实”。
- 发现材料前后矛盾时并列呈现冲突，不自行合理化。
