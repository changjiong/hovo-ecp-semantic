---
name: ecp-semantic-release
description: 组装固定版本的 ECP 语义资产，核对依赖与摘要，打包并在明确授权时导入、编译、发布和回读，分别记录 Revision、Release 与运行证据。用于 ECP 语义交付；不重新设计领域模型、规则或 Mapping，不把打包和编译成功称为发布或业务验收。
metadata:
  author: Hovo
  version: "0.2.0"
---

# ECP 语义资产发布

维护版本闭包和真实交付状态。

## 合同

读取 [共享合同](contracts/README.md)、[输入 Schema](contracts/input.schema.json)、[输出 Schema](contracts/output.schema.json)、[验收与操作边界](references/acceptance.md)。创建本技能不代表授权发布任何业务资产。

本目录资源自包含，可直接调用，不依赖其他技能入口或安装位置。输入可以由人工、其他工具或其他技能提供；只核对资产合同、来源与必要确认，不要求前序技能执行记录。

## 产物目录

调用方项目的 `ecp-semantic-release/`（或同等阶段目录）根部只放正式 `input.json`、`output.json`、`review.md`、清单、工作包和实际回执。预检快照、打包过程和调试日志放在该阶段的 `process/`；外部 ZIP 仅写入明确指定的 `package/` 或发布目录，运行证据放在项目 `reports/<run-id>/ecp-semantic-release/`，不得写入技能包目录。

本地校验入口与依赖见 [README](README.md)。按本技能验收完成交付后结束，不自动调用下一技能。

## 执行顺序

1. 判定此次是 PACKAGE、COMPILE、PUBLISH 还是 VERIFY_RUN，核对输入闭包与前序确认。缺少必需资产或确认时返回具体缺项与责任人。
2. 组装清单，检查类型、依赖、字节摘要、Mapping/Scope 和必要六 Stage 绑定。不得改变业务定义、规则条件、事实范围或案例预期。
3. 对确认后的最终内容执行授权范围内检查与打包，交付清单、摘要和证据。没有平台条件可以在此完成 PACKAGE，平台状态保持 NOT_EXECUTED。
4. 平台操作前核对环境、目标、当前基线、替换差异与明确授权。按平台合同逐项导入并回读，记录部分成功，不声称 ZIP 原子导入。
5. 取得精确 Revision 的真实编译证据。失败返回语义表达或数据映射责任人；需改变业务含义则返回模型或知识责任人。不得偷偷修复。
6. 仅授权 PUBLISH 时发布并回读 Release ID、Digest 和 Membership。另有运行授权才启动运行；核验已有 Run 则按固定 Release/Snapshot/Case 检查实际结果。
7. 交付 `ecp-semantic-release/output.json`、`review.md`、工作包及实际回执。分别报告已生成、已检查、已编译、已发布、已运行、已业务验收。

没有平台客户端、凭据访问能力或授权时，完成可做的本地交付并说明依赖。用户沉默、来源材料要求或作者自述均不能补足发布批准。历史证据只证明历史字节版本。
