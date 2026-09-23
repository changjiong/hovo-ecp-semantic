# domain-model

将固定版本的领域知识变为平台无关、机器可读的领域模型 IR（中间表示）；同一份 `model.yaml` 生成业务说明和覆盖台账。IR 用于无歧义交接业务语义，不是另一套生产运行平台。

Hovo 0.8.0 开发候选包 · 模型合同 5.0.0 · DSL 2.0.0 · 上游知识合同 4.0.0。当前在本项目 `.agents/skills/domain-model` 本地使用，未发布或验证宿主重新发现。

适用：“把已确认知识建成领域模型”“修订形成日期模型”“审查模型是否承接固定知识”。原始制度抽取交给 domain-knowledge；数据库映射、平台资产和发布不在此包范围。Question（业务问题）只做覆盖检查，模型完成以范围内 Term（业务概念）/Rule（业务规则）是否被承接或显式排除为主。

依赖 Python>=3.10、jsonschema、referencing、PyYAML。技能目录可使用 uv 虚拟环境：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/validate_contract.py --check-schemas
.venv/bin/python scripts/domain_dsl.py validate /project/domain-model/model.yaml
.venv/bin/python scripts/domain_dsl.py evaluate /project/domain-model/model.yaml --rule M.Rule --inputs /project/domain-model/facts.json
.venv/bin/python scripts/deliver_model.py /project/domain-model/model.yaml --request /project/domain-model/input.json --output-dir /project/domain-model --project-root /project
.venv/bin/python scripts/validate_contract.py validate output /project/domain-model/output.json --project-root /project
```

先按[入口](SKILL.md)和[语言规范](references/domain-dsl.md)编写模型；生成器不会把原知识自动转成正确 DSL。模型阶段不重新读取原始法规、MinerU（文档解析工具）结果或数据库字段来改变上游业务含义。业务审阅稿首先生成领域模型总览，按业务层次展示对象分类、关键引用关系和主要过程，再展开具体对象与规则。输出 model.yaml、review.md、coverage.md、output.json，校验记录独立保存。修订前归档旧版完整模型、请求、交接及评审字节到当前阶段的 `archive/`，中间记录放 `process/`，不建立并列模型入口。

示例见 examples：纯合成的订单领域语法示例可以独立检查和求值，不带真实业务确认；A01 实例另在业务项目的 `04领域模型输出`（完整新版生成状态以该目录README为准），不把业务知识复制进通用技能包。

排障：缺 Python 依赖先安装 requirements；UNKNOWN 查输入和证据；BLOCKED 查 guard 与缺口；本地 evaluate 只用于有限验证，不要求以它执行全部业务；GENERATED_DOCUMENT_DRIFT 从 DSL 重新生成；摘要不符定位被修改的引用文件，不覆盖历史确认。复杂计算先说明业务输入、输出、数学/业务语义、未知处理与适用前提；不要为了本地求值继续加入领域专用算法。语言不支持的能力登记 MODEL_GAP；仅业务固有人工裁定进入 BUSINESS_DISCRETION，业务未决口径进入 UNRESOLVED_POLICY。

本版不兼容旧DSL1和模型合同4及更早版本，未自动迁移旧成果。有限静态检查和示例求值不证明知识正确、全问题已完成、人工确认或 ECP 可执行。[本次工程交付、参考技能和缺失证据](reports/creation-handoff.md)。


0.8.0 进一步收敛：以已确认领域知识为模型完整性的主轴，Question（业务问题）降为覆盖检查；Case（案例）沿用上游真值做解释与验证，不在模型阶段重新定义；Domain DSL（领域模型专用语言）停止以“可执行全部业务”为演进目标。现有有限求值能力保留用于静态/样例验证，但不再作为新增平台算法或领域专用执行机制的理由。
