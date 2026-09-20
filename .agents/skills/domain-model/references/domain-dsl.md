# Domain DSL 2.0.0

## 定位：领域模型 IR，而不是影子运行时

本语言首先是平台无关、机器可读的领域模型 IR（中间表示）。它负责无歧义表达业务对象、身份、关系、时间、规则合同、人工判断和过程依赖，使后续实现阶段无需重新猜测自然语言；它不承担数据库访问、ECP 平台能力或生产业务执行。

表达式和本地求值用于减少阈值、布尔条件、未知值和简单计算的歧义，并为案例提供有限验证辅助。是否能被本地解释器完整执行，不是领域模型完成条件。不要为了让模型“可运行”而加入平台算法、数据库操作、网络访问或只服务单一领域的执行机制；复杂计算先明确输入、输出、数学/业务语义、未知处理与适用前提，无法由通用构造无歧义表达时登记语言能力缺口，再由后续实现阶段选择算法。

本地、声明式、基于 YAML 的领域语言；规范结构由 `contracts/domain-model.dsl.schema.json` 约束，跨引用与表达式类型由 `scripts/domain_dsl.py` 检查。无需数据库或 ECP。所有对象拒绝未知字段；safe loader 拒绝重复键、别名、合并键、自定义对象标签及非 JSON 数据。日期使用带引号的 ISO 字符串。Date 严格为 YYYY-MM-DD；DateTime 必须带时区，求值时统一 UTC。

## 根结构

`dsl_version, artifact_id, content_version, name, knowledge_ref, knowledge_basis, question_scope_ids, types, temporal, rules, state_machines, judgments, question_coverage, case_explanations, upstream_issue_bindings, issues` 必须完整提供；不适用的集合写空数组。

knowledge_ref 为精确版本、路径、sha256 的知识 4.0.0 ArtifactRef。依据链来自知识中的 statement、term、rule 标识；模型不得创建新的制度断言。knowledge_basis 表示上游依据状态，不是 DSL 的业务批准。

## 类型与关系

Type：`id, name, kind, description, basis_ids, identity, fields, examples, counterexamples`。kind 为 ENTITY/ROLE/FACT/EVENT/OBSERVATION/EVIDENCE/DECISION/TASK。identity 至少一个本类型字段，每个键为必需、单值。角色额外提供单值、必需 Ref 的 bearer_field。

Field：`name, label, type, cardinality: {min, max}, description`。max=null 表示多值无上限。类型为 Text/Boolean/Integer/Decimal/Date/DateTime/Enum/Ref/IntervalSet；Enum 必须声明 values，Ref 必须声明 target。关系由 Ref 字段的方向、目标类型、基数表达，不重复另建关系表。

identity 声明不是缺证时生成虚拟身份的许可。输入记录中的未知值须保留未知。Decimal 用十进制数值运算；原始输入推荐十进制字符串，求值的 Decimal 结果按字符串输出以保精度。禁止 NaN/Infinity。加法、乘法及路径连乘按操作数确定精度，拒绝隐式舍入；精度和指数规模超过10000位时报错，不给近似阈值结论。

## 时间

Temporal：`id, type_id, start_field, end_field, end_status_field, basis_ids`。起止同为 Date 或同为 DateTime；起点必需、终点可空，状态 Enum 包含 OPEN/KNOWN/UNKNOWN。

区间为 `[start,end)`：OPEN 代表有依据确认尚未终止，UNKNOWN 代表无法确定终止，二者均可有空 end，但不可互换。KNOWN 必须 end>start。同日先后无法证明时不能假造精度。

## 规则表达式

Rule：`id, name, description, inputs, result, expression, on_unknown: PROPAGATE, basis_ids`。输入按 name 声明类型；结果声明类型。表达式四选一：

```yaml
expression:
  op: and
  args:
    - input: corrected
    - input: consistent
```

其他表达式：`{literal: {type: Integer, value: 25}}`、`{field: {of: {input: self}, name: state}}`。只有声明过的输入、字段、运算符可用；没有字符串代码或eval；依赖声明不执行跨规则调用。

| 运算符 | 参数 | 结果 |
| --- | --- | --- |
| and/or | 至少两个 Boolean | 三值 Boolean |
| not | 一个 Boolean | 三值 Boolean |
| eq/ne | 两个兼容单值 | Boolean 或 UNKNOWN |
| lt/lte/gt/gte | 数值或相同日期类型 | Boolean 或 UNKNOWN |
| add/multiply | 至少两个数值 | Decimal 或 UNKNOWN |
| current_interval_start | IntervalSet, Date, Boolean, Boolean | Date 或 UNKNOWN |

