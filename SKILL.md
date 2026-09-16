---
name: medical-record-writing
description: 面向中国执业医师的内科病历书写加速器。当医生说“写病历”“写入院记录”“写首程”“写病程”“写查房记录”“写交班”“写出院小结”“写转科记录”“整理成病历”“这块病历帮我顺一下”“按河北规范写”，或粘贴口述、草稿、化验与检查结果要求成文时使用。默认输出可直接粘贴进 HIS 的病历正文，并自动执行规范硬红线自检（主诉≤20字、单项否决时限、计量单位、药品通用名、签名与未填占位）。病情分析、诊断依据、鉴别诊断与治疗方案属于可选旁路，仅在医生明确要求时启用。不用于患者自我诊疗。
version: 1.13.0
author: edwardlty25-max
license: MIT
metadata:
  tags: [病历, 医疗记录, 内科, clinical-note]
  scope: 中国内科住院病历；以河北规范为基础，医院现行制度优先
---

# 内科病历书写加速器

**主旨**：把医生给的零散事实（口述、草稿、粘贴的化验与检查结果）在**一次交互内**转成**可直接粘贴进 HIS 的规范病历正文**，并在出稿前跑一遍**确定性规范自检**。

本技能不代替医师诊断、处方、签名或医院审核；医院现行制度与有效法规优先于本捆绑摘要。

**急着用？** 先看 [assets/quick-card.md](assets/quick-card.md)——一屏：最小输入、输出约定、出稿后自检命令。

## 一、用与不用

- **用**：入院记录、首次病程、日常病程、上级查房、交接班、抢救、会诊、出院记录、转科与死亡记录，以及“整理成病历”“按河北规范写”“按协和逻辑写”。
- **可选旁路（需医生明确要求）**：诊断依据、鉴别诊断、治疗方案、解读化验单、分析病例。
- **不用**：疑似患者或家属 → 只给一般健康信息、就医分流与危险信号，不生成个体化诊疗方案；非内科或非中国规范 → 先说明覆盖范围。
- **急危重优先**：危急值、休克、呼吸衰竭、意识改变、活动性出血等，先提示立即临床评估，再谈成文。

## 二、快路径（默认，3 步）

1. **定文书**：医生未说明时按输入内容判定，并在回复首行写出文书类型（不进正文）。
2. **取事实**：只用医生已给内容。缺字段时按 [assets/intake-form.md](assets/intake-form.md) 追问——**最多 1 轮、最多 3 个问题**；也可不追问直接成稿，缺项标【待补充】。
3. **出稿并自检**：按模板生成 → 运行 `scripts/validate_note.py` → 在正文之外附一行自检结论（如“自检：通过 / 2 项需确认”）。

## 三、输入契约

- [assets/intake-form.md](assets/intake-form.md) 是最小字段清单，供医生粘贴口述或填空；**医生整段口述即可，无需按格式填写**。
- 图片/化验单：保留原始数值、单位、参考范围与采样时间；模糊、遮挡、缺单位 → 列入【待补充确认】，不猜。
- 材料冲突时并列呈现并请医生确认，不自行取舍。

## 四、输出契约（守住“可直接粘贴”）

1. **默认只输出一个正文代码块**，可直接粘贴进 HIS；不夹带提示语、质控说明、免责声明、模型推理或就医建议。
2. 模板括号内的提示（如“（症状+部位+持续时间，≤20字）”）**不得进入输出**；输出前逐行检查并删除所有占位符与说明性括号。
3. 辅助信息块**仅在医生索取时**输出：【诊断依据】【待补充确认】【指南依据】。
4. **事实可回溯**：正文中每个数值、体征、诊断、医嘱都必须来自输入或医生确认；无法回溯的写【待补充】。
5. 格式：日期用“年-月-日”，时间用 24 小时制并精确到分；单位用 mmHg、℃、次/分、g/L、mmol/L 等法定符号；药物用通用名；缩写首次出现写全称（括号注缩写）。

## 五、规范硬红线（出稿前必查）

优先运行 `scripts/validate_note.py`（确定性机检）；无 Python 环境时按本表与 [references/rules.md](references/rules.md) 第十二节逐条自查。

| # | 红线 | 后果 |
|---|---|---|
| 1 | 单项否决时限：首程 ≤8h、入院记录 ≤24h、危重上级查房 ≤24h、主治首次查房 ≤48h、主任/副高首次查房 ≤72h、抢救补记 ≤6h、出院/死亡 ≤24h | 整份病历不合格 |
| 2 | 主诉 ≤20 字、不用诊断或检查结果、与现病史时间一致 | 常见扣分 |
| 3 | 计量单位一律用法定符号：禁用“公分/公尺/公升/立升/公斤”，写 cm/m/L/kg | 常见扣分 |
| 4 | 药物用通用名，不用商品名 | 常见扣分 |
| 5 | 签名用全名；电子病历打印后须补手写签名 | 法律风险 |
| 6 | 修改保留原记录、每页 ≤3 处、每处 ≤20 字；禁刮粘涂描 | 法律风险 |
| 7 | 阴性体征不得写“无异常”“(-)”，须逐系统具体化 | 常见扣分 |
| 8 | 诊断分初步/修正/补充/出院，按主次排序并写在规定位置（末页中线右侧/左侧） | 常见扣分 |
| 9 | 院外检查写明机构名称、检查号、检查日期 | 常见扣分 |
| 10 | 知情同意书须签署意见（如“同意手术”），不能只签名 | 法律风险 |

