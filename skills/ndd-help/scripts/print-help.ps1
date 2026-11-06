# Print the shared reference without invoking an agent. PowerShell 5.1+ / 7+.
$ErrorActionPreference = 'Stop'
$helpFile = Join-Path $PSScriptRoot '../assets/help.md'
$versionFile = Join-Path $PSScriptRoot '../../ndd-setup/VERSION'
try {
    $helpText = Get-Content -LiteralPath $helpFile -Raw -Encoding UTF8
} catch {
    throw "Help text missing or unreadable: $helpFile. $_"
}
$version = ''
try {
    $version = (Get-Content -LiteralPath $versionFile -Raw -Encoding UTF8).Trim()
} catch {
    # An incomplete version file must not prevent the reference from being shown.
    $version = ''
}
if ($version -notmatch '^[0-9]+\.[0-9]+\.[0-9]+$') {
    $version = 'version unavailable ' + [char]0x2014 + ' incomplete installation'
}
[Console]::OutputEncoding = New-Object Text.UTF8Encoding($false)
[Console]::Write($helpText.Replace('{{VERSION}}', $version))
