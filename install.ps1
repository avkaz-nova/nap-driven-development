<#
.SYNOPSIS
Install NDD for Claude Code and/or Codex. PowerShell 5.1+ / 7+ on Windows.
.DESCRIPTION
Receipts are stored beside each skills directory in <directory>.ndd-kit.
Existing NDD skills, including local edits, are replaced automatically.
Successful installs retain no backups. Use -DryRun to preview.
-Replace is accepted for compatibility; replacement is automatic.
Uninstall permanently deletes owned skills and all NDD install state, without backups.
With both agents selected, it also removes this verified clean NDD clone unless -KeepSource is set.
#>
[CmdletBinding()]
param(
    [switch]$Claude, [switch]$Codex, [switch]$All,
    [switch]$Link, [switch]$Uninstall, [switch]$DryRun, [switch]$Replace, [switch]$KeepSource,
    [string]$ClaudeDir, [string]$CodexDir
)
$ErrorActionPreference = 'Stop'
$KitDir = $PSScriptRoot
if ($KitDir -match '[\r\n\t]') { throw 'The distribution path must not contain tabs or line breaks.' }
$Names = @('ndd-setup', 'ndd-spec', 'ndd-plan', 'ndd-do', 'ndd-help', 'ndd-review')
$UserDirectory = [Environment]::GetFolderPath('UserProfile')
function Clear-RegisteredProjects([switch]$Preview) {
    $helper = Join-Path $KitDir 'skills/ndd-setup/scripts/project-registry.ps1'
    $stateDir = if ($env:NDD_STATE_DIR) { $env:NDD_STATE_DIR } else { Join-Path $UserDirectory '.ndd' }
    if (Test-Path -LiteralPath $helper -PathType Leaf) {
        try { & $helper -Action Cleanup -DryRun:$Preview }
        catch { Write-Warning "Project cleanup was skipped or incomplete; continuing NDD removal. Registry retained at $stateDir/projects. $_" }
    } elseif ((Get-Item -LiteralPath (Join-Path $stateDir 'projects') -Force -ErrorAction SilentlyContinue) -or
              (Get-Item -LiteralPath (Join-Path $stateDir '.projects.lock') -Force -ErrorAction SilentlyContinue)) {
        Write-Warning "Project cleanup helper is missing; continuing NDD removal. Registry retained at $stateDir/projects."
    }
}
if ($ClaudeDir) { $Claude = $true }
else {
    $configDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $UserDirectory '.claude' }
    $ClaudeDir = Join-Path $configDir 'skills'
}
if ($CodexDir) { $Codex = $true }
else { $CodexDir = Join-Path $UserDirectory '.agents\skills' }
if ($All) { $Claude = $true; $Codex = $true }
if ($Uninstall -and ($Replace -or $Link)) { throw '-Replace and -Link are install-only options.' }
if ($KeepSource -and -not $Uninstall) { throw '-KeepSource requires -Uninstall.' }
if (-not $Claude -and -not $Codex) {
    if (Test-Path -LiteralPath (Split-Path $ClaudeDir -Parent)) { $Claude = $true }
    $codexHomeDir = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $UserDirectory '.codex' }
    if ((Test-Path -LiteralPath $codexHomeDir) -or (Test-Path -LiteralPath (Split-Path $CodexDir -Parent))) { $Codex = $true }
}
if (-not $Claude -and -not $Codex) { throw 'No agent detected. Select -Claude, -Codex, or -All.' }
$Targets = @()
if ($Claude) { $Targets += $ClaudeDir }
if ($Codex) { $Targets += $CodexDir }

