# ecp-data-mapping

将已定义语义与真实数据连接，明确字段背后的身份、关联、单位、时间、未知含义以及设计期数据血缘。Hovo 0.3.0，本地候选。

> 使用 ecp-data-mapping，根据这份精确版本的本体、事实需求和真实 Schema 编制 Mapping，说明关联依据、缺值策略及无法提供的事实。

见 [输入合同](contracts/input.schema.json)、[输出合同](contracts/output.schema.json)、[设计期数据血缘](references/data-lineage.md) 与 [验收清单](references/acceptance.md)。默认可依据已提供结构生成候选；访问当前数据源需要该任务授权和实际发现证据。所需 Scope 在 Mapping 稳定后编制。

## 独立安装与使用

本技能无需安装其他技能，但不再是只复制本目录即可运行的完全自包含包：除本目录合同、方法资料和 ECP Kit 1.7 外，合同校验还需要仓库级 `contracts/lineage/v1` 共享合同。部署/分发时必须同时携带该共享合同目录。输入可由人工、其他工具或其他技能提供；按 [合同说明](contracts/README.md) 整理引用、来源和必要确认。完成本技能交付后结束，不自动启动下游。

Python 3.10+ 的本地检查依赖见 [requirements.txt](requirements.txt)。在本技能目录运行：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_contract.py --check-schemas
python3 scripts/validate_contract.py validate input /path/to/project/ecp-data-mapping/input.json --project-root /path/to/project
python3 scripts/validate_contract.py validate output /path/to/project/ecp-data-mapping/output.json --project-root /path/to/project
```

ECP 有限静态检查使用本目录 `scripts/validate_ecp_assets.py --help`。当前数据源与 ECP 编译、导入、发布或运行仍需任务环境提供真实访问能力和对应授权。`data-lineage.json` 是设计期审计资产，不等于 Runtime 已产生 source-record → assertion → result 的运行血缘。

## 验收与排查

以 [输入合同](contracts/input.schema.json)、[输出合同](contracts/output.schema.json) 和 [验收清单](references/acceptance.md) 为准。缺少 Python 库时安装本包依赖；缺少随包文件时恢复当前版本完整目录，不从其他技能查找替代文件。摘要不符时核对内容变化并重新确认受影响版本，不能只刷新摘要冒充原批准仍有效。

本地 Schema 检查只证明结构、引用和摘要等有限条件，不能证明专家认可、模型行为、宿主上下文隔离或实际平台执行。当前保持 scaffold 候选；真实模型评估和宿主安装验证尚未执行。来源版本与快照摘要见 [资料清单](references/sources.json)，权利与方法借鉴见 [来源说明](THIRD_PARTY_NOTICES.md)。
