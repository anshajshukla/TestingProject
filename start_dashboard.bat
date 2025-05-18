@echo off
echo Starting Banking Test Framework ML Dashboard...
echo.
echo This may take a few moments to initialize...
echo.

:: Ensure directories exist
if not exist "data" mkdir data
if not exist "reports" mkdir reports

:: Run the dashboard with the proper Python path
cd %~dp0
python -m dashboard.app
