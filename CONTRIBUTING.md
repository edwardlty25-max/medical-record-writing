# 贡献指南

本仓库面向**中国执业医师**的内科病历书写加速。任何改动都以「不虚构、可回溯、可直接粘贴」为前提。

## 可以怎么贡献

| 类型 | 入口 |
|---|---|
| 规范条款、时限或来源有误 | [规范纠错](https://github.com/edwardlty25-max/medical-record-writing/issues/new?template=spec-correction.yml) |
| 需要新增文书模板或字段 | [模板请求](https://github.com/edwardlty25-max/medical-record-writing/issues/new?template=template-request.yml) |
| 指南版本过期 | 提 issue，写明指南名称、年份、来源链接 |

## 硬性要求

1. **不虚构来源**：涉及法规、时限、剂量、阈值的内容必须给出文件名称 + 文号/年份，并注明核验日期；无法核实的写【来源待核验】，不得凭记忆补全。
2. **不写入未确认的医学结论**：模板与示例中的诊断、用药必须标明「虚构示例」或【待医生确认】。
3. **用中文规范用语**：药物用通用名；计量单位用法定符号（cm/m/L/kg/mmHg/℃）。
4. **示例数据必须虚构**，不得使用真实病历或任何可识别信息。

## 本地自检（提交前必跑）

```bash
python scripts/check_links.py     # 链接与 frontmatter
python scripts/run_tests.py       # 校验器回归测试
```

## 修改规范类文件的流程

1. 在 `references/rules.md` 顶部「来源与核验状态」登记来源与核验日期；
2. 同步更新受影响的所有模板（同一时限可能出现在多个模板中）；
3. 新增可机检规则时，在 `scripts/validate_note.py` 实现，并在 `tests/cases/` 增加正反用例；
4. 更新 `CHANGELOG.md`。
