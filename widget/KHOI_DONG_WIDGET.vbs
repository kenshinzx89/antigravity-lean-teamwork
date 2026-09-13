Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "powershell.exe -ExecutionPolicy Bypass -File """ & WshShell.CurrentDirectory & "\KHOI_DONG_WIDGET.ps1""", 0, False
