param([string]$Root)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$createdRoot = -not $Root
if ($createdRoot) {
    $chinese = [string]([char]0x4E2D) + [char]0x6587
    $Root = Join-Path ([IO.Path]::GetTempPath()) ("TaskFlow Windows $chinese " + [guid]::NewGuid())
}

function Invoke-TaskFlow {
    param([string[]]$Arguments, [switch]$MustFail)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $output = & "$here\run-hook.cmd" task @Arguments 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $oldPreference
    if ($MustFail -and $exitCode -eq 0) { throw "Expected failure: $($Arguments -join ' ')" }
    if (-not $MustFail -and $exitCode -ne 0) { throw "Command failed: $($Arguments -join ' '): $output" }
}

function Invoke-SessionStart {
    param([string]$Phase)
    $oldRoot = $env:TASKFLOW_REPO_ROOT
    $oldPhase = $env:TASKFLOW_PHASE
    $oldClaudeRoot = $env:CLAUDE_PLUGIN_ROOT
    try {
        $env:TASKFLOW_REPO_ROOT = $Root
        $env:TASKFLOW_PHASE = $Phase
        $env:CLAUDE_PLUGIN_ROOT = Split-Path -Parent $here
        $output = & "$here\run-hook.cmd" session-start 2>&1
        if ($LASTEXITCODE -ne 0) { throw "SessionStart failed: $output" }
        return (($output -join [Environment]::NewLine) | ConvertFrom-Json)
    }
    finally {
        $env:TASKFLOW_REPO_ROOT = $oldRoot
        $env:TASKFLOW_PHASE = $oldPhase
        $env:CLAUDE_PLUGIN_ROOT = $oldClaudeRoot
    }
}

