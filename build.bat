@echo off
chcp 65001 >nul
echo ========================================
echo   CHM to MD 打包工具
echo ========================================
echo.

REM 检查是否有 pyinstaller
python -c "import pyinstaller" 2>nul
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

REM 检查7z.exe
if not exist "C:\Program Files\7-Zip\7z.exe" (
    if not exist "C:\Program Files (x86)\7-Zip\7z.exe" (
        echo 警告: 未找到 7-Zip，将使用系统PATH中的7z命令
    )
)

echo.
echo 开始打包...
echo.

REM 打包
pyinstaller chm_to_md.spec --clean

if errorlevel 1 (
    echo.
    echo 打包失败!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   打包完成!
echo ========================================
echo.
echo 输出文件: dist\chm_to_md.exe
echo.

REM 询问是否删除build目录
set /p clean="是否删除build目录? (Y/N): "
if /i "%clean%"=="Y" (
    rmdir /s /q build
    echo 已删除build目录
)

echo.
pause
