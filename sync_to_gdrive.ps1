[CmdletBinding()]
param(
    [string]$TargetGDrive = ""
)

$ErrorActionPreference = "Stop"

# 自動動態尋找 Google Drive 上的 ManimGX-media 資料夾 (避免 UTF-8/Big5 編碼字串硬編碼問題)
if ([string]::IsNullOrWhiteSpace($TargetGDrive)) {
    $found = Get-ChildItem -Path "G:\*","I:\*" -Directory -ErrorAction SilentlyContinue | ForEach-Object { 
        Get-ChildItem -Path $_.FullName -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            Get-ChildItem -Path $_.FullName -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*ManimGX-media*" }
        }
    } | Select-Object -First 1

    if ($found) {
        $TargetGDrive = $found.FullName
    } else {
        $TargetGDrive = "G:\我的雲端硬碟\數學教學\ManimGX-media"
    }
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " [ManimGX-media] Syncing videos to Google Drive..." -ForegroundColor Cyan
Write-Host " Target: $TargetGDrive" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

if (!(Test-Path $TargetGDrive)) {
    Write-Warning "Target directory not found: $TargetGDrive"
    exit 1
}

$projectRoot = $PSScriptRoot
$copiedCount = 0
$totalSize = 0

$folders = Get-ChildItem -Path $projectRoot -Directory | Where-Object { 
    $_.Name -notmatch "^(\.agents|\.git|media|voice_samples|\.venv)$" 
}

foreach ($folder in $folders) {
    $topic = $folder.Name
    $destFolder = Join-Path $TargetGDrive $topic

    if (!(Test-Path $destFolder)) {
        New-Item -ItemType Directory -Path $destFolder -Force | Out-Null
    }

    $rootVideos = Get-ChildItem -Path $folder.FullName -Filter "*.mp4" -File -ErrorAction SilentlyContinue
    $mediaVideos = Get-ChildItem -Path $folder.FullName -Recurse -Filter "*.mp4" -File -ErrorAction SilentlyContinue | 
        Where-Object { $_.FullName -notmatch "partial_movie_files" -and $_.DirectoryName -ne $folder.FullName }

    $allVideos = @($rootVideos) + @($mediaVideos)

    foreach ($video in $allVideos) {
        $destPath = Join-Path $destFolder $video.Name
        $needCopy = $false

        if (!(Test-Path $destPath)) {
            $needCopy = $true
        } else {
            $destFile = Get-Item $destPath
            if ($video.LastWriteTime -gt $destFile.LastWriteTime -or $video.Length -ne $destFile.Length) {
                $needCopy = $true
            }
        }

        if ($needCopy) {
            $sizeMB = [math]::round($video.Length / 1MB, 2)
            Write-Host "  -> Copying [$topic] $($video.Name) ($sizeMB MB)" -ForegroundColor Green
            Copy-Item -Path $video.FullName -Destination $destPath -Force
            $copiedCount++
            $totalSize += $video.Length
        }
    }
}

Write-Host "------------------------------------------" -ForegroundColor Cyan
if ($copiedCount -eq 0) {
    Write-Host "All videos in Google Drive are up to date." -ForegroundColor Green
} else {
    $totalMB = [math]::round($totalSize / 1MB, 2)
    Write-Host "Sync complete! Copied $copiedCount files ($totalMB MB)." -ForegroundColor Green
}
Write-Host "==========================================" -ForegroundColor Cyan
