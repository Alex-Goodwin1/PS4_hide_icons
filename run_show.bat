@echo off
chcp 65001 >nul
cd /d "%~dp0"
title hide_icons - bring the hidden icons back

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
echo   PS4 %IP%   -   BRING BACK the icons you choose (visible=1)
echo   Every icon of app.db is printed with a number, then type the
echo   numbers to bring back, separated by a comma (for example 1,3,7).
echo   The program then asks which user to edit (a number from the profiles
echo   list, or Enter for the first profile only).
echo   Second argument = set that user at once (profile suffix).
echo ================================================================
echo.
%PROG% %IP% --show --pick --apply %PROFILE_ARG%
echo.
echo Log the PS4 user out or reboot the console so PS4 reads app.db again.
echo.
pause
