# domain-model

将固定版本的领域知识变为平台无关的领域 DSL；同一份 `model.yaml` 生成业务说明和覆盖台账。

Hovo 0.7.0 开发候选包 · 模型合同 5.0.0 · DSL 2.0.0 · 上游知识合同 4.0.0。当前在本项目 `.agents/skills/domain-model` 本地使用，未发布或验证宿主重新发现。

适用：“把已整理知识建成领域模型”“修订形成日期模型”“审查模型是否覆盖知识问题”。原始制度抽取交给 domain-knowledge；数据库映射、平台资产和发布不在此包范围。

依赖 Python>=3.10、jsonschema、referencing、PyYAML。技能目录可使用 uv 虚拟环境：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/validate_contract.py --check-schemas
.venv/bin/python scripts/domain_dsl.py validate /project/model.yaml
.venv/bin/python scripts/domain_dsl.py evaluate /project/model.yaml --rule M.Rule --inputs /project/facts.json
.venv/bin/python scripts/deliver_model.py /project/model.yaml --request /project/input.json --output-dir /project/output --project-root /project
.venv/bin/python scripts/validate_contract.py validate output /project/output/output.json --project-root /project
```

先按[入口](SKILL.md)和[语言规范](references/domain-dsl.md)编写模型；生成器不会把原知识自动转成正确 DSL。输出 model.yaml、review.md、coverage.md、output.json，校验记录独立保存。修订前归档旧版完整模型、请求、交接及评审字节；新版本继续使用当前输出目录，不建立并列模型入口。

示例见 examples：纯合成的订单领域语法示例可以独立检查和求值，不带真实业务确认；A01 实例另在业务项目的 `05领域模型输出`（完整新版生成状态以该目录README为准），不把业务知识复制进通用技能包。

排障：缺 Python 依赖先安装 requirements；UNKNOWN 查输入和证据；BLOCKED 查 guard 与缺口；GENERATED_DOCUMENT_DRIFT 从 DSL 重新生成；摘要不符定位被修改的引用文件，不覆盖历史确认。语言不支持的能力登记 MODEL_GAP；仅业务固有人工裁定进入 BUSINESS_DISCRETION，业务未决口径进入 UNRESOLVED_POLICY。

本版不兼容旧DSL1和模型合同4及更早版本，未自动迁移旧成果。有限静态检查和示例求值不证明知识正确、全问题已完成、人工确认或 ECP 可执行。[本次工程交付、参考技能和缺失证据](reports/creation-handoff.md)。


0.7.0新增：业务名称和实例要求、全量范围门槛、规则七要素覆盖、规则字段绑定、过程依赖、人工裁定准则，以及业务视图与审计视图分开生成。规则和案例引用齐全仍须语义回读，不能单凭数量宣称业务完成。

当前0.7.0已完成A01全量模型生成、结构合同检查和关键边界行为验证；86个案例逐案执行、独立业务语义评审、宿主安装和平台运行仍未证明。报告须绑定本版实际文件；缺失执行或人工评审证据的项目保留未执行。