try {
    $launcherArgs = @('space value', ([string]([char]0x4E2D) + [char]0x6587), 'quoted value', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
    $launcherOutput = @(& "$here\run-hook.cmd" smoke-test --echo-args @launcherArgs 2>&1)
    if ($LASTEXITCODE -ne 0) { throw "Launcher argument check failed: $launcherOutput" }
    $expected = (($launcherArgs | ForEach-Object { "<$_>" }) -join '|') + '|'
    $actual = ($launcherOutput -join '').Replace("`r", '').Replace("`n", '').Trim()
    $tokens = @($actual -split '\|' | Where-Object { $_ })
    if ($tokens.Count -ne $launcherArgs.Count) { throw "Launcher argument count changed: $launcherOutput" }
    for ($i = 0; $i -lt $launcherArgs.Count; $i++) {
        $expectedToken = '<' + ([BitConverter]::ToString([Text.Encoding]::UTF8.GetBytes([string]$launcherArgs[$i])).Replace('-', '').ToLowerInvariant()) + '>'
        if ($tokens[$i].Trim() -ne $expectedToken) { throw "Launcher argument $i changed: $launcherOutput" }
    }
    'WINDOWS LAUNCHER ARGS PASSED'

    New-Item -ItemType Directory -Path $Root | Out-Null
    $common = @('--root', $Root)
    $goal = 'Windows ' + [char]0x5B8C + [char]0x6574 + [char]0x751F + [char]0x547D + [char]0x5468 + [char]0x671F + '.'
    Invoke-TaskFlow (@('intake', $goal, 'PowerShell 5.1 fixture') + $common)
    $todo = Join-Path $Root 'TaskFlowDocs\todo.md'
    # The suffix is a hex digest of the goal, not a counter, so this must accept
    # both hex digits and any future letter case.
    $todoId = ([regex]::Match([IO.File]::ReadAllText($todo), '(?m)^- ID: (TF-\d{8}-[0-9a-f]{6})$')).Groups[1].Value
    if (-not $todoId) { throw 'Todo ID missing' }
    if ([IO.File]::ReadAllText($todo) -notmatch [regex]::Escape($goal)) { throw 'Unicode goal was not preserved' }

    Invoke-TaskFlow (@('intake', $goal, 'PowerShell 5.1 fixture') + $common) -MustFail
    Invoke-TaskFlow (@('promote', $todoId, '2026-09-11-windows-smoke', 'small') + $common)
    $task = Join-Path $Root 'TaskFlowDocs\2026-09-11-windows-smoke'
    $plan = Join-Path $task 'plan.md'

    Invoke-TaskFlow (@('state', '2026-09-11-windows-smoke', 'in_progress') + $common) -MustFail
    $utf8 = New-Object Text.UTF8Encoding($false)
    # The approval gate reads the approver as well as the version: the template
    # ships `pending` in every Approval field, so a version match alone still
    # admits an unapproved task. `progress` and `complete` use the same gate as
    # `state in_progress`, which is why this fixture has to record a real one.
    $text = [IO.File]::ReadAllText($plan).Replace('- Status: requested', '- Status: approved').Replace('- Approved by: pending', '- Approved by: user').Replace('- Approved version: pending', '- Approved version: v1')
    [IO.File]::WriteAllText($plan, $text, $utf8)
    Invoke-TaskFlow (@('state', '2026-09-11-windows-smoke', 'in_progress') + $common)
    Invoke-TaskFlow (@('progress', '2026-09-11-windows-smoke', '1', 'done') + $common) -MustFail

    $text = [IO.File]::ReadAllText($plan).Replace('- [ ]', '- [x]')
    [IO.File]::WriteAllText($plan, $text, $utf8)
    $verification = 'Windows Unicode path verification'
    Invoke-TaskFlow (@('progress', '2026-09-11-windows-smoke', '1', 'done', $verification) + $common)
    Invoke-TaskFlow (@('complete', '2026-09-11-windows-smoke') + $common) -MustFail
    Invoke-TaskFlow (@('complete', '2026-09-11-windows-smoke', '--user-accepted') + $common)

    $achieved = Join-Path $Root 'TaskFlowDocs\achieved\2026-09-11-windows-smoke'
    if (Test-Path $task) { throw 'Active task still exists' }
    if (-not (Test-Path $achieved)) { throw 'Achieved task missing' }
    if ([IO.File]::ReadAllText($todo) -notmatch '(?m)^- Status: done\r?$') { throw 'Todo is not done' }

    [IO.File]::WriteAllText((Join-Path $Root 'CONTRIBUTING.md'), "# Contributing`n", $utf8)
    $first = Invoke-SessionStart 'pr'
    $index = Join-Path $Root 'TaskFlowDocs\repository-docs\index.md'
    if (-not (Test-Path $index)) { throw 'SessionStart did not create repository-docs index' }
    $context = $first.hookSpecificOutput.additionalContext
    if ($context -notmatch 'Repository document routes \(pr\)') { throw 'PR phase route missing from SessionStart JSON' }
    if ($context -notmatch 'CONTRIBUTING\.md') { throw 'Applicable source missing from SessionStart JSON' }
    if ([IO.File]::ReadAllText($index) -notmatch '\| repository-rule \| `CONTRIBUTING\.md` \| design,code,commit,pr,release \| yes \|') { throw 'Index did not record existing source' }
    $before = (Get-FileHash -Algorithm SHA256 -LiteralPath $index).Hash
    $second = Invoke-SessionStart 'pr'
    $after = (Get-FileHash -Algorithm SHA256 -LiteralPath $index).Hash
    if ($before -ne $after) { throw 'Repeated SessionStart changed an up-to-date index' }
    if ($second.hookSpecificOutput.additionalContext -notmatch 'Read routing record first') { throw 'Repeated SessionStart context missing' }
    'WINDOWS SESSIONSTART PASSED'
    'WINDOWS LIFECYCLE PASSED'

    # The pre-write gate, driven through the same launcher, on a repository path
    # that carries both a space and Chinese characters — the two things the
    # launcher exists for. It needs a real Git repository because the gate
    # resolves its store with `git -C` on the target file's own directory, and
    # the event carries a forward-slash drive path, which is what Claude Code
    # reports on Windows.
    $gateRepo = Join-Path $Root 'gate repo'
    $gateTask = Join-Path $gateRepo 'TaskFlowDocs\2026-09-11-gate'
    New-Item -ItemType Directory -Path $gateTask -Force | Out-Null
    & git -C $gateRepo init -q 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'gate fixture git init failed' }
    [IO.File]::WriteAllText((Join-Path $gateTask 'plan.md'), "# Plan`n> Task version: v1`n> Status: planning`n", $utf8)

    # The event goes through a file and a `cmd` redirect rather than the
    # PowerShell pipeline. PowerShell 5.1 encodes a piped string with a UTF-8 BOM,
    # and the hook reads the event as JSON, where a leading BOM is not whitespace
    # — the hook would no-op and the test would prove nothing about it. A file
    # written without a BOM is the bytes a host actually sends.
    function Invoke-Hook {
        param([string]$Hook, [string]$Event)
        $eventFile = Join-Path $gateRepo 'event.json'
        [IO.File]::WriteAllText($eventFile, $Event, $utf8)
        $oldPreference = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'
        $out = & cmd /c "`"$here\run-hook.cmd`" $Hook < `"$eventFile`"" 2>&1
        $code = $LASTEXITCODE
        $ErrorActionPreference = $oldPreference
        Remove-Item -LiteralPath $eventFile -Force
        return [pscustomobject]@{ Output = ($out -join "`n"); Exit = $code }
    }

    $gateRepoUrl = $gateRepo.Replace('\', '/')
    $prdEvent = '{"hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"file_path":"' + (Join-Path $gateTask 'prd.md').Replace('\', '/') + '"}}'

    $verdict = Invoke-Hook 'capability-gate' $prdEvent
    if ($verdict.Exit -ne 0) { throw "capability-gate exited $($verdict.Exit): $($verdict.Output)" }
    if ($verdict.Output -notmatch '"permissionDecision":"deny"') { throw "gate did not deny an unreleased stage: $($verdict.Output)" }
    if ($verdict.Output -notmatch 'task unaided PRD --considered') { throw 'gate deny message omits the escape command' }

    $skillEvent = '{"hook_event_name":"PostToolUse","tool_name":"Skill","cwd":"' + $gateRepoUrl + '","tool_input":{"skill":"windows:cap"}}'
    $verdict = Invoke-Hook 'capability-evidence' $skillEvent
    if ($verdict.Exit -ne 0) { throw "capability-evidence exited $($verdict.Exit): $($verdict.Output)" }
    $verdict = Invoke-Hook 'capability-gate' $prdEvent
    if ($verdict.Output -match '"permissionDecision":"deny"') { throw 'gate denied a stage that had a real invocation' }

    # One invocation is spent by one stage, and the escape hatch is a real command
    # that has to work on this host too.
    $specEvent = '{"hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"' + (Join-Path $gateTask 'spec.md').Replace('\', '/') + '"}}'
    $verdict = Invoke-Hook 'capability-gate' $specEvent
    if ($verdict.Output -notmatch '"permissionDecision":"deny"') { throw 'gate released a second stage on spent evidence' }
    Invoke-TaskFlow (@('unaided', 'Spec', '--considered', 'architecture and design') + @('--root', $gateRepo))
    $verdict = Invoke-Hook 'capability-gate' $specEvent
    if ($verdict.Output -match '"permissionDecision":"deny"') { throw 'gate denied a stage the escape hatch had released' }
    'WINDOWS PRE-WRITE GATE PASSED'
}
finally {
    if ($createdRoot -and (Test-Path $Root)) { Remove-Item -LiteralPath $Root -Recurse -Force }
}
