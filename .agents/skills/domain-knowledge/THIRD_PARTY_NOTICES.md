# 来源与权利

本技能由 Hovo 维护。随包手册 V2.1来自用户提供的固定版本材料，原文与摘要保存在本目录。用途和来源见 [资料索引](references/handbook-index.md) 与 [快照清单](references/sources.json)。本地可用不代表获得公开再分发许可，未增加新的公开授权。

技能工程方法采用用户指定的 qiaomu-meta-skill：精简入口、按需加载参考资料、输入输出合同与分项证据。上游标注 Copyright (c) 向阳乔木；X https://x.com/vista8，GitHub https://github.com/joeseesun/ 。这些属于方法借鉴，不构成本技能的运行依赖。

已有方法参考 OntologyEX 的能力问题与消费者边界，以及 ontology-agent-suite 的证据记录与分阶段审阅；未复制其实现。没有比较评估证据，不宣称效果优于这些技能。当前修订聚焦业务可读交付与可审查判断解释；设备维护材料为本次编制的合成教学内容，不提供真实制度或行业规则。


## TypeSafe Jev

模糊文档边界判断运行时使用 TypeSafe Jev API 和 `typesafe-sdk` Python SDK。该依赖只用于有限集合结构判断，不用于生成或改写领域知识。模型请求固定使用 `jev-latest`，实际解析后的模型版本随 BoundaryDecision 一并记录。

项目参考 TypeSafe 官方 Quick start、Choice、Confidence 与 Python SDK 文档确定请求/响应合同和置信度门控方式。TypeSafe 服务及 SDK 的权利、许可和服务条款由其各自发布方负责；本仓库不复制模型权重。
