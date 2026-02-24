@echo off
setlocal enabledelayedexpansion

set "psScript=%temp%\%~n0_temp.ps1"

(
echo Add-Type -AssemblyName System.Windows.Forms
echo $fb = New-Object System.Windows.Forms.FolderBrowserDialog
echo $fb.Description = "Select CHM folder"
echo if ($fb.ShowDialog() -eq "OK") { echo $fb.SelectedPath }
) > "%psScript%"

for /f "delims=" %%a in ('powershell -ExecutionPolicy Bypass -File "%psScript%"') do set "selectedFolder=%%a"
del "%psScript%"

if not defined selectedFolder goto :cancel

echo Selected: %selectedFolder%

set "outputFolder=%selectedFolder%\html"
if not exist "%outputFolder%" mkdir "%outputFolder%"

for %%f in ("%selectedFolder%\*.chm") do (
    set "chmName=%%~nf"
    set "destFolder=%outputFolder%\!chmName!"
    if not exist "!destFolder!" (
        mkdir "!destFolder!"
        7z x -y "%%f" -o"!destFolder!" >nul 2>&1
        echo Done: %%~nf.chm
    ) else (
        echo Skip: %%~nf.chm
    )
)

echo.
echo Finished!
pause
exit /b

:cancel
echo Cancelled
pause
