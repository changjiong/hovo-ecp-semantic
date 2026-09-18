# domain-model 0.5.0升级说明

原技能入口版本0.4.0，manifest为0.3.0；本轮统一为0.5.0。模型合同升至3.0.0，接收固定的领域知识4.0.0；不迁移或兼容旧版模型合同。

## 已完成的调整

- 将知识基础DRAFT/CONFIRMED与模型评审方式IN_SESSION/DEFERRED分开，保留会话讨论和线下回收反馈回路。
- 固定上游身份、版本、字节摘要和非空问题范围；CONFIRMED要求真实外部批准，同时绑定知识output、review.md、coverage.md和答复。
- 所有开放上游问题逐项处置，并将影响传到对应模型问题；不能靠遗漏gap_ids把存在缺口的问题标为MODELED。
- 问题逐项记MODELED/PARTIAL/DEFERRED；案例逐项记EXPLAINED/BLOCKED，保留原预期和禁止结果。
- review.md服务业务阅读，coverage.md承担完整矩阵；校验文档版本与摘要。
- 删除不能代表新版状态的旧静态reports，旧字节已归档；技能继续是candidate/scaffold，不声称生产成熟或已验收。

原版已经支持DEFERRED草案。本轮修复的是过期输入合同、上游确认与本轮评审方式混绑，以及覆盖和未决事项缺少强制传递。

## 本次实际产出

05模型0.2.0：30概念、73属性、60关系、12项语义政策、24组判断流程、41问题、86案例、15项上游未决映射。模型与知识确认仍PENDING。

schema检查、实际input/output合同和skill-creator入口检查已通过。这些检查不验证业务含义、案例运行或正式批准。

## 安装清单

完整新包为[domain-model-0.5.0.zip](domain-model-0.5.0.zip)，文本差异为[skill-upgrade.patch](skill-upgrade.patch)。旧版被替换文件为[domain-model-before-0.5.0.zip](domain-model-before-0.5.0.zip)。正式技能目录位于当前A01写入边界之外；已获工具写入许可并完成安装，安装后19项变更的字节与清单一致。已使用正式目录脚本重新检查当前输入、最终模型输出与技能入口，结果PASS，见validation.json及validation-final.json。

| 动作 | 相对技能路径 |
| --- | --- |
| REPLACE | README.md |
| REPLACE | SKILL.md |
| REPLACE | agents/interface.yaml |
| REPLACE | contracts/README.md |
| REPLACE | contracts/common.schema.json |
| REPLACE | contracts/imports/README.md |
| ADD | contracts/imports/domain-knowledge-common.schema.json |
| REPLACE | contracts/imports/domain-knowledge.schema.json |
| REPLACE | contracts/input.schema.json |
| REPLACE | contracts/output.schema.json |
| REPLACE | manifest.json |
| REPLACE | references/acceptance.md |
| REPLACE | references/interactive-review.md |
| REPLACE | references/sources.json |
| REPLACE | scripts/domain_checks.py |
| REPLACE | scripts/validate_contract.py |
| REMOVE_OBSOLETE_REPORT | reports/domain-revision.md |
| REMOVE_OBSOLETE_REPORT | reports/domain-static-checks.json |
| REMOVE_OBSOLETE_REPORT | reports/standalone-checks.json |
