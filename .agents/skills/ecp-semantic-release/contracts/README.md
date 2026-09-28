# ecp-semantic-release 资产合同 2.0.0

2.0.0 只接收一个 ecp-semantic-authoring 2.0.0 技术语义模型闭包，不再接收独立 ecp-data-mapping 输出。

进入 release 前必须有两份独立外部确认，且都绑定同一个 authoring ArtifactRef 的完整身份、版本和字节摘要：
- semantic_confirmation：语义实现负责人确认忠实转译；
- data_confirmation：数据负责人确认真实源绑定、身份、Join、NULL、时间、Coverage 与 UNKNOWN 传播。

这两份确认体现职责分离，不再通过两个技能目录制造阶段分离。

动作只支持 COMPILE、PUBLISH、VERIFY_RUN。COMPILE 创建不可变 Revision 并执行目标环境 V3 原生跨资产候选编译；PUBLISH 只能建立在该精确候选编译成功之上；VERIFY_RUN 只能针对固定 Release 和 Run。

output.json 分别记录 members、Revision、compilation_report、Release、Runtime 和 CaseResult。任何平台 PASS 状态都必须引用真实证据；静态检查、编译、发布、运行与业务验收不得互相冒充。
