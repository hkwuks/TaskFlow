# Plan — `task intake` inserts a new entry into the previous section instead of `## Items`

> Task version: v1
> Status: completed

No spec required — small, self-contained task.

## Reference Pointers

- `hooks/task` `intake` branch — the only production edit.
- `hooks/task` `remove` — how `## Removed` is placed; must stay compatible.
- `hooks/todo-check` `removed_at` (`sed -n '/^## Removed$/,/^## /p'`) — the
  reader the insertion must not poison.
- `TaskFlowDocs/todo.md` — `<!-- Add new items at the top … -->`.
- `hooks/smoke-test` — new section after the parallel-intake block.

## Related Tasks

- `TF-20260921-337ab8` — this task's Todo item.
- `TF-20260918-985164` — duplicate ID + false Removed record; **not fixed here**
  (data cleanup, separate).
- Promote title mismatch / Goal alignment — deferred per PRD Q1.

## Skills / Tools Used

- `Unaided — no capability applied to this phase; considered: shell/awk text
  processing, POSIX-portability references, and the repository's own hook
  conventions, all read directly.`

## Preconditions

- [x] Applicable repository documents and personal rules inspected;
  precedence/conflicts recorded. — `CONTRIBUTING.md`, `CODE_STYLE.md`,
  `TaskFlowDocs/todo.md`, `hooks/task`, `hooks/todo-check`, `hooks/smoke-test`
  read in this worktree.
- [x] Worktree isolation: `.worktrees/fix-todo-intake-insert` on
  `fix/todo-intake-insert` from `main` = `895e102`.

## Approval

- Status: approved
- Approved by: user
- Approved at: 2026-09-22
- Approved version: v1
- Approved scope: R1–R5; intake insertion only — no promote/title alignment
  (PRD Open Question 1), no new refusal path when Items is missing (Q2).

## Steps

### Step 1 — `intake` insertion index

- Goal: new block lands at top of `## Items` (R1), or just before
  `## Removed` when Items is missing (R2), or EOF only when neither exists
  (R3).
- Dependencies: none.
- Files: `hooks/task`.
- Implementation checklist:
  - [x] In the `intake` branch, compute an insertion line index instead of
        always emitting after `line[n]`.
  - [x] Scan for `^## Items` then skip blanks / one leading HTML comment;
        insert there. Else scan for `^## Removed`; insert there. Else keep
        current EOF path (rstrip + append).
  - [x] Keep Goal/ID duplicate checks, title derivation, and field template
        unchanged (R4) — fields now go through the shared `emit()` path.
  - [x] `bash -n hooks/task`.
- Acceptance: A, B, D.
- Verification: four manual fixtures (Items+trailing Removed; bare `# Todo`;
  no Items + Removed; Removed-above-first-entry). Order
  `Items < new < seed < Removed`; new ID absent from the `removed_at` range;
  Goal-derived `## <title>` written.
- Rollback: revert this commit; no other file depends on the index.
- Status: done

### Step 2 — smoke assertions

- Goal: a regression of the insertion point fails the suite (R5).
- Dependencies: Step 1.
- Files: `hooks/smoke-test`.
- Implementation checklist:
  - [x] Fixture with `## Items` + seed entry + trailing `## Removed`; intake;
        assert new heading is after `## Items` and before both the seed
        heading and `## Removed`.
  - [x] Assert new ID absent from the `removed_at` sed range.
  - [x] Bare `# Todo` still intakes (R3); no-Items+Removed lands before
        Removed (R2).
- Acceptance: C.
- Verification: one full `bash hooks/smoke-test` → `ALL SMOKE PASSED`.
- Rollback: drop the block; Step 1 still stands alone.
- Status: done

## Checkpoints

- After Step 1: manual fixtures + `bash -n` before touching smoke — done.
- After Step 2: one full `bash hooks/smoke-test` — done; no chained mutation
  runs; `pkill` confirmed 0 leftover processes.

## Verification / Review

| Check | Result |
|---|---|
| `bash -n hooks/task` | pass |
| `bash -n hooks/smoke-test` | pass |
| `bash hooks/smoke-test` | `ALL SMOKE PASSED` (rc=0) |
| `git diff --check` | clean |
| PRD reproduction fixture | order + removed-range + Goal title OK |
| No interpreter / bash 3.2 parse section | pass (suite) |

## Change Log

- v1 — approved and implemented; scope from `TF-20260921-337ab8` Notes
  (insertion point + Removed pollution + smoke acceptance). Title/promote
  alignment explicitly out of scope.

## Follow-ups

- `TF-20260918-985164` — remove the false tombstone / restore or cancel the
  live duplicate.
- `TF-20260921-4d8ae2` — close the stale inbox entry (fix already on
  `fix/repository-docs-reader`, merged via #46).
- Promote-title vs Goal — decide in the todo Notes' open question when that
  item is picked up.

## Version History

- v1 — planning.
- v1 — approved (user, 2026-09-22); Steps 1–2 done; suite green.

## Todo Record

Moved verbatim from the TODO entry by `hooks/archive`, grouped by the field each block followed.

### `- Notes:`

- **2026-09-21 用户指定：单独开一条。**
  **问题**：`hooks/task intake` 把新条目写进文件里的上一个 `## ` 节，而不是插到 `## Items` 下。新条目因此挂到别人的标题下——那次它挂在了「Stop `TaskFlowDocs/todo.md` from growing without bound…」节里，`promote` 又拿那行当标题生出 task 文档（本轮我用假标题「State in the Skill…」跑出了 plan/prd 的首行）。
  **另一半**：`intake` 的插入点固定在文件末尾，所以它落在 `## Removed` 之后；如果 `## Removed` 不是最后一节，新条目会插进 `## Removed` 节内，`todo-check` 读 `## Removed` 时会把在途条目当成已删除记录（该节与 `TF-20260918-985164` 的删除语义直接冲突）。
  **根因**：`hooks/task` 的 `intake` 分支（约 `:206-216`）是「rstrip 尾部空行 → 整文件原样输出 → 再追加 `## <title>` 块」，没有定位 `## Items` 边界，也没有插入点概念。
  **违反的既有约定**：`TaskFlowDocs/todo.md` 自己的 `## Items` 节里写着 `<!-- Add new items at the top using the template below. -->`——实现与文档约定相反。
  **判定依据**：`hooks/task get <todo-id>` 与 `hooks/task next <todo-id> … [notes]` 能只读/只改一条条目（`next` 的第三个位置参数就是 Notes），所以本次是「用 hook 写 Notes」而非手改——这正是 `task next` 存在的理由。
  **验收**：新条目落在 `## Items` 节内、位于任何其他 `## ` 节之前；`## Removed` 之后插入新条目不再可能污染删除记录；`todo-check` 的 removed 判定不受影响；smoke 增加一条断言（新条目不得出现在 `## Removed` 与文件末尾之间）。相关：本轮 PR #45 里我被这个 bug 误导，绕过后才 promote 成功。
  **同因的另一现象**：`## ` 标题与 Goal 对不齐是既有习惯，不是个别错误——本文件的 `## ` 节数比 `- ID:` 行数多 23，多出来的全是模板块（`## T-YYYYMMDD-001` 等），另有约 30 条已交付条目的标题是手写摘要、与 Goal 前缀不一致。`hooks/task get` 按 ID、`findsec` 按 `TaskFlowDocs/<task>/` 解析条目，都不看标题，所以目前只是可读性问题；唯一出错的是 `promote`——它用标题去派生任务目录名。口径待定：标题由 Goal 派生（与 intake 一致、可校验），还是保留人写标题但 `promote` 一并更新它。