null 表示 UNKNOWN；不能把缺失变成 false 或 0。false AND unknown=false，true OR unknown=true，其余按三值逻辑。比较未知值仍为 UNKNOWN。

current_interval_start 的后两个参数为 history_complete、continuity_verified。任一不为 true 或任一区间终止未知，返回 UNKNOWN。有证据支持完整性与连续性后，才归并重叠/相接区间并取包含 as_of 的当前区间起点；真实空档保留。没有当前达标区间返回 UNKNOWN。输入区间为 `{start, end, end_status}`，此运算符只接受 Date。它不证明输入的历史完整性或实际法律生效。

## 状态与人工判断

StateMachine：`id, type_id, state_field, initial, transitions, basis_ids`。state_field 为单值 Enum；迁移：`id, event, from, to, guard, on_unknown: BLOCK, basis_ids`。guard 只读取 self 记录，必须为 Boolean。同一状态与事件不得出现两条路径；本版不推测优先级。求值只计算转换建议，不写数据库，不自动保存历史。

Judgment：`id, name, description, inputs, outputs, responsible_role, required_evidence, question_ids, issue_ids, on_missing: BLOCK, basis_ids`。这是显式人工裁定边界，没有自动求值。nature=BUSINESS_DISCRETION 表示具有完整准则的业务判断，允许无缺口；nature=UNRESOLVED_POLICY必须关联影响全部相关问题的开放MODEL_GAP。

## 覆盖与确认

question_coverage 逐题列模型 ID、缺口 ID、MODELED/PARTIAL/DEFERRED 与原因。case_explanations 逐例保留知识预期及禁止结果，标 EXPLAINED/BLOCKED；解释不等于执行通过。upstream_issue_bindings 穷举上游 OPEN，含范围外及理由；未解决的上游问题对应本地开放缺口。

输入、DSL 和交接须绑定同一知识版本及问题范围。review.md、coverage.md 为确定性视图；合同检查比较其生成字节以发现单独修改。审阅意见另写 review-session-log.md，修订在 DSL 中落实。

## DSL2 必需的业务描述

根增加scope_mode、constraints、processes、rule_coverage。Type增加term_origin（KNOWLEDGE/PROPOSED）、business_sentence、why_object、identity_description。名称的业务质量仍需语义审查；结构字段齐全不是质量证明。Field可用value_labels为枚举值给业务名称；若提供必须覆盖全部枚举。

Input增加必需label与binding，可选cardinality。binding是TypeID或TypeID.field；直接字段绑定的类型、目标、枚举和基数必须一致。Rule增加question_ids、depends_on、result_binding、business_meaning。结果必须绑定字段。前序依赖必须读取前序结果字段，依赖不得循环；依赖只作声明，不自动求值整个规则网。

Constraint为id/name/type_id/expression/on_unknown/basis_ids；self是type_id的记录，表达式返回单值Boolean。用于表达记录不变量。evaluate和transition先检查输入Ref及嵌套Ref的全部声明约束；违反约束或证据不足均返回BLOCKED，并记录具体约束与BLOCK/REVIEW处置。标量字段输入不等于整条记录，不能证明所在对象全部约束成立。未运行记录校验时不能宣称实际记录已符合约束。

Judgment增加nature、criteria、record_fields、review_requirements；inputs/outputs与规则一样绑定字段，输出列入record_fields。BUSINESS_DISCRETION可完整建模人工裁定；UNRESOLVED_POLICY需开放事项。规则不能求值并不自动成为业务人工裁定。

StateMachine和Transition都增加业务name，用于审阅稿。业务状态值优先使用明确中文或value_labels。

## 集合与日期表达式

query节点为`{query: {from: Expr, as: Name, where: Expr, select: Expr}}`。from为多值；as在局部绑定单个元素，不得遮蔽外层变量；where为Boolean，select为单值。过滤条件或被选值不确定时返回UNKNOWN，不悄悄丢弃未知记录。集合形状与单值分别检查。

