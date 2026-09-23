# 0.5.0 同步验证记录

验证时间：2026-09-20（Asia/Shanghai）。模型：`model.yaml` 0.5.0；知识：`03领域知识输出/output.json` 2.5.0；DSL：2.0.0。该记录只证明当前文件的结构和合同边界，不代表模型业务确认、平台运行或制度结论。

## 已执行

| 检查 | 结果 | 说明 |
| --- | --- | --- |
| DSL 校验 | PASS | `domain_dsl.py validate model.yaml`，无错误 |
| 输入合同 | PASS | `validate_contract.py validate input input.json` |
| 输出合同 | PASS | `validate_contract.py validate output output.json` |
| 范围一致性 | PASS | 41/41 业务问题；59/59 规则；86/86 案例解释；15个模型开放事项 |

当前模型包含22个业务类型、62条计算/判断规则、13个人工裁定、12项约束和9个流程。`review.md`、`coverage.md`和`output.json`均由当前`model.yaml`生成。

## 未执行与停止边界

- 模型确认状态仍为 `PENDING`，不能从知识侧2.5.0的确认记录继承为模型确认。
- 86个案例仍为 `NOT_EXECUTED`；历史72项重放和旧摘要属于归档的0.4.0及更早版本，未作为本轮通过证据。
- 形成日期、人工裁定、国企性质认定和开放事项仍需业务/合规人员逐项审查。
- 未进行平台编译、发布或运行；本轮只完成领域模型层的同步和合同校验。
