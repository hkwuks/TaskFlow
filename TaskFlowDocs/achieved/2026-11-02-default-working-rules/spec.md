# Spec — 默认仓库规则

> Task version: v1
> Status: completed

## Objective

新用户的仓库里没有规则文档，而 TaskFlow 每个阶段都假设有。本模块补上这份缺失，并且**只在规则真正被需要的时候提出来**——建分支前、决定 commit 归属前、写代码前——因为用户在那三个时刻才判断得了这份默认值合不合适。

**目标用户**：第一次在自有仓库使用 TaskFlow 的人。他们的仓库里只有自己的代码。

**已有规则的用户不受打扰**：文件存在即视为用户所有，不被覆盖；只有检出与 TaskFlow 冲突的规则时给一条指向具体行的建议，且不修改。

## Commands

不需要新命令。三处接入点都是**已有的 Skill 阶段**，提醒由 `hooks/prompt-reminder` 同一条 `UserPromptSubmit` 事件带出。

```text
用户：帮我修个 bug
  ↓
TaskFlow 进入 Phase 1，准备建分支
  ↓
[提醒] 本仓库没有 CONTRIBUTING.md。建分支要选 feature/ fix/ docs/ chore/ 前缀，
       这份默认规则里有。要我创建吗？（可以先看内容）
  ↓
用户同意 → 写入 → 继续建分支
用户拒绝 → 不写 → 继续建分支（提醒不是门禁）
```

模板的展示与写入用两条命令，写入前必须先展示：

```bash
bash hooks/repo-rules show CONTRIBUTING      # 打印模板全文，不写任何文件
bash hooks/repo-rules create CONTRIBUTING    # 用户同意后才运行；同名文件已存在则拒绝
bash hooks/repo-rules check                  # 已有规则时，报告与 TaskFlow 冲突的行
```

`create` 拒绝覆盖已存在的文件，`show` 是纯读取——这两个性质让"同意后才写"成为命令本身的约束，而不是调用者的自觉。

## Project structure

```text
hooks/templates/CONTRIBUTING.md          # 新增：默认规则
hooks/templates/CODE_STYLE.md            # 新增：默认规则
hooks/repo-rules                         # 新增：show / create / check
hooks/prompt-reminder                    # 改：三个触发点各加一句
skills/taskflow/SKILL.md                 # 改：说明默认规则从哪来
skills/taskflow/references/artifacts.md  # 改：同上
hooks/README.md                          # 改：清单加 repo-rules
skills/taskflow/references/runtime.md    # 改：hook 树
hooks/smoke-test                         # 改：A1–A8 断言
```

`hooks/templates/` 是新目录。文件随插件分发，**不进入用户仓库**，除非用户同意后由 `create` 复制。

## Code style

模板内容本身要符合它所描述的规则——一份讲「用 ATX 标题、简洁段落」的模板如果自己不用 ATX 标题，就是自相矛盾的。

壳脚本沿用 `CODE_STYLE.md` 的 Shell 节：`#!/usr/bin/env bash`、`set -euo pipefail`、引号、退出码 `0/2/3`。

模板文件头注明来源与版本，因为本仓库的规则改了模板不会自动跟随：

```markdown
<!-- 源自 TaskFlow 1.1.11 的 CONTRIBUTING.md 的通用部分；不含 TaskFlow 自身的工作流 -->
```

## Testing strategy

全部离线，smoke 覆盖：

- **A1/A5** — 在无规则文件的夹具仓库里断言提醒文本出现且含缺失文件名；在三处之外的阶段断言不出现。
- **A2** — 同意后写入，`grep` 断言不含 `TaskFlowDocs/achieved`、不含 `capability`。
- **A3** — 拒绝后断言文件不存在；再次进入同一阶段断言提醒**仍然**出现（"每次都问"）。
- **A4** — 已有规则且含冲突条目的夹具，断言建议指向具体行号，且文件 `diff` 未变。
- **A6** — 提醒不改变任何命令的退出码。
- **A7** — 无网络的 PATH、无 `gh` 的 PATH 下，`show` 仍能打印。
- **A8** — 本仓库自身跑一遍，断言零提醒。

**变异验证**：每条断言都要能被"删掉对应分支"红化，逐个做并还原（`cmp` 确认字节一致）。

## Boundaries

- **Always**：先 `show` 再询问；用户同意后才 `create`；只带通用规则；已有文件视为用户所有。
- **Ask first**：新增触发点；把"每次都问"改成"问一次记住"；扩展模板内容。
- **Never**：未经同意写入用户仓库；覆盖或自动修改已有规则；生成 `ROADMAP.md`；让提醒变成阻塞。
