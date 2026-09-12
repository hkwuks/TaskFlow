: << 'CMDBLOCK'
@echo off
setlocal EnableDelayedExpansion
REM Cross-platform polyglot wrapper for TaskFlow hook scripts.
REM On Windows: cmd.exe runs the batch portion, which finds and calls bash.
REM On Unix: the shell interprets this as a script (: is a no-op in bash).
REM
REM Hook scripts are extensionless bash (e.g. "session-start", "summarize-state")
REM so Claude Code's Windows auto-detection -- which prepends "bash" to any
REM command containing ".sh" -- doesn't interfere. Pattern from
REM obra/superpowers/hooks/run-hook.cmd.
REM
REM Usage: run-hook.cmd <script-name> [args...]

if "%~1"=="" (
    echo run-hook.cmd: missing script name >&2
    exit /b 1
)

set "HOOK_DIR=%~dp0"
set "GIT_BASH="

REM Try Git for Windows bash in standard locations
if exist "C:\Program Files\Git\bin\bash.exe" (
    "C:\Program Files\Git\bin\bash.exe" "%~f0" %*
    exit /b !ERRORLEVEL!
)
if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
    "C:\Program Files (x86)\Git\bin\bash.exe" "%~f0" %*
    exit /b !ERRORLEVEL!
)

REM Find Git Bash beside the Git for Windows installation, including non-default drives.
for /f "delims=" %%G in ('where git 2^>nul') do (
    if not defined GIT_BASH if exist "%%~dpG..\bin\bash.exe" set "GIT_BASH=%%~dpG..\bin\bash.exe"
    if not defined GIT_BASH if exist "%%~dpG..\usr\bin\bash.exe" set "GIT_BASH=%%~dpG..\usr\bin\bash.exe"
)
if defined GIT_BASH (
    "%GIT_BASH%" "%~f0" %*
    exit /b !ERRORLEVEL!
)

REM Accept another PATH bash, but never Windows' WSL launchers.
for /f "delims=" %%B in ('where bash 2^>nul') do (
    if not defined GIT_BASH if /I not "%%~fB"=="%SystemRoot%\System32\bash.exe" if /I not "%%~fB"=="%LOCALAPPDATA%\Microsoft\WindowsApps\bash.exe" set "GIT_BASH=%%~fB"
)
if defined GIT_BASH (
    "%GIT_BASH%" "%~f0" %*
    exit /b !ERRORLEVEL!
)

REM A configured hook that cannot run must fail visibly; silent success hides a broken install.
echo run-hook.cmd: Git for Windows Bash not found >&2
exit /b 1
CMDBLOCK

# Unix: run the named script directly
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_NAME="$1"
shift
exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
