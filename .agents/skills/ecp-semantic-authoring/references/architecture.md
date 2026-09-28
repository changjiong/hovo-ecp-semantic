# Authoring 与 Mapping 合并评审

## 结论

合并为一个 ecp-semantic-authoring（ECP 语义资产编制）技能，删除 ecp-data-mapping（ECP 数据映射）技能。

## 依据

ECP 2026-09-28 当前建模顺序明确为 Ontology/SHACL → Mapping → Derivation/Evaluation/Lifecycle/Action Policy → 不可变 Draft Revision → 跨资产候选编译。平台控制面把 Ontology、Mapping、SHACL、Derivation、Evaluation、Lifecycle、Action Policy 作为同一个 Published Release（已发布版本）的资产成员。

V3 Mapping 的 ontologySourceDigest 绑定 Ontology 精确字节，这使 Mapping 与本体不是两个可独立封版的阶段。任何 Ontology 字节变化都会使 Mapping 失效；任何数据绑定缺口也会影响 Derivation/Evaluation 可消费事实。把两者拆成两个技能会人为产生往返交接和两个不必要的“确认后才能继续”闸门。

## 保留的职责分离

合并的是执行阶段，不是治理责任：
- 领域负责人：确认平台无关 Business Domain Model；
- 语义实现负责人：确认业务模型到 ECP 表达的忠实性；
- 数据负责人：确认真实源、身份、Join、NULL、时间和 Coverage；
- 发布负责人：授权目标 Workspace 的编译、发布和运行。

语义实现确认与数据确认绑定同一 authoring 输出，二者都通过后才能发布。

## 新主链

Document → Domain Knowledge → Business Domain Model → ECP V3 Authoring → ECP Release

其中 ECP V3 Authoring 内部顺序为：
1. Semantic skeleton：Ontology/SHACL；
2. Source binding：V3 Mapping；
3. Decision implementation：Derivation/Evaluation/Lifecycle/Action Policy；
4. Cross-asset closure：implementation_map、fact_bindings、coverage、cases；
5. 双责任人审查。

这保留了关注点分离，同时使技术语义模型与平台真实编译单元一致。
