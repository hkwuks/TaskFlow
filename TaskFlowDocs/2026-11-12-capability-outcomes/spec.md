# Spec — 能力选择与真实问题解决调查
> Task version: v1

## Objective and Success Criteria

让开发阶段真正使用适合当前问题的能力并解决用户问题；不能用填写字段、调用无关工具或测试字符串替代行为验证。

## Architecture Boundaries and Responsibilities

- 宿主事件只能证明事件到达及记录，不能单独证明能力相关、被采纳或修复成功。
- TaskFlow 负责阶段路由与有界提示；专家能力负责具体调查和规划；评估由独立的真实案例和产物检查完成。
- Codex `apply_patch` 与通过 shell / Python 写文件走不同事件路径；不得把某一工具上的门禁宣称成所有写入的强制保证。

## Project Structure / Affected Files

调查范围：`hooks/prompt-reminder`、`hooks/capability-evidence`、`hooks/capability-gate`、`hooks/hooks-codex.json`、`skills/taskflow/SKILL.md` 和现有测试；具体修改须依据验证结果确定。

## Interfaces, Data Flow, and Contracts

当前机制观察：`capability-evidence` 接受 `mcp__*` 事件；`capability-gate` 按队列先后匹配阶段。事件与阶段意图及产物贡献没有一一对应，允许 unaided，审批检查审查字段完整性而非结论正确性。不能将这些机制视为真实能力选择或问题修复的证明。

规划技能默认输出 `tasks/plan.md`；TaskFlow 把任务目录的 `plan.md` 作为事实源。采用技能的方法时将有效内容纳入 TaskFlow 的指定文档，保留被 hooks 匹配的标题和字段，不另造竞争文档。

## Invariants and Compatibility

不从任意事件推断模型内部动机；不声称所有宿主事件行为相同；不改变仓库外的个人配置。未获真实效果证据之前，不把提示或强制字段作为最终修复。

## Validation and Error Semantics

基线包括本次遗漏能力的真实会话与 digdig 原始案例。后续受控实验要固定任务、模型、工具可用性、提示和宿主，比较具体任务的能力选择、根因证据、计划可执行性与产物；必须记录实际调用、提示到达、错误、结果和盲评口径。至少包含无需外部能力的简单对照，不能强迫所有任务调用技能。一次提示主动要求读技能的运行不构成引导效果验证。

真实模型测试前须由操作系统限制文件读取，仅向 OpenAI 模型服务提供获准的测试材料和仓库数据。普通 read-only 沙箱仍允许读取本机记忆，不能作为隔离证明；Windows 二进制由 WSL 互操作启动不能假设被 Linux mount namespace 隔离；凭据也不能被模型工具读取或输出。无法证实边界时不得启动。

## Code and Test Constraints

定向测试事件形状与脚本入口，真实行为测试必须独立于标记字段；所有夹具保留或按用户许可清理。

## Design Decisions and Alternatives

- 候选 A：加强当前阶段的能力选择提示。成本较小，但需实测是否改变选择与产物，不能仅比较提示字符串。
- 候选 B：提高调用和阶段的对应准确性。可以减少错配，但仍不能证明调用有用，单独实施只会增加流程标记。
- 候选 C：改变模型与流程交互方式，把确定性操作交由程序负责。可能降低复杂度，但须先定位真实摩擦，不预设改造。
- 硬门禁：可能阻断无适合能力的场景；用户要求先实测再决定，不预设增加。

## Open Questions

缺少可同时限制文件读取和凭据暴露的真实宿主隔离运行环境；当前 WSL 只有 Windows 版 Codex 包，不能证明 Linux 隔离包住 Windows 进程。候选方案尚未决定。
