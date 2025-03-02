@echo off
setlocal

REM 获取Python安装路径
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
set PYTHONW_PATH=%PYTHON_PATH:python.exe=pythonw.exe%

REM 创建VBS脚本
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\Desktop\PDF工具.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%PYTHONW_PATH%" >> CreateShortcut.vbs
echo oLink.Arguments = """%~dp0app.py""" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
if exist "%~dp0icon.ico" (
    echo oLink.IconLocation = "%~dp0icon.ico" >> CreateShortcut.vbs
)
echo oLink.Save >> CreateShortcut.vbs

REM 执行VBS脚本
cscript //nologo CreateShortcut.vbs
if errorlevel 1 (
    echo 创建快捷方式失败！
) else (
    echo 桌面快捷方式创建成功！
)

REM 清理VBS脚本
del CreateShortcut.vbs

pause 