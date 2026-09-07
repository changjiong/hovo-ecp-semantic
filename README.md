# hovo-ecp-semantic 0.3.0

依据三册V2.0，以可验证能力问题为切片，设计、审阅、生成和打包ECP（企业认知平台）本体语义资产。正式技能名沿用仓库名称，不新增 `semantica` 别名或兼容入口。

## 本版重点

不是让模型“扮演专家”，而是要求每个核心概念明确：定义、粒度、身份、参与关系、时间计量和消费反例。先说明建模承诺，再按平台能力落实；不能因某公理不支持就静默删除业务要求。

三册原始Markdown（轻量标记文本）已按字节保存，章节路由和摘要见 `references/handbook-index.md`、`references/handbooks-v2/source-manifest.json`。第三册工程保留为参考，不自动当成ECP工作区。

## 使用

把完整 `hovo-ecp-semantic/` 文件夹放入宿主支持的技能目录，不只复制入口。依赖安装与本地检查：

```bash
python -m pip install -r requirements.txt
python scripts/run_verification.py --output ../hovo-verification
```

本轮基础依赖的具体版本另存于 `requirements-tested.txt`（实测依赖快照），并非离线安装包或其他环境的兼容性证明。

当前操作命令：

```bash
python scripts/scaffold_design.py ./new-project
python scripts/validate_design.py ./new-project
python scripts/validate_ecp_assets.py ./ecp-workspace --json-out ../asset-check.json
python scripts/package_workspace.py ./ecp-workspace --output ../new-workspace.zip
```

摘要只有在确认源改动后才单独刷新：

```bash
python scripts/refresh_workspace_digests.py ./ecp-workspace
```

随后必须重新验证。打包不会刷新摘要，也不会覆盖已有输出；未登记草稿、目录逃逸、符号链接和非法引用均阻止打包。

## 典型任务

“根据这些制度、来源模式与已有资产，按三册V2.0先做一个直接持有人查询切片；解释核心建模取舍，生成需要的ECP资产和正反例。缺真实输入只局部阻塞。”

“审阅这个模型的身份、时间和计量是否合理；不要修改文件，给出有来源的缺陷与最小修订。”

“扩展贷后事件场景，先检查哪些主体与证据语义可复用，不直接套用所有权模型。”

## 交互

默认证据优先；最多一轮、五个高影响问题。可逆设计采用推荐并留痕，真实数据、规则阈值、权限与批准不得假设。研讨仅显式开启，不把29项变成29次拷问。

## 实测与未执行

最新运行证据以 `reports/verification.json` 为准，不以本说明中的旧数字为准。工具单元测试、手册参考工程、样例合同、实际模型生成和平台验收分列。关键词路由检查不等于模型触发评估；文字存在性不等于真实交互遵从。

标准SHACL（形状约束语言）实例验证可通过 `scripts/validate_shacl_instance.py` 运行；额外依赖见 `requirements-shacl.txt`。依赖缺失时明确未执行，不使用自写检查冒充标准引擎。完整OWL（网络本体语言）一致性、平台编译和独立业务审核不由本地脚本自动授予。

## 文件职责

- `SKILL.md`：唯一技能入口和阅读路由。
- `references/handbooks-v2/`：三册规范源及摘要。
- `references/ecp-kit-1.7/`：原工具箱快照，未静默改写。
- `assets/`：最小设计契约模板与模式；不是导入资产。
- `scripts/`：确定性检查、只读打包和本地验证。
- `examples/`：受限示例与原手册参考实现。
- `evals/model-generation/`：真实生成评估任务与证据规范，未执行状态不伪造。
- `reports/`：本版实际验证与交付记录。

## 发布边界

这是内部交付候选，不是银行生产批准。随包材料包含用户提供的第三方引文与平台规范；公开再分发权限尚未确认，见 `THIRD_PARTY_NOTICES.md`。本次没有远程推送或平台写回。
