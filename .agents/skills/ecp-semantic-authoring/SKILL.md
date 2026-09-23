---
name: ecp-semantic-authoring
description: 将已确认且固定版本的领域模型忠实转译为 ECP Ontology、SHACL、Derivation、Evaluation 和 Action Policy，交付模型到实现的对应与能力缺口。用于 ECP 资产编制和语义实现审查；不重定义业务知识、不猜测数据映射，也不导入、发布或运行平台。
metadata:
  author: Hovo
  version: "0.2.1"
---

# ECP 语义资产编制

维护平台表达，保留业务定义。

## 合同

读取 [共享合同](contracts/README.md)、[输入 Schema](contracts/input.schema.json)、[输出 Schema](contracts/output.schema.json) 和 [验收清单](references/acceptance.md)。先按实际资产定位 Kit 指南，不能把通用 OWL/SPARQL 示例视为 ECP 支持证明。

本目录资源自包含，可直接调用，不依赖其他技能入口或安装位置。输入可以由人工、其他工具或其他技能提供；只核对资产合同、来源与必要确认，不要求前序技能执行记录。

## 产物目录

调用方项目的 `ecp-semantic-authoring/`（或同等阶段目录）根部只放正式 `input.json`、`output.json`、`review.md` 和实际语义资产。候选、生成日志、校验快照及包外草稿放在该阶段的 `process/` 或项目 `reports/<run-id>/ecp-semantic-authoring/`，不得写入技能包目录。

本地校验入口与依赖见 [README](README.md)。按本技能验收完成交付后结束，不自动调用下一技能。

## 执行顺序

1. 核对模型与确认的精确版本、案例、Profile 与合同摘要。缺模型确认向模型责任人返回问题；缺当前平台信息时只编制基于指定 Kit 的候选。
2. 为每个模型要素指定实现落点，列出不支持部分和外部责任，形成 implementation_map。
3. 依正式格式生成所需 Ontology、SHACL 和规则；保持 IRI 稳定，保留单位、时间、身份及未知语义。只产出本次能力需要的资产。
4. 列出规则需要的语义事实，交给映射阶段落实。Mapping 反馈可以调整忠实表达中的技术细节；改变模型含义则提出 CHANGE_REQUEST，等待上游确认。
5. 用案例与禁止结果复核，按授权调用有限静态工具。尚未取得编译器预期的 Evaluation 留在包外，不伪造平台证据。
6. 生成 `ecp-semantic-authoring/output.json` 与 `review.md`，登记候选、包外草稿、依赖、Capability Gap 与分项状态。提交实现负责人确认，交付可供数据映射使用的资产。

编译错误返回本技能修订所属表达；涉及业务规则时返回知识或模型责任人。不得通过删要求、降低约束或改预期掩盖失败。已编制、静态已检查和平台已编译必须分别报告。
