# 心动积分项目 - 打包脚本
# 用于创建期末作业提交的压缩包

$projectPath = "D:\Obsidian知识库\知识库\10_Projects\Python心动积分"
$zipFileName = "Python心动积分_期末作业_$(Get-Date -Format 'yyyyMMdd').zip"
$outputPath = "D:\Obsidian知识库\知识库\10_Projects"

Write-Host "====================================" -ForegroundColor Green
Write-Host "  心动积分项目 - 期末作业打包工具" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# 创建临时目录
$tempDir = Join-Path $env:TEMP "Python心动积分_打包"
if (Test-Path $tempDir) {
    Remove-Item -Recurse -Force $tempDir
}
New-Item -ItemType Directory -Path $tempDir | Out-Null

Write-Host "正在复制文件到临时目录..." -ForegroundColor Yellow

# 复制必须包含的文件和文件夹
$filesToCopy = @(
    "期末大作业报告.md",
    "main.py",
    "requirements.txt",
    "backend",
    "frontend",
    "tests",
    "data",
    "截图"
)

foreach ($item in $filesToCopy) {
    $sourcePath = Join-Path $projectPath $item
    if (Test-Path $sourcePath) {
        Write-Host "  ✓ 复制: $item" -ForegroundColor Green
        Copy-Item -Recurse -Force $sourcePath (Join-Path $tempDir $item)
    } else {
        Write-Host "  ✗ 未找到: $item" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "正在创建压缩包..." -ForegroundColor Yellow

# 创建压缩包
$tempZipPath = Join-Path $env:TEMP "$zipFileName.zip"
if (Test-Path $tempZipPath) {
    Remove-Item -Force $tempZipPath
}

# 使用PowerShell的Compress-Archive
Compress-Archive -Path "$tempDir\*" -DestinationPath $tempZipPath -Force

# 移动到输出目录
$finalZipPath = Join-Path $outputPath $zipFileName
Move-Item -Force $tempZipPath $finalZipPath

# 清理临时目录
Remove-Item -Recurse -Force $tempDir

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  打包完成！" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "压缩包位置: $finalZipPath" -ForegroundColor Cyan
Write-Host ""

# 显示文件大小
$fileSize = (Get-Item $finalZipPath).Length / 1MB
Write-Host "文件大小: $($fileSize.ToString('0.00')) MB" -ForegroundColor Cyan
Write-Host ""

Write-Host "包含的文件和文件夹:" -ForegroundColor Yellow
Get-ChildItem $tempDir -Recurse | ForEach-Object {
    Write-Host "  - $($_.FullName.Replace($tempDir, ''))" -ForegroundColor Gray
}

Write-Host ""
Write-Host "✓ 作业已准备就绪，可以提交了！" -ForegroundColor Green
Write-Host ""

# 打开文件夹
explorer $outputPath
