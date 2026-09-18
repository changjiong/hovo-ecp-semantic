# domain-model 0.7.0 与 A01 完整模型执行清单

本轮依据用户批准的优化方案实施；固定知识2.1.0，覆盖41问题、59规则、86案例、15开放事项。业务批准仍独立，不因技能或脚本通过自动确认。

| 任务 | 状态 | 完成证据 |
| --- | --- | --- |
| T01 当前状态、范围、知识摘要与回滚备份 | COMPLETE | 本清单、下列固定摘要、/tmp/domain-model-070-before.zip |
| T02 业务语言、对象划分、具体实例与身份规则 | IN_PROGRESS | 已生成22个业务类型，含名称来源、业务句子、正反例与身份说明；独立语义审查中 |
| T03 全量规则要素和问题案例建模 | COMPLETE | 根目录model.yaml已生成：59规则七要素、41问题、86案例解释、15OPEN；案例执行状态另行记录 |
| T04 DSL模型连接、表达能力及人工判断边界 | COMPLETE | DSL2/合同5、62计算规则、13人工裁定、12约束、9流程已落盘；结构检查和关键运行边界通过 |
| T05 业务语言审阅稿与审计台账生成 | COMPLETE | A01业务稿、审计表、output.json由同一DSL生成；业务确认仍独立待审 |
| T06 41题、59规则、86案例及反例验证 | IN_PROGRESS | [verification-report.md](verification-report.md)记录关键边界，[independent-audit.json](independent-audit.json)重放72项既有CLI检查；86业务案例尚未逐案执行，语义审查中 |
| T07 qiaomu评估、版本交付、最终逐项审计 | IN_PROGRESS | qiaomu trigger 11/11；output-eval 为 PARTIAL；独立审计72/72；业务确认与完整案例回放仍待完成 |

命名选择若改变业务含义，登记可讨论的模型决策；常规措辞和结构问题直接修订。已答业务口径保留来源；未决业务事项保留责任与影响范围。

## 固定知识

- artifact_id: A01.DomainKnowledge
- content_version: 2.1.0
- sha256: 0962cfa90d0c2ee6ca60d02cefc3c4e06229368b3537e12f8b2fb701c7c9f0d9

## 2026-09-16 实施记录

- 技能0.7.0开发候选已写入，入口、业务方法、评审回路、验收、DSL2/合同5与接口版本已同步。
- 表达式已增加集合、查询、聚合、日期、条件分支和身份去重；仅语法检查及结构检查完成，实际行为验证待独立执行。
- 业务/审计视图分开生成；合成订单已从DSL2实际生成。业务名称贴切性仍需语义审查。
- 全量业务蓝图：`/tmp/a01-model-070-business.json` 与 `.md`。这是内部建模依据整理，不是已完成的最终DSL。
- 实际静态报告：技能`reports/validation.json`。旧0.6.0证据已归档，不沿用为0.7.0通过。
- 已完成关键边界行为验证：阈值、未知传播、国企风险门控、年月差异、实际更正闭环、查询额度、附件反馈、约束、路径循环和状态迁移；详见`verification-report.md`。
- 独立审计代理提供的 72 项既有命令与断言已在当前模型上重放并全部通过；原始审计运行中的旧摘要失配已单独标注，不计作当前失败。
- 86/86 案例静态语义审查通过（输入、expected、forbidden、模型引用和步骤解释）；86/86 仍是 `NOT_EXECUTED`，因此不把静态审查称为案例运行通过。
- 剩余：全量语义审查、86案例逐案执行、输出质量评估及最终审计。业务确认保持PENDING。

- A01当前已编写22个具体业务类型和时间字段，保存在内部集成文件`/tmp/a01-model-070-foundation-root.json`；其类型Schema、依据ID和Ref目标检查通过（`/tmp/a01-model-070-foundation-static.json`）。尚须补约束、判断、规则、流程和全量覆盖，不称完整模型。

## 最新落盘状态

模型0.3.0完整范围已生成；旧模型已归档至history/model-before-dsl2-0.2.0.zip。结构和生成合同均PASS；关键边界已有本地求值记录，但86案例目前全部NOT_EXECUTED，不能把解释覆盖称为执行通过。


## 2026-09-18 归档修复（助手执行，非独立验真）

- 目录改名后引用未同步：`model.yaml` 与 `input.json` 的知识引用指向已改名目录、摘要为旧字节；`input.json`/`output.json` 引用 `05领域模型输出/`，均已修正为 `03领域知识输出/`、`04领域模型输出/`，并更新知识 output.json 摘要为本版字节。
- 用 domain-model 0.7.0 生成器重生成审阅稿：`review.md`、`coverage.md` 逐字节未变（证明生成可复现），`output.json` 仅更新引用路径与摘要。
- 三项检查重跑 PASS：DSL 校验、输入合同、输出合同；validation.json 与 validation-final.json 按当前 model.yaml 摘要重登记（执行者记为助手，非独立验真）。行为验证与 72/72 重放证据基于修复前字节，未重新执行，已在记录中单独标注其摘要。
- 清理无引用旧文档 4 个（知识确认状态、输入评估、修订说明、技能升级说明）；历史版本 zip、dsl-preview、技能补丁此前已清理，历史保留在 Git。
- 业务评审与确认状态未变：business_confirmation 仍为 PENDING。
