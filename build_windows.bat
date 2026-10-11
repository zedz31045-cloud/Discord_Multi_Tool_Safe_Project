@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
echo ================================================
echo Dafan Discord Multi-Tool - Safe Edition Builder
echo ================================================
where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher was not found. Install Python 3.11+ from python.org and enable Add Python to PATH.
  pause
  exit /b 1
)
py -m pip install --upgrade pip
if errorlevel 1 goto :fail
py -m pip install -r requirements.txt
if errorlevel 1 goto :fail
py -m PyInstaller --noconfirm --clean --onefile --windowed --name Discord_Multi_Tool main.py
if errorlevel 1 goto :fail
echo.
echo Build completed. EXE: dist\Discord_Multi_Tool.exe
pause
exit /b 0
:fail
echo.
echo Build failed. Read the error above.
pause
exit /b 1
