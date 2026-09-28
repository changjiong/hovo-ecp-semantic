# semantic-foundry

可选的跨阶段编排技能。当前主链只有四个生产技能：

| 阶段 | 技能 | 交付 |
| --- | --- | --- |
| 1 | domain-knowledge | 领域知识 |
| 2 | domain-model | Business Domain Model |
| 3 | ecp-semantic-authoring | ECP V3 技术语义模型闭包，包含 Mapping |
| 4 | ecp-semantic-release | Revision、候选编译、Release 与运行证据 |

关键变化：ecp-data-mapping 已删除。真实 Schema 与 Mapping 仍有独立的数据负责人审查，但与 Ontology、SHACL 和规则资产共同属于 ecp-semantic-authoring 的同一个版本闭包。

跨阶段编排使用 pipeline.json；单技能独立使用不需要本技能。每个生产技能保持自己的输入合同、输出合同、验收清单和责任边界。

本地检查：

```bash
python3 scripts/validate_pipeline.py --check-schemas
python3 scripts/validate_pipeline.py stage input /path/to/project/domain-model/input.json --project-root /path/to/project --skill domain-model
```

校验器只证明有限结构条件，不证明业务批准、目标 Workspace 的 V3 编译、发布或 Run。
