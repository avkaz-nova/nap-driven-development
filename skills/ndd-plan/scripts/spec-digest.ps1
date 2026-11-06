# PowerShell 5.1+/7+. Same canonical bytes as spec-digest.sh.
[CmdletBinding()]
param([Parameter(Mandatory=$true, Position=0)][string]$Path)
$ErrorActionPreference = 'Stop'
$text = [IO.File]::ReadAllText((Resolve-Path -LiteralPath $Path).Path)
$text = $text.TrimStart([char]0xFEFF).Replace("`r`n", "`n")
$lines = $text.Split([char]10)
if ($lines[0] -ne '---') { throw 'Missing YAML frontmatter.' }
$end = -1
for ($i = 1; $i -lt $lines.Length; $i++) { if ($lines[$i] -eq '---') { $end=$i; break } }
if ($end -lt 0 -or $end -eq $lines.Length - 1) { throw 'Missing Markdown body.' }
$body = ($lines[($end + 1)..($lines.Length - 1)] -join "`n").TrimEnd([char]10)
if ($body.Length -eq 0) { throw 'Empty Markdown body.' }
$sha = [Security.Cryptography.SHA256]::Create()
try {
    $bytes = [Text.Encoding]::UTF8.GetBytes($body + "`n")
    ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
} finally { $sha.Dispose() }
