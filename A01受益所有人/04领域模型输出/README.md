# 04 领域模型输出

当前根目录是 `domain-model 1.0.0` 的 Business Domain Model（业务领域模型）正式草案输出边界。

- `input.json`：本次 PRODUCE + FULL_BASELINE 请求。
- `model.yaml`：纯业务模型，只包含业务对象、业务关系、业务判断和最小外部上下文。
- `coverage.json`：固定 Domain Knowledge 5.0.0 到模型的规则、问题、案例、OPEN 与 MODEL_GAP 审计。
- `review.md`：由 model.yaml 生成的业务审阅视图。
- `coverage.md`：由 coverage.json 生成的覆盖审计视图。
- `output.json`：精确引用本次 model / coverage / request 的交接索引。
- `archive/`：旧模型和旧交付，仅供追溯，不作为 PRODUCE 语义来源。

当前模型版本：`2026-09-28.business-v1.0.0.draft.1`。
当前知识版本：`2026-09-24.draft.1`（DRAFT）。
业务确认：PENDING。
