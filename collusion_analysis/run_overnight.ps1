# Overnight launcher (sprint): keeps Windows from idle-sleeping only while the run is going
# (SetThreadExecutionState, the same request media players make; no power settings are changed),
# then runs the unattended pipeline with the $40 budget settings logged in SPRINT_PROTOCOL.md.
# A closed lid or a manual Sleep still sleeps the machine.
Add-Type -Namespace Sprint -Name Power -MemberDefinition @'
[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS = [uint32]2147483648; $ES_SYSTEM_REQUIRED = [uint32]1
[void][Sprint.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED)
Write-Host "[$(Get-Date -Format HH:mm)] Sleep blocked while the run is going. Leave the lid open." -ForegroundColor Cyan

Set-Location (Split-Path $PSScriptRoot -Parent)
$env:BUDGET_USD = "39"; $env:K_J = "3"; $env:N_G = "3"
$bash = "C:\Program Files\Git\bin\bash.exe"
try {
    & $bash collusion_analysis/run_all.sh
} finally {
    [void][Sprint.Power]::SetThreadExecutionState($ES_CONTINUOUS)
    Write-Host "[$(Get-Date -Format HH:mm)] Run finished; normal sleep restored. Start with WRITING_PACK.md" -ForegroundColor Cyan
}
