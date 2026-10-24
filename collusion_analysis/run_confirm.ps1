# C2 launcher: blocks idle sleep only while running (no settings changed), uses the real-environment
# Python (envw), then runs the pre-registered confirmatory replication.
Add-Type -Namespace Sprint -Name Power -MemberDefinition @'
[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);
'@
[void][Sprint.Power]::SetThreadExecutionState([uint32]2147483648 -bor [uint32]1)
Set-Location (Split-Path $PSScriptRoot -Parent)
if (Test-Path envw\Scripts\python.exe) { $env:PY = "envw/Scripts/python.exe" } else { throw "Run collusion_analysis\setup_realenv.ps1 first" }
Write-Host "[$(Get-Date -Format HH:mm)] C2 starting; sleep blocked while running. Leave the lid open." -ForegroundColor Cyan
try { & "C:\Program Files\Git\bin\bash.exe" collusion_analysis/run_confirm.sh }
finally { [void][Sprint.Power]::SetThreadExecutionState([uint32]2147483648); Write-Host "[$(Get-Date -Format HH:mm)] C2 finished." -ForegroundColor Cyan }