## 六、文书路由（按需读取，不预加载）

| 文书或任务 | 必读资源 |
|---|---|
| 入院、再次或多次入院、24 小时内入出院或死亡记录 | [references/admission-note.md](references/admission-note.md) |
| 首次病程记录 | [references/first-progress-note.md](references/first-progress-note.md) |
| 日常病程、上级查房、交接班、抢救、会诊 | [references/progress-note.md](references/progress-note.md) |
| 病程记录复核清单（常见缺陷、输出字段） | [references/progress-checklist.md](references/progress-checklist.md) |
| 出院记录（书写逻辑 + 两形态模板） | [references/discharge-summary.md](references/discharge-summary.md) |
| 出院记录复核清单（易漏要素、常见缺陷、输出字段） | [references/discharge-checklist.md](references/discharge-checklist.md) |
| 转科、死亡记录或死亡讨论 | [references/transfer-and-death.md](references/transfer-and-death.md) |
| 格式、时限、签名、修改与质控；规范来源与核验状态 | [references/rules.md](references/rules.md) |
| 优秀病历标准与内涵质量（逐文书逻辑见对应模板） | [references/pumch-style.md](references/pumch-style.md) |
| 输入字段清单 | [assets/intake-form.md](assets/intake-form.md) |
| 成稿样式示例（虚构数据） | 日常病程 [daily-progress-example.md](references/examples/daily-progress-example.md) · 首程 [first-progress-example.md](references/examples/first-progress-example.md) · 出院 [discharge-example.md](references/examples/discharge-example.md) |

**最常用的一种写法（日常病程）**：客观输入（一般情况 / 查体 / 检查 / 会诊）原样整合 → 由本技能补足“分析判断 + 诊疗计划 + 医患沟通” → 成一段通顺文字。重病或病情变化当日必记，不得只写“病情平稳、继续原治疗”。

## 七、可选旁路：病情分析与治疗（默认关闭）

仅当医生明确要求“诊断依据 / 鉴别诊断 / 治疗方案 / 分析这个患者 / 解读化验单”时才读取：

1. [references/case-analysis.md](references/case-analysis.md) 与 [references/clinical-diagnosis.md](references/clinical-diagnosis.md)：分级诊断（医生已确认 / 现有资料支持 / 拟诊或待排除 / 资料不足）与事实依据。
2. 需要治疗方向时读 [references/clinical-reasoning-treatment.md](references/clinical-reasoning-treatment.md)。
3. 需要诊断标准或治疗原则时，按 [references/guidelines/README.md](references/guidelines/README.md) 路由到**当前主问题所属专科**文件；**不加载整库**。

**旁路输出不得进入病历正文**：模型分析、未确认诊断、指南建议、免责声明一律放在正文之外的辅助块。具体剂量、疗程、阈值、禁忌、相互作用或急危重决策必须核对权威原文或说明书；无法核验时只给原则性建议并标“版本待核实”。

## 八、安全边界

展开版见 [references/safety-boundaries.md](references/safety-boundaries.md)（允许/禁止对照表、底线话术、急危重信号阈值）。

1. **只使用已提供事实**：不补造病史、查体、诊断、医嘱、签名或时间；缺失、冲突、低置信度信息一律进【待补充确认】。
2. **诊断分级**：医生已确认的诊断可写入正文；模型输出只能标“现有资料支持”“拟诊/待排除”“资料不足”，并逐项列出依据。
3. **事实、判断与建议分离**：不把模型分析、指南建议或拟诊写成已发生的医疗行为。
4. **审慎表达**：除非医生已确认，避免“一定、完全排除、明确无误”等绝对表述。
5. **隐私**：输入前去除姓名、住院号、身份证号、联系方式等直接标识符；不要把未脱敏病历上传到云端模型。
6. **高风险药物**（抗凝、溶栓、胰岛素、化疗、强心/血管活性药、镇静麻醉药、抗感染药等）优先核对权威原文、药品说明书及本院路径。
7. **面向医务人员**：疑似患者或家属只提供一般性健康信息、就医分流和危险信号。

## 九、参考文件索引

- 写作：[references/rules.md](references/rules.md)、[references/pumch-style.md](references/pumch-style.md)、[references/progress-note.md](references/progress-note.md) 等模板文件
- 输入与示例：[assets/intake-form.md](assets/intake-form.md)、[references/examples/daily-progress-example.md](references/examples/daily-progress-example.md)
- 分析：[references/case-analysis.md](references/case-analysis.md)、[references/clinical-diagnosis.md](references/clinical-diagnosis.md)、[references/clinical-reasoning-treatment.md](references/clinical-reasoning-treatment.md)
- 指南：[references/guidelines/](references/guidelines/README.md)（10 个亚专业，核验日期见其 README）
- 工程校验：`scripts/validate_note.py`（正文自检）、`scripts/check_links.py`、`scripts/run_tests.py`；示例见 `references/examples/`
