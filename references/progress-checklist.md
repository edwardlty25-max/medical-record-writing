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

## 二、输出字段清单（供结构化 / 对接 HIS）

```yaml
kind: progress   # progress | rounds-critical | rounds-attending | rounds-director | handover | rescue | consultation
record_time: ""
general_condition: ""
treatment: [{generic: "", dose: "", route: "", frequency: "", change_reason: ""}]
exam: ""
aux_exams: [{date: "", item: "", result: "", unit: "", ref: ""}]
consultations: []
assessment: ""    # 分析判断：好转/加重/平稳、诊断是否调整、治疗反应
plan: ""          # 下一步检查与治疗：目标、监测指标、调整/升级条件
communication: ""
signature: ""
```
