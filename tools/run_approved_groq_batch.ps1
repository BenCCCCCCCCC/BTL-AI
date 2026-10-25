# Run only the batch in an explicitly authorised sheet. No persistent key storage.
[CmdletBinding()]
param([string]$AuthorizationFile = '')

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$sheetPath = Join-Path $repoRoot 'ai/eval/free_baseline_authorization.experimental.v0.1.json'
if ($AuthorizationFile) { $sheetPath = (Resolve-Path -LiteralPath $AuthorizationFile).Path }
$pythonPath = Join-Path $repoRoot '.venv/Scripts/python.exe'
$sheet = Get-Content -Raw -LiteralPath $sheetPath | ConvertFrom-Json

if (-not $sheet.execution_authorized -or $sheet.authorization_status -ne 'AUTHORIZED') {
    throw "This batch is not open for execution (status: $($sheet.authorization_status))."
}
if (Test-Path -LiteralPath (Join-Path $repoRoot $sheet.output_path)) {
    throw 'Batch output already exists. Preserve it and review completed cases before running again.'
}
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'The repository Python environment is missing.'
}

Write-Host "Approved batch: Groq $($sheet.model); $($sheet.case_ids.Count) cases; at most $($sheet.max_generation_requests) requests; USD $($sheet.budget_usd)."
Write-Host 'Check the Groq account is on Free tier. Do not upgrade or add billing for this batch.'
if (-not $sheet.free_tier_confirmed) {
    $tier = Read-Host 'Type FREE after checking the account tier (anything else stops)'
    if ($tier -cne 'FREE') { throw 'Free tier has not been confirmed. No request was made.' }
    $sheet.free_tier_confirmed = $true
    $sheet | Add-Member -NotePropertyName free_tier_confirmation_source -NotePropertyValue 'User typed FREE in the local launcher' -Force
    $sheetJson = $sheet | ConvertTo-Json -Depth 10
    [IO.File]::WriteAllText($sheetPath, $sheetJson + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
}

$secureKey = Read-Host 'Paste the Groq API key (hidden; used only for this run)' -AsSecureString
$previousKey = [Environment]::GetEnvironmentVariable('GROQ_API_KEY', 'Process')
$previousEncoding = [Environment]::GetEnvironmentVariable('PYTHONIOENCODING', 'Process')
$batchExit = 1
Push-Location -LiteralPath $repoRoot
try {
    $env:GROQ_API_KEY = [Net.NetworkCredential]::new('', $secureKey).Password
    $env:PYTHONIOENCODING = 'utf-8'
    & $pythonPath -m ai.prototype.baseline --adapter groq --authorization $sheetPath
    $batchExit = $LASTEXITCODE
} finally {
    [Environment]::SetEnvironmentVariable('GROQ_API_KEY', $previousKey, 'Process')
    [Environment]::SetEnvironmentVariable('PYTHONIOENCODING', $previousEncoding, 'Process')
    $secureKey.Dispose()
    Pop-Location
}
exit $batchExit
