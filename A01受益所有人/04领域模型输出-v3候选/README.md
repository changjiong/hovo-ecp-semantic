# A01 受益所有人领域模型 v3 候选

本目录基于：

- `domain-model（领域模型构建）` 0.8.0 的新边界；
- `03领域知识输出-v3候选/review.md` 3.1.0-draft；

形成一版平台无关的 UBO（最终受益所有人）领域模型候选。

## 文件

- [review.md](review.md)：业务专家主读的领域模型审阅稿；
- [model-candidate.yaml](model-candidate.yaml)：平台无关结构化模型候选；
- [coverage.md](coverage.md)：69条知识规则、30个业务问题和8个OPEN到模型的承接说明。

## 这版模型最重要的变化

1. 不再用一个“非自然人主体”同时表示公司、分支机构、信托和资产管理产品；
2. 将“适用哪套法定基础识别规则”和“是否免于/简化/加强”拆为两个判断维度；
3. 直接持有关系与最终所有权计算结果分开；
4. 实际控制关系与职位、第一大股东、第三方标签分开；
5. 管理人员兜底以“负责日常经营管理”的事实为中心，不以固定职位替代；
6. UBO结果拆成 `QualificationBasis（认定依据）` 和 `BeneficialOwnerStatus（当前状态）`；
7. 时间挂在基础事实和每项认定依据上，保留历史；
8. 上游8个OPEN原样进入模型边界，不由模型补业务政策。

## 为什么不是正式 model.yaml

正式 Domain DSL 2.0 要求精确绑定 Contract 4.0.0 的上游领域知识 `output.json` 和 SHA-256 digest。

当前 PR #8 的 v3 领域知识还是业务候选稿，没有正式生成新的 `output.json`。因此这次不伪造一个看起来“contract-valid（合同有效）”的 `model.yaml`，而先使用 `model-candidate.yaml` 验证业务抽象。

## 下一步

先由业务专家审：

- 对象边界；
- 基础识别规则 / 识别措施两层结构；
- QualificationBasis / BeneficialOwnerStatus；
- 时间；
- 8个OPEN。

业务抽象认可后，再在项目运行环境：

```text
domain-knowledge 1.1.0
→ 正式 output.json
→ domain-model 0.8.0
→ 正式 Domain DSL 2.0 model.yaml
→ review.md / coverage.md / output.json
```

本候选不涉及数据库、BOMIS接口字段、ECP平台资产或运行算法。
