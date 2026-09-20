# Lineage Contract v1

本目录只定义当前能够明确落地的设计期数据血缘，不建立通用血缘引擎。

## Design-time Data Lineage

机器合同见 [design-time-data-lineage.schema.json](design-time-data-lineage.schema.json)。

它回答：

> 一个已定义业务事实或业务身份，在设计上由哪个 Mapping、哪些 Scan/Column、哪些 Join 提供？

它不回答：

> 本次 Run 实际读取了哪一行？

后者属于 Runtime Data Lineage（运行期数据血缘），由 ECP Runtime 的 Snapshot / Assertion / Derived Fact / Evaluation / PROV 链负责。当前仓库只规定责任边界，不虚构尚未由 Runtime 保证的 wire 字段。
