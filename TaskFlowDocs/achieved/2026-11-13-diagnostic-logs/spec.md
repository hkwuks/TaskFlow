# Spec — TaskFlow 脱敏诊断日志与导出
> Task version: v1

## Objective and Success Criteria

以最小可观测元数据诊断真实宿主事件，并提供明确、可测试的隐私和非阻塞边界。

## Architecture Boundaries and Responsibilities

宿主负责实际投递事件，TaskFlow 仅记录接收到的已知事件；记录器不读取会话或其他日志，不推断模型思维。导出只处理本模块的结构化数据并重新校验。

## Project Structure / Affected Files

复用 `hooks/` 及各宿主现有事件接线；按实际需要补充日志命令、自动测试、TaskFlow skill 和中英文 README。不得修改用户 Agent 配置目录。

## Interfaces, Data Flow, and Contracts

提供用户可发现的启用、停用和导出命令。默认无配置视为关闭；启用状态与日志存放于任务工作区的本地 Git 元数据，不进入 Git 提交。事件进入记录器前必须降为固定枚举；未知值统一归为 unknown 或丢弃，绝不保存原值。能力标识只有硬编码允许值可写，其余使用类别或 unknown，不将任意宿主名字、路径或哈希作为安全替代。

记录采用结构化单行格式，字段和可取值均严格白名单；时间仅由记录器生成。绝不将原始输入、错误消息或命令参数写入。导出重新解析并重建允许字段，拒绝或跳过异常记录；目标已存在时不覆盖，失败不留下看似成功的导出。

## Invariants and Compatibility

日志记录是可选、异步且可丢失的旁路；日志输出的任何磁盘 IO 或等待不得发生在受观察执行路径。不得依赖新增的兼容代码或外部依赖。仅对实际宿主提供且验证的事件声称覆盖。

## Validation and Error Semantics

测试包含默认关闭、启停、导出与已有目标、结构化允许列表、带令牌和私人信息的输入、篡改的本地记录、并发、不可写存储和可控长时间阻塞的写入；验证被观察流程及时完成且输出未变。测量和记录受控真实宿主投递，明确无法证明 skill 内容已采纳或解释未观察到的调用。

## Code and Test Constraints

复用既有测试框架；不接触用户个人文件或凭据。运行适用 smoke、离线评估及 `git diff --check`，如宿主或环境不可用则保留未验证状态。

## Design Decisions and Alternatives

选择默认关闭、固定枚举、用户指定本地导出；较宽泛的正则脱敏不能保证未知密钥和代码安全，因此不将原始内容交给日志存储。诊断所需的细节与严格隐私冲突时保留隐私边界并公开可观察性限制。

## Open Questions

不同宿主的异步投递和事件字段需先以现有运行时实现及验证结果确定；不以静态配置代替真实宿主验证。