| 运算 | 参数 | 含义 |
| --- | --- | --- |
| is_known | 一个表达式 | 检查值是否已提供；不证明真实性或集合完整性 |
| if | Boolean, 同类型真分支, 假分支 | 条件未知则未知；只求值选中的分支 |
| list | 同类型单值若干 | 构造集合；空集合推断为Text集合 |
| count | 集合 | 数量，未知集合不作0 |
| sum/product | 数值集合 | 合计/连乘；空集合分别0/1，业务须另检验完整性 |
| all/any | Boolean集合 | 三值聚合；空集合分别true/false |
| contains | 集合, 单值 | 有确定匹配为true；未知元素可能使否定结果未知 |
| distinct | 集合 | 标量去重；Ref按业务身份去重，冲突记录不擅自择一 |
| date_add_days | Date, Integer | 自然日偏移 |
| date_add_months | Date, Integer | 月份偏移，月末超出时取目标月末 |
| date_year/date_month | Date | 取得年月，不把DateTime静默降精度 |
| intervals_of | Ref集合, 起点字段文本, 终点字段文本, 状态字段文本 | 从明确Date/Date/状态字段形成IntervalSet |

集合输入由cardinality声明。所有单值运算拒绝集合。表达式Integer可扩为Decimal；Enum可按受限Text比较；Text计算结果落入Enum字段时，实际求值必须验证枚举成员。未知规则结果不会由默认值补齐。

## 业务过程

Process含id、name、question_ids、trigger、steps、basis_ids。Step含id、name、kind（DETERMINE/VERIFY/RECORD/REQUEST/UPDATE）、uses、reads、writes、depends_on、on_missing、description、basis_ids。reads/writes为真实Type.field；uses引用规则、判断、约束或状态机。判断/核验步骤必须有机制。声明规则/判断的步骤须包含其全部字段输入输出；步骤依赖仅在同一流程内且无环。本地解释器不执行外部请求或业务流程。

## 七要素覆盖与案例

rule_coverage逐条保留knowledge_rule_id、question_ids、model_ids、status、gap_ids和facets。facets固定七项scope/preconditions/conditions/result/exceptions/missing_evidence/effective_period，每项有source_text原文、model_refs精确引用、explanation、status（FORMALIZED/MANUAL/MIXED/GAP）。条件FORMALIZED须引用规则或约束的.expression或迁移.guard；MANUAL须引用判断.criteria；MIXED须同时引用计算表达式和人工准则；GAP须关联开放事项。

model_refs允许元素ID、Type.field，以及机制成员.expression/.on_unknown/.result_binding、判断.criteria/.required_evidence/.on_missing/.review_requirements、流程.trigger、步骤.reads/.writes/.depends_on/.on_missing和迁移.guard。引用存在不证明解释正确，仍需语义审查。

question_coverage增加question原文、answer、rule_ids（知识规则ID）、process_ids、case_ids，校验器从固定知识核对范围内逐题规则和案例集合。CaseExplanation增加title、input_facts原文、steps（model_ids+explanation）、execution、evaluation_ids。EXPLAINED只表示有解释；LOCAL_EVALUATION/MANUAL_REVIEW需要交接证据标识。NOT_EXECUTED必须没有执行证据。

知识合同仍4.0.0；当前模型交接合同5.0.0、DSL2.0.0，不接受旧DSL1文件。历史版本归档，新的model.yaml及其生成文档构成当前唯一模型。


## 身份与无环图

identity_key(单值Ref)依该类型声明的业务身份字段生成稳定的带类型身份键；引用身份递归按自身身份取值，不能用姓名代替。dag_path_products(边Ref集合, 起节点Text, 终节点Text, 起节点字段名Text, 终节点字段名Text, Decimal权重字段名Text)枚举给定有向无环图的全部路径乘积。重复边按身份去重，同一身份矛盾记录报错；任一未知边/权重或图中循环返回UNKNOWN。10000边或100000路径展开步的安全上限超出时明确报错，不返回截断结果。调用规则必须另核对图范围、时点与完整性。

现有图运算只作为已经纳入 DSL 的受限数学语义与验证辅助，不构成继续把平台图算法搬入领域语言的先例。它不定义持股循环的法律算法，也不证明输入结构完整。领域规则负责权利类型及时间筛选，并明确循环等上游未决项。新增复杂算法前应先判断是否属于跨领域、稳定的业务语义构造；若只是平台实现方案，应留在后续实现阶段。

字面值可以用类型明确的null表示UNKNOWN，使条件不满足或材料不齐时保留未知；它不能以空值证明事实为否。is_known仅检查值是否存在，不证明真实性或完整性。

生成器支持--refresh-draft重生成同一模型身份和内容版本、业务评审NOT_EXECUTED且确认PENDING的工作草稿；生成后仍不继承检查或确认状态。已业务评审或更换内容版本时须先归档旧成果。
