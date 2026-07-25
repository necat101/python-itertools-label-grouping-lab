@echo off
REM run_lab.bat — python-itertools-label-grouping-lab
setlocal

REM Find a usable Python (prefer python, fall back to python3, then py)
where python >nul 2>nul
if %errorlevel%==0 (
    set PY=python
    goto :run
)
where python3 >nul 2>nul
if %errorlevel%==0 (
    set PY=python3
    goto :run
)
where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py
    goto :run
)
echo Error: python / python3 / py not found in PATH
exit /b 1

:run
%PY% --version
echo.
echo === run_lab.py ===
%PY% run_lab.py
if %errorlevel% neq 0 exit /b %errorlevel%
echo.
echo === unittest test_lab ===
%PY% -m unittest test_lab -v
