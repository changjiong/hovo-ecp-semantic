# ecp-semantic-authoring

把固定领域模型转成受目标 ECP 合同约束的语义资产，保留每项业务要求的实现对应和无法覆盖部分。Hovo 0.2.1，本地候选；接收领域模型合同2.0.0，本阶段资产合同仍为1.0.0。

> 使用 ecp-semantic-authoring，将这份已确认模型按指定 Profile 编制为 ECP 资产，交付实现对应、事实需求和能力缺口。

输入与输出分别见 [输入合同](contracts/input.schema.json)、[输出合同](contracts/output.schema.json)。输出 `ecp-semantic-authoring/output.json`、`review.md` 及实际 TTL/JSON；未取得编译器预期的 Evaluation Definition 留作包外草稿。

## 独立安装与使用

将本技能整个目录放入宿主支持的 skills 目录即可单独调用，无需安装其他技能。本包自带合同、方法资料、ECP Kit 1.7 和职责所需工具，不依赖相邻目录。输入可由人工、其他工具或其他技能提供；按 [合同说明](contracts/README.md) 整理引用、来源和必要确认。完成本技能交付后结束，不自动启动下游。

Python 3.10+ 的本地检查依赖见 [requirements.txt](requirements.txt)。在本技能目录运行：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_contract.py --check-schemas
python3 scripts/validate_contract.py validate input /path/to/project/ecp-semantic-authoring/input.json --project-root /path/to/project
python3 scripts/validate_contract.py validate output /path/to/project/ecp-semantic-authoring/output.json --project-root /path/to/project
```

ECP 有限静态检查使用本目录 `scripts/validate_ecp_assets.py --help`。标准 SHACL 实例检查另需 [requirements-shacl.txt](requirements-shacl.txt)，入口为 `scripts/validate_shacl_instance.py --help`。当前数据源与 ECP 编译、导入、发布或运行仍需任务环境提供真实访问能力和对应授权。

## 验收与排查

以 [输入合同](contracts/input.schema.json)、[输出合同](contracts/output.schema.json) 和 [验收清单](references/acceptance.md) 为准。缺少 Python 库时安装本包依赖；缺少随包文件时恢复当前版本完整目录，不从其他技能查找替代文件。摘要不符时核对内容变化并重新确认受影响版本，不能只刷新摘要冒充原批准仍有效。

本地 Schema 检查只证明结构、引用和摘要等有限条件，不能证明专家认可、模型行为、宿主上下文隔离或实际平台执行。当前保持 scaffold 候选；真实模型评估和宿主安装验证尚未执行。来源版本与快照摘要见 [资料清单](references/sources.json)，权利与方法借鉴见 [来源说明](THIRD_PARTY_NOTICES.md)。