function Get-Entry([string]$Path) {
    # Unlike Test-Path alone, enumerating the parent also finds broken links.
    $parent = Split-Path $Path -Parent
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) { return $null }
    $leaf = Split-Path $Path -Leaf
    return Get-ChildItem -LiteralPath $parent -Force | Where-Object { $_.Name -eq $leaf } | Select-Object -First 1
}
function Test-Link($Item) {
    return $null -ne $Item -and ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)
}
function Get-TextHash([string]$Text) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($Text)))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function Get-Fingerprint([string]$Path) {
    $root = [IO.Path]::GetFullPath($Path).TrimEnd('\', '/')
    $lines = New-Object 'System.Collections.Generic.List[string]'
    # Walk explicitly: reject links before recursion, including on PowerShell 5.1.
    $pending = New-Object 'System.Collections.Generic.Stack[string]'
    $pending.Push($root)
    while ($pending.Count -gt 0) {
        foreach ($item in Get-ChildItem -LiteralPath $pending.Pop() -Force) {
            if (Test-Link $item) { throw "Linked entry cannot be fingerprinted: $($item.FullName)" }
            $relative = './' + $item.FullName.Substring($root.Length + 1).Replace('\', '/')
            if ($relative.Contains("`n") -or $relative.Contains("`r") -or $relative.Contains("`t")) { throw "Unsupported filename: $relative" }
            if ($item.PSIsContainer) { $lines.Add("D`t$relative"); $pending.Push($item.FullName) }
            else {
                $digest = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                $lines.Add("F`t$digest`t$relative")
            }
        }
    }
    # Receipt fingerprints are platform-local; copied content is verified on the same host.
    $lines.Sort([StringComparer]::Ordinal)
    $text = if ($lines.Count) { ($lines -join "`n") + "`n" } else { '' }
    return Get-TextHash $text
}
function Test-OwnedReceipt([string]$Receipt) {
    $record = Get-Entry $Receipt
    if (-not $record -or $record.PSIsContainer -or (Test-Link $record)) { return $false }
    $lines = @(Get-Content -LiteralPath $Receipt -Encoding UTF8)
    return $lines.Count -eq 5 -and $lines[0] -eq 'ndd-kit-install-v1' -and $lines[2] -in @('copy', 'link')
}
function Assert-DirectoryPath([string]$Path) {
    if (-not [IO.Path]::IsPathRooted($Path) -or $Path -match '[\r\n\t]') { throw "Use an absolute path: $Path" }
    $current = [IO.Path]::GetFullPath($Path)
    if ($current.TrimEnd('\', '/') -eq [IO.Path]::GetPathRoot($current).TrimEnd('\', '/')) { throw 'Cannot use a filesystem root as a skills directory.' }
    while ($current -and $current -ne [IO.Path]::GetPathRoot($current)) {
        $entry = Get-Entry $current
        if ($entry -and ((Test-Link $entry) -or -not $entry.PSIsContainer)) { throw "Destination parent must be a real directory: $current" }
        $current = Split-Path $current -Parent
    }
}
function Remove-NddEntry([string]$Path) {
    $entry = Get-Entry $Path
    if (-not $entry) { return }
    # Never recurse through a junction/symlink, including one inside an old backup.
    if (Test-Link $entry) {
        if ($entry.Attributes -band [IO.FileAttributes]::Directory) { [IO.Directory]::Delete($Path) }
        else { [IO.File]::Delete($Path) }
    } elseif ($entry.PSIsContainer) {
        foreach ($child in Get-ChildItem -LiteralPath $Path -Force) { Remove-NddEntry $child.FullName }
        [IO.Directory]::Delete($Path)
    } else { Remove-Item -LiteralPath $Path -Force }
}

# Only this script's standalone clone is eligible; never follow receipt paths.
function Get-SourceRetentionReason {
    if ($KeepSource) { return '-KeepSource requested' }
    if (-not $Claude -or -not $Codex) { return 'select both agents (-All) to remove the clone' }
    if ($KitDir -eq $UserDirectory) { return 'source is the user home directory' }
    try { Assert-DirectoryPath $KitDir }
    catch { return 'source is a protected or redirected directory' }
    $gitDir = Join-Path $KitDir '.git'
    $entry = Get-Entry $gitDir
    if (-not $entry -or -not $entry.PSIsContainer -or (Test-Link $entry)) {
        return 'not a standalone Git clone (ZIPs and linked worktrees are kept)'
    }
    if (-not (Get-Command git -CommandType Application -ErrorAction SilentlyContinue)) {
        return 'Git is unavailable; source could not be verified'
    }
    $gitArgs = @('--no-optional-locks', '-c', 'core.fsmonitor=false', "--git-dir=$gitDir", "--work-tree=$KitDir")
    try {
        $origin = @(& git @gitArgs config --local --no-includes --get remote.origin.url 2>$null)
        if ($LASTEXITCODE -ne 0 -or $origin.Count -ne 1) { return 'could not verify the source repository' }
        if ($origin[0] -cnotin @('https://github.com/avkaz/nap-driven-development',
                'https://github.com/avkaz/nap-driven-development.git',
                'git@github.com:avkaz/nap-driven-development.git',
                'ssh://git@github.com/avkaz/nap-driven-development.git')) {
            return 'origin is not the NDD repository'
        }
        if (Test-Path -LiteralPath (Join-Path $gitDir 'worktrees')) { return 'clone has linked worktree metadata' }
        $entries = @(& git @gitArgs ls-files -v 2>$null)
        if ($LASTEXITCODE -ne 0) { return 'could not verify the source index' }
        if (@($entries | Where-Object { $_ -cmatch '^[a-zS] ' }).Count) {
            return 'source index can hide changes (assume-unchanged or skip-worktree)'
        }
        $changes = @(& git @gitArgs status --porcelain=v1 --untracked-files=all --ignored --ignore-submodules=none 2>$null)
        if ($LASTEXITCODE -ne 0) { return 'could not check local source changes' }
        if ($changes.Count) { return 'clone contains local changes, untracked or ignored files' }
        $commits = @(& git @gitArgs rev-list --max-count=1 HEAD --all --reflog --not --remotes 2>$null)
        if ($LASTEXITCODE -ne 0) { return 'could not check unpublished source commits' }
        if ($commits.Count) { return 'clone contains history not present in local remote-tracking refs' }
    } catch { return 'Git source verification failed' }
    return ''
}

$Version = 'unknown'
if (-not $Uninstall) {
    $Version = (Get-Content -LiteralPath (Join-Path $KitDir 'skills\ndd-setup\VERSION') -Raw).Trim()
    if ($Version -notmatch '^\d+\.\d+\.\d+$') { throw 'Invalid VERSION.' }
    foreach ($name in $Names) {
        $source = Join-Path $KitDir "skills\$name"
        foreach ($file in @('SKILL.md', 'agents\openai.yaml')) {
            if (-not (Test-Path -LiteralPath (Join-Path $source $file) -PathType Leaf)) { throw "Incomplete distribution: $name/$file" }
        }
        if (Test-Link (Get-Entry $source)) { throw "Source must be a real directory: $source" }
        $null = Get-Fingerprint $source
    }
    foreach ($asset in @('spec.md', 'plan.md')) {
        if (-not (Test-Path -LiteralPath (Join-Path $KitDir "skills\ndd-setup\assets\$asset") -PathType Leaf)) { throw "Missing asset: $asset" }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $KitDir 'skills/ndd-help/assets/help.md') -PathType Leaf)) { throw 'Missing help resource: assets/help.md' }
    foreach ($resource in @('assets/review.md', 'references/report-updates.md')) {
        if (-not (Test-Path -LiteralPath (Join-Path $KitDir "skills/ndd-review/$resource") -PathType Leaf)) { throw "Missing review resource: $resource" }
    }
}
foreach ($target in $Targets) {
    if (-not [IO.Path]::IsPathRooted($target)) { throw "Use an absolute path: $target" }
}
$Targets = @($Targets | ForEach-Object { [IO.Path]::GetFullPath($_).TrimEnd('\', '/') })
if (@($Targets | Select-Object -Unique).Count -ne $Targets.Count) { throw 'Targets must be distinct.' }
foreach ($target in $Targets) {
    Assert-DirectoryPath $target
    Assert-DirectoryPath "$target.ndd-kit"
    if (-not $Uninstall) { Assert-DirectoryPath (Join-Path "$target.ndd-kit" 'backups') }
    $comparison = [StringComparison]::OrdinalIgnoreCase
    $separator = [IO.Path]::DirectorySeparatorChar
    if (($target + $separator).StartsWith($KitDir.TrimEnd('\', '/') + $separator, $comparison)) { throw 'Cannot install inside the distribution.' }
    foreach ($name in $Names) {
        if (($KitDir + $separator).StartsWith((Join-Path $target $name) + $separator, $comparison)) { throw 'Distribution overlaps the installation destination.' }
    }
    if (($KitDir + $separator).StartsWith("$target.ndd-kit" + $separator, $comparison)) { throw 'Distribution overlaps installation metadata.' }
    foreach ($other in $Targets) {
        if ($other -eq $target) { continue }
        if (($target + $separator).StartsWith($other + $separator, $comparison) -or
            ($target + $separator).StartsWith("$other.ndd-kit" + $separator, $comparison)) { throw 'Targets must not overlap.' }
    }
    Write-Host "Target: $target"
    foreach ($name in $Names) {
        $dest = Join-Path $target $name
        $record = Join-Path "$target.ndd-kit" "$name.receipt"
        $entry = Get-Entry $record
        if ($entry -and ($entry.PSIsContainer -or (Test-Link $entry))) { throw "Invalid receipt: $record" }
        if ($Uninstall) {
            if ((Get-Entry $dest) -and -not (Test-OwnedReceipt $record)) { throw "Cannot establish NDD ownership: $dest. No files removed." }
            Write-Host "  Permanently remove if present (including local edits): $name"
        } elseif (Get-Entry $dest) {
            Write-Host "  Replace (including local edits; no retained backup): $name"
        } else {
            $mode = if ($Link) { 'link' } else { 'copy' }
            Write-Host "  Install $Version ($mode): $name"
        }
    }
    if ($Uninstall -and (Test-Path -LiteralPath "$target.ndd-kit")) {
        Write-Host "  Permanently remove all receipts, backups and staging files: $target.ndd-kit"
    } elseif (-not $Uninstall -and (Test-Path -LiteralPath (Join-Path "$target.ndd-kit" 'backups'))) {
        Write-Host "  Remove previous backups after successful installation: $target.ndd-kit/backups"
    }
}
$sourceReason = ''
if ($Uninstall) {
    $sourceReason = Get-SourceRetentionReason
    if ($sourceReason) { Write-Host "Keep source: $KitDir ($sourceReason)" }
    else { Write-Host "Permanently remove source clone after uninstall: $KitDir" }
}
if ($DryRun) {
    if ($Uninstall -and $Claude -and $Codex) { Clear-RegisteredProjects -Preview }
    Write-Host 'Dry run: no files changed.'; return
}

if ($Uninstall) {
    $uninstallLocks = New-Object 'System.Collections.Generic.List[string]'
    try {
        foreach ($target in $Targets) {
            if (-not (Test-Path -LiteralPath "$target.ndd-kit")) { continue }
            $lock = Join-Path "$target.ndd-kit" 'lock'
            $stream = [IO.File]::Open($lock, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
            $stream.Dispose()
            $uninstallLocks.Add($lock)
        }
        if ($Claude -and $Codex) { Clear-RegisteredProjects }
        foreach ($target in $Targets) {
            if (-not (Test-Path -LiteralPath "$target.ndd-kit")) { continue }
            foreach ($name in $Names) {
                $dest = Join-Path $target $name
                if (Get-Entry $dest) {
                    if (-not (Test-OwnedReceipt (Join-Path "$target.ndd-kit" "$name.receipt"))) { throw "Ownership changed: $dest" }
                    Remove-NddEntry $dest
                    Write-Host "  Removed: $name"
                }
            }
            $lock = Join-Path "$target.ndd-kit" 'lock'
            foreach ($entry in Get-ChildItem -LiteralPath "$target.ndd-kit" -Force) {
                if ($entry.FullName -ne $lock) { Remove-NddEntry $entry.FullName }
            }
            # Hold the lock until contents are gone; remove the empty root last.
            Remove-Item -LiteralPath $lock -Force
            $null = $uninstallLocks.Remove($lock)
            [IO.Directory]::Delete("$target.ndd-kit")
        }
        if (-not $sourceReason) {
            $sourceReason = Get-SourceRetentionReason
            if ($sourceReason) { Write-Host "Source retained: $KitDir ($sourceReason)" }
            else {
                # Leave both PowerShell's and the process's working directories.
                $parent = Split-Path $KitDir -Parent
                Set-Location -LiteralPath $parent
                [Environment]::CurrentDirectory = $parent
                Remove-NddEntry $KitDir
                if (Get-Entry $KitDir) { throw "Source removal incomplete: $KitDir" }
                Write-Host "Removed source clone: $KitDir"
            }
        }
    } catch {
        Write-Warning 'Uninstall incomplete; already deleted files have no backup. Fix the reported error and rerun.'
        throw
    } finally {
        foreach ($lock in $uninstallLocks) {
            try { Remove-Item -LiteralPath $lock -Force }
            catch { Write-Warning "Could not remove lock $lock`: $_" }
        }
    }
    Write-Host 'NDD skills and install state removed. No backups retained. Your project files were preserved.'
    return
}

$Locks = New-Object 'System.Collections.Generic.List[string]'
$Stages = New-Object 'System.Collections.Generic.List[string]'
$Journal = New-Object 'System.Collections.Generic.List[object]'
$InstallFailed = $false
try {
    foreach ($target in $Targets) {
        $null = New-Item -ItemType Directory -Force -Path "$target.ndd-kit"
        $lock = Join-Path "$target.ndd-kit" 'lock'
        # Exclusive file creation also rejects stale locks and concurrent installers.
        $stream = [IO.File]::Open($lock, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        $stream.Dispose()
        $Locks.Add($lock)
    }
    foreach ($target in $Targets) {
        $null = New-Item -ItemType Directory -Force -Path $target
        foreach ($name in $Names) {
            $dest = Join-Path $target $name
            $record = Join-Path "$target.ndd-kit" "$name.receipt"
            $stage = Join-Path "$target.ndd-kit" ('stage.' + [Guid]::NewGuid().ToString('N'))
            $null = New-Item -ItemType Directory -Path $stage
            $Stages.Add($stage)
            $source = Join-Path $KitDir "skills\$name"
            $mode = if ($Link) { 'link' } else { 'copy' }
            if ($Link) { $null = New-Item -ItemType Junction -Path (Join-Path $stage 'skill') -Target $source }
            else { Copy-Item -LiteralPath $source -Destination (Join-Path $stage 'skill') -Recurse -Force }
            $digest = Get-Fingerprint $source
            if ((Get-Fingerprint (Join-Path $stage 'skill')) -ne $digest) { throw "Copy verification failed: $name" }
            $receiptText = "ndd-kit-install-v1`n$Version`n$mode`n$source`n$digest`n"
            [IO.File]::WriteAllText((Join-Path $stage 'receipt'), $receiptText, (New-Object Text.UTF8Encoding($false)))
            $backup = Join-Path "$target.ndd-kit" ('backups\' + $name + '.' + [Guid]::NewGuid().ToString('N'))
            $null = New-Item -ItemType Directory -Force -Path $backup
            $operation = [PSCustomObject]@{ Destination=$dest; Receipt=$record; Backup=$backup; OldMoved=$false; RecordMoved=$false; NewInstalled=$false; NewRecorded=$false }
            $Journal.Add($operation)
            if (Get-Entry $dest) { Move-Item -LiteralPath $dest -Destination (Join-Path $backup 'skill'); $operation.OldMoved=$true }
            if (Get-Entry $record) { Move-Item -LiteralPath $record -Destination (Join-Path $backup 'receipt'); $operation.RecordMoved=$true }
            Move-Item -LiteralPath (Join-Path $stage 'skill') -Destination $dest; $operation.NewInstalled=$true
            Move-Item -LiteralPath (Join-Path $stage 'receipt') -Destination $record; $operation.NewRecorded=$true
            Write-Host "  Installed: $name"
        }
    }
} catch {
    $InstallFailed = $true
    $failure = $_
    Write-Warning 'Installation failed; restoring previous skills and receipts.'
    $restoreFailed = $false
    for ($i = $Journal.Count - 1; $i -ge 0; $i--) {
        $operation = $Journal[$i]
        try {
            if ($operation.NewInstalled) { Remove-NddEntry $operation.Destination }
            if ($operation.NewRecorded) { Remove-Item -LiteralPath $operation.Receipt -Force }
            if ($operation.OldMoved) { Move-Item -LiteralPath (Join-Path $operation.Backup 'skill') -Destination $operation.Destination }
            if ($operation.RecordMoved) { Move-Item -LiteralPath (Join-Path $operation.Backup 'receipt') -Destination $operation.Receipt }
        } catch { $restoreFailed = $true; Write-Warning "Restore failed; recover from $($operation.Backup): $_" }
    }
    throw $failure
} finally {
    $cleanupFailed = $false
    foreach ($stage in $Stages) {
        # Remove a staged junction itself before recursively deleting its container.
        try {
            Remove-NddEntry (Join-Path $stage 'skill')
            Remove-Item -LiteralPath $stage -Recurse -Force
        } catch { $cleanupFailed = $true; Write-Warning "Could not clean staging directory $stage`: $_" }
    }
    # Previous copies exist only for rollback until all selected targets succeed.
    if (-not $InstallFailed) {
        foreach ($target in $Targets) {
            try { Remove-NddEntry (Join-Path "$target.ndd-kit" 'backups') }
            catch { $cleanupFailed = $true; Write-Warning "Could not remove backups in $target.ndd-kit`: $_" }
        }
    } elseif (-not $restoreFailed) {
        foreach ($operation in $Journal) {
            try { [IO.Directory]::Delete($operation.Backup) }
            catch { $cleanupFailed = $true; Write-Warning "Could not remove recovery directory $($operation.Backup): $_" }
        }
    }
    foreach ($lock in $Locks) {
        try { Remove-Item -LiteralPath $lock -Force }
        catch { $cleanupFailed = $true; Write-Warning "Could not remove lock $lock`: $_" }
    }
    if ($cleanupFailed -and -not $InstallFailed) { throw 'Install applied but cleanup is incomplete; inspect the reported paths before retrying.' }
}
Write-Host "Installed NDD $Version. In your project use /ndd-setup (Claude Code) or `$ndd-setup (Codex)."
Write-Host 'Restart the agent if the skills do not appear.'
