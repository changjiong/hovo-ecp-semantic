# 03 领域知识输出

本目录是 `domain-knowledge` 在 A01 项目中的唯一输出边界。

- 根目录：当前待业务审阅的知识交付 `input.json`、`source-inventory.json`、`review.md`、`coverage.md`、`output.json`。结构校验通过不代表业务含义审阅或正式确认。
- `process/runs/`：按运行批次保存请求、规范化输入和生成脚本。
- `process/review/`：评审意见、任务跟踪和修订记录。
- `process/confirmation/`：确认记录。
- `process/validation/`：本阶段结构/合同校验快照。
- `process/package/`：知识阶段生成的中间阅读包及打包说明。
- `candidates/`：尚未确认的候选输出，不能当作正式知识版本。
- `archive/`：历史证据和旧版本，只用于追溯。

后续运行继续使用本目录，不再创建公共的 `过程与评审记录` 目录；跨阶段汇总证据放在项目级 `reports/<run-id>/`。
