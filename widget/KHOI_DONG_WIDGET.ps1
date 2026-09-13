# ==============================================================================
#  1-CLICK LAUNCHER: ANTIGRAVITY QUOTA WIDGET (V10 PRO ULTIMATE)
# ==============================================================================
$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $projectDir -or -not (Test-Path "$projectDir\main.py")) {
    $projectDir = $PSScriptRoot
}
if (-not (Test-Path "$projectDir\main.py")) {
    $projectDir = (Get-Location).Path
}

# 1. Đóng cửa sổ widget cũ một cách an toàn
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class AntigravityWidgetCloser {
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern IntPtr FindWindow(string className, string windowName);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam);
}
'@
foreach ($cls in @('AntigravityQuotaWidgetV10Pro', 'CockpitQuotaWidgetV10Pro', 'CockpitQuotaWidgetV9')) {
  for ($i = 0; $i -lt 10; $i++) {
    $wnd = [AntigravityWidgetCloser]::FindWindow($cls, $null)
    if ($wnd -eq [IntPtr]::Zero) { break }
    [void][AntigravityWidgetCloser]::PostMessage($wnd, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) # WM_CLOSE
    Start-Sleep -Milliseconds 40
  }
}

# Đảm bảo tiến trình python main.py cũ kết thúc hoàn toàn để giải phóng Mutex
Get-CimInstance Win32_Process -Filter "CommandLine like '%main.py%'" | ForEach-Object {
  Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Milliseconds 300

# 2. Khởi chạy Antigravity Quota Widget qua pythonw (tìm động trên mọi máy)
$pyw = (Get-Command pythonw -ErrorAction SilentlyContinue).Source
if (-not $pyw) {
    $py = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($py) {
        $cand = Join-Path (Split-Path $py) 'pythonw.exe'
        if (Test-Path $cand) { $pyw = $cand }
    }
}
if (-not $pyw) {
    try {
        $pyPath = (py -c "import sys; print(sys.executable)" 2>$null)
        if ($pyPath) {
            $cand = Join-Path (Split-Path $pyPath.Trim()) 'pythonw.exe'
            if (Test-Path $cand) { $pyw = $cand }
        }
    } catch {}
}

if ($pyw -and (Test-Path "$projectDir\main.py")) {
  Start-Process -FilePath $pyw -ArgumentList "main.py" -WorkingDirectory $projectDir
} elseif (Test-Path "$projectDir\main.py") {
  Start-Process -FilePath "python" -ArgumentList "main.py" -WorkingDirectory $projectDir -WindowStyle Hidden
}
Start-Sleep -Milliseconds 500
