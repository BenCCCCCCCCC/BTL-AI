param([switch]$Legacy)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $repoRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw 'Repository Python environment is missing. See docs/07_HANDOFF.md.'
}
Push-Location -LiteralPath $repoRoot
try {
    $storyModule = if ($Legacy) { 'ai.prototype.story_desktop' } else { 'ai.prototype.chapter_desktop' }
    & $pythonPath -m $storyModule
    if ($LASTEXITCODE -ne 0) { throw "Story window exited with code $LASTEXITCODE." }
} finally {
    Pop-Location
}
