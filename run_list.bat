@echo off
chcp 65001 >nul
cd /d "%~dp0"
title hide_icons - list the desktop icons of the PS4

set PROG="%~dp0hide_icons.exe"
if not exist "%~dp0hide_icons.exe" (
	echo.
	echo hide_icons.exe was not found next to this file.
	echo Unpack the whole archive into one folder and run it from there.
	echo.
	pause
	exit /b 1
)

set IP=%1
if "%IP%"=="" set /p IP=PS4 IP address: 
if "%IP%"=="" (
	echo.
	echo No PS4 IP address was given.
	echo.
	pause
	exit /b 1
)

set "PROFILE_ARG="
if not "%2"=="" set "PROFILE_ARG=--profile %2"

echo.
echo ================================================================
echo   PS4 %IP%   -   LIST ONLY, app.db is not changed
echo   Every user (tbl_appbrowse_<suffix>) is printed as a separate column.
echo   Second argument = list one user only (profile suffix).
echo ================================================================
echo.
%PROG% %IP% --list %PROFILE_ARG%
echo.
pause
