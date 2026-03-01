@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PYEXE=c:\Users\zxf\AppData\Local\Programs\Python\Python313\python.exe"
echo 当前使用的 Python: %PYEXE%
echo.
echo [1/2] 检查 PyInstaller 是否已安装...
"%PYEXE%" -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 未检测到 PyInstaller，正在安装...
    "%PYEXE%" -m pip install pyinstaller
    if errorlevel 1 (
        echo 安装 PyInstaller 失败，请检查网络后重试。
        pause
        exit /b 1
    )
)
echo.
echo [2/2] 开始打包 "打铁计算器".exe ...
"%PYEXE%" -m PyInstaller --noconsole --onefile --name "打铁计算器" main.pyw
if errorlevel 1 (
    echo.
    echo 打包失败，请查看上方错误信息。
    pause
    exit /b 1
)
echo.
echo 打包完成：dist\打铁计算器.exe
pause
