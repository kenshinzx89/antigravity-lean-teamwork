# ====================================================================
# Antigravity Lean Teamwork + Desktop Widget 1-Click Installer
# ====================================================================
$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🚀 CÀI ĐẶT ANTIGRAVITY LEAN TEAMWORK v1.5.0 + DESKTOP WIDGET" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Kiểm tra Python
Write-Host "`n[1/4] Kiểm tra môi trường Python..." -ForegroundColor White
$pythonCmd = "python"
if (Get-Command "py" -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Không tìm thấy Python! Vui lòng cài đặt Python 3.10+ từ python.org trước." -ForegroundColor Red
    Exit 1
}

$pyVer = & $pythonCmd --version 2>&1
Write-Host "  ✓ Tìm thấy: $pyVer" -ForegroundColor Green

# 2. Đồng bộ Skill & Hook vào Antigravity IDE
Write-Host "`n[2/4] Nạp Lean Teamwork Protocol & PreInvocation Hook vào Antigravity..." -ForegroundColor White
& $pythonCmd sync_skill.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Đồng bộ thất bại!" -ForegroundColor Red
    Exit 1
}

# 3. Tạo Shortcut Desktop cho Widget
Write-Host "`n[3/4] Tạo Shortcut ngoài màn hình Desktop..." -ForegroundColor White
try {
    $WshShell = New-Object -comObject WScript.Shell
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcut = $WshShell.CreateShortcut("$desktopPath\Antigravity Widget.lnk")
    $vbsPath = Join-Path $PSScriptRoot "widget\KHOI_DONG_WIDGET.vbs"
    $shortcut.TargetPath = "wscript.exe"
    $shortcut.Arguments = "`"$vbsPath`""
    $shortcut.WorkingDirectory = Join-Path $PSScriptRoot "widget"
    $shortcut.WindowStyle = 7
    $shortcut.Description = "Khởi động Antigravity Quota Widget & Teamwork HUD"
    $shortcut.Save()
    Write-Host "  ✓ Đã tạo shortcut 'Antigravity Widget' trên Desktop!" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Không thể tạo shortcut desktop (bỏ qua): $_" -ForegroundColor DarkYellow
}

# 4. Khởi động Desktop Widget
Write-Host "`n[4/4] Khởi động Antigravity Desktop Widget..." -ForegroundColor White
try {
    Start-Process "wscript.exe" -ArgumentList "`"$PSScriptRoot\widget\KHOI_DONG_WIDGET.vbs`"" -WorkingDirectory "$PSScriptRoot\widget"
    Write-Host "  ✓ Desktop Widget đã được kích hoạt thành công!" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Hãy chạy file widget\KHOI_DONG_WIDGET.vbs thủ công." -ForegroundColor DarkYellow
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "  🎉 CÀI ĐẶT HOÀN TẤT 100%! HỆ THỐNG ĐÃ SẴN SÀNG!" -ForegroundColor Green
Write-Host "  • Skill & Hook: Đã tích hợp trực tiếp vào Antigravity IDE" -ForegroundColor White
Write-Host "  • Desktop Widget: Đang chạy nổi trên màn hình" -ForegroundColor White
Write-Host "  • Hướng dẫn chi tiết: Xem file INSTALL.md" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
