# 版本化业务上下文参考模型

本目录是通用引擎使用范例，不是引擎保留表、内置业务模块或调度服务。采用 `ecp-versioned-business-context-input/1` 约定。源码所在的两个项目仍是同级独立仓库，本范例不依赖宿主 `v3/`。

## 文件与执行入口

`ontology.ttl`、`mapping.json`、`derivation.json`、`input-shapes.ttl`、`output-shapes.ttl` 是实际发布资产。`input-values.json` 为便于阅读的原始值，不是可以直接传给 ROWS 的协议帧。按 mapping 中的列类型生成完整 SourceRow；根据 recordKey 使用现有规范键算法生成 rowId，不能直接使用 tenant 或账户编号作 rowId。原生示例见 `crates/runtime/tests/business_context.rs`。

映射的 ontologySourceDigest 绑定 ontology.ttl 的精确字节；修改资产时必须同步摘要。输入形状放在 `asserted` 检查点，结果形状放在 `output` 检查点（资产字段小写）。两张源表有明确 FULL_SNAPSHOT 覆盖声明；声明不替代宿主对完整捕获的责任。

## 计算语义

每条账户有租户、到期时刻、观测时刻、金额。每个租户有一条上下文：evaluationAt、lookbackOffset、threshold、calendarPolicy。上下文使用稳定租户键，值变化只改变行版本；不同租户不会通过同一上下文行混合。

```text
windowStart = evaluationAt + lookbackOffset
needsReview = evaluationAt >= dueAt
           && observedAt >= windowStart
           && observedAt <= evaluationAt
           && amount >= threshold
age = evaluationAt - observedAt
```

本模型窗口为闭区间，lookbackOffset 不大于零，threshold 非负，calendarPolicy 必须为 ELAPSED_TIME。输入为带偏移的 dateTimeStamp，不查询服务器时钟或环境时区；天数是已逝时长，不是交易日/工作日。交易日需求应作为新的明确模型或版本化日历输入，不能把标签随意换成 LOCAL_BUSINESS_DAYS 后继续沿用计算。

## 可核对结果

初始 A 的观测时刻为 2026-01-01 00:00:00+08:00，到期时刻为 1 月 31 日，金额 150；上下文为 1 月 30 日、回看 30 天、阈值 100。初始 needsReview=false。只把 A 时点推进到 1 月 31 日，结果为 true；推进到 2 月 1 日，观测时刻离开窗口，结果为 false。B 的独立上下文与结果不变。

在 1 月 31 日把 A 阈值提高到 200，或回看缩短到 29 天，结果均为 false。等价的时区词法表达代表相同时间值，但原始行词法和版本仍不同，解释必须能反映实际源版本。

缺少上下文时不能从“没有结果”得出 false：targetObjectsOf 形状会对被引用却不存在的上下文产生违反，输出形状也要求每个账户具有唯一决策。负阈值、正回看或错误策略可能仍生成候选事实，但候选必须质量不合格。宿主不得绕过 strictCommitAllowed 使用这些结果。

## 更新、模拟与恢复

对上下文行发送带旧版本摘要的 REPLACE，使用现有 PREPARE 计算隔离候选。查看结果/QUALITY/PROOF 后可丢弃；满足明确的宿主政策后才能提交或提升。模拟与真实刷新使用同一计算路径，不另写时点分支。完整输入与检查点一起保留上下文版本；不能把最新时间自动注入旧检查点。

运行 `cargo test --locked --release -p ecp-v3-runtime --test business_context` 验证真实原生进程调用；CARGO_TARGET_DIR 应指向仓库外。此命令不是规模、长期或宿主业务存储验收。
