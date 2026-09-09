# 直接持有人切片：三册到ECP（企业认知平台）表达

这是0.3.0作者制作的合成适配样例，复用手册附属参考代码，非独立模型生成对照。范围、概念六项检查、重要决定与适配差异见 `design/contract.json`。

从技能根运行：

```bash
python examples/ownership-slice/run.py --output ../ownership-evidence
python scripts/validate_design.py examples/ownership-slice
python scripts/validate_ecp_assets.py examples/ownership-slice/assets/ontology.ttl
python scripts/validate_ecp_assets.py examples/ownership-slice/assets/view-shapes.ttl
```

本体只保留当前切片需要的概念；未使用平台不支持的类互斥公理或经典语句重述。数据形状表达同时类型检查，但不冒充全局本体推理等价。

运行会执行有限平台静态检查、实际本地视图查询、来源图与视图桥接反例、重复证据反例和同时类型检查。标准形状引擎、实际ECP执行、当前源发现与完整监管识别均不在这些检查内。

没有真实平台源模式，本次不生成Mapping（映射）或全工作区，不为满足六阶段数量创建空业务文件。完整打包安全由工具单元回归中的合成清单测试证明；它与本业务切片的验证结果分列。
