@echo off
:: SolSense Launcher - Auto-install dependencies and run application
:: ============================================================

setlocal enabledelayedexpansion

:: Set console colors and title
color 0A
title SolSense GeoTIFF Viewer - Launcher

echo.
echo ========================================
echo   SolSense GeoTIFF Viewer Launcher
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

:: Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available!
    echo Please ensure pip is installed with Python.
    echo.
    pause
    exit /b 1
)

echo [OK] pip found:
python -m pip --version
echo.

:: Create a flag file to track if dependencies were installed
set "FLAG_FILE=%TEMP%\solsense_deps_installed.flag"

:: Check if this is the first run or dependencies need installation
if not exist "%FLAG_FILE%" (
    echo ========================================
    echo   Installing Required Dependencies
    echo ========================================
    echo.
    echo This may take a few minutes on first run...
    echo.
    
    :: Upgrade pip first
    echo [1/7] Upgrading pip...
    python -m pip install --upgrade pip --quiet
    
    :: Install numpy first (required by many other packages)
    echo [2/7] Installing numpy...
    python -m pip install numpy --quiet
    
    :: Install matplotlib
    echo [3/7] Installing matplotlib...
    python -m pip install matplotlib --quiet
    
    :: Install Pillow
    echo [4/7] Installing Pillow...
    python -m pip install Pillow --quiet
    
    :: Install requests
    echo [5/7] Installing requests...
    python -m pip install requests --quiet
    
    :: Install psutil
    echo [6/7] Installing psutil...
    python -m pip install psutil --quiet
    
    :: Install rasterio (may take longer)
    echo [7/7] Installing rasterio...
    python -m pip install rasterio --quiet
    
    if errorlevel 1 (
        echo.
        echo [WARNING] Some packages failed to install!
        echo.
        echo GDAL/rasterio may require special installation.
        echo If the app fails to run, try:
        echo   - conda install -c conda-forge rasterio gdal
        echo   - Or visit: https://github.com/rasterio/rasterio
        echo.
        pause
    ) else (
        :: Create flag file to skip installation next time
        echo Installation completed successfully! > "%FLAG_FILE%"
        echo.
        echo [OK] All dependencies installed successfully!
    )
    
    echo.
    echo ========================================
    echo.
) else (
    echo [OK] Dependencies already installed (skipping installation)
    echo     To force reinstall, delete: %FLAG_FILE%
    echo.
)

:: Check if main.py exists
if not exist "main.py" (
    echo [ERROR] main.py not found in current directory!
    echo Please ensure you're running this batch file from the SolSense directory.
    echo.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

:: Launch the application
echo ========================================
echo   Starting SolSense Application
echo ========================================
echo.
echo The application window will open shortly...
echo This console will minimize automatically.
echo.

:: Wait a moment for user to read message
timeout /t 2 /nobreak >nul

:: Launch Python with pythonw.exe to hide console, fallback to python if not available
where pythonw.exe >nul 2>&1
if errorlevel 1 (
    start "" python main.py
) else (
    start "" pythonw.exe main.py
)

:: Check exit code
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Application exited with errors!
    echo ========================================
    echo.
    echo Common issues:
    echo   1. Missing tkinter: Install python3-tk
    echo   2. GDAL not installed: Try conda installation
    echo   3. Missing resource files: Check resources/ folder
    echo.
    pause
    exit /b 1
)

:: Application launched successfully, exit quietly
exit /b 0