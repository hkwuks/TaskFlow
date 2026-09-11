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

try {
    New-Item -ItemType Directory -Path $Root | Out-Null
    $common = @('--root', $Root)
    $goal = 'Windows ' + [char]0x5B8C + [char]0x6574 + [char]0x751F + [char]0x547D + [char]0x5468 + [char]0x671F + '.'
    Invoke-TaskFlow (@('intake', $goal, 'PowerShell 5.1 fixture') + $common)
    $todo = Join-Path $Root 'TaskFlowDocs\todo.md'
    $todoId = ([regex]::Match([IO.File]::ReadAllText($todo), '(?m)^- ID: (TF-\d+-\d+)$')).Groups[1].Value
    if (-not $todoId) { throw 'Todo ID missing' }
    if ([IO.File]::ReadAllText($todo) -notmatch [regex]::Escape($goal)) { throw 'Unicode goal was not preserved' }

    Invoke-TaskFlow (@('intake', $goal, 'PowerShell 5.1 fixture') + $common) -MustFail
    Invoke-TaskFlow (@('promote', $todoId, '2026-09-11-windows-smoke', 'small') + $common)
    $task = Join-Path $Root 'TaskFlowDocs\2026-09-11-windows-smoke'
    $plan = Join-Path $task 'plan.md'

    Invoke-TaskFlow (@('state', '2026-09-11-windows-smoke', 'in_progress') + $common) -MustFail
    $utf8 = New-Object Text.UTF8Encoding($false)
    $text = [IO.File]::ReadAllText($plan).Replace('- Status: requested', '- Status: approved').Replace('- Approved version: pending', '- Approved version: v1')
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
    'WINDOWS LIFECYCLE PASSED'
}
finally {
    if ($createdRoot -and (Test-Path $Root)) { Remove-Item -LiteralPath $Root -Recurse -Force }
}
