cd /d "G:\GitSYNC\MapTextLang"
git pull origin master


@echo off
set "sd=F:\CSGOSERVER\csgoserverzev2\csgo\addons\sourcemod\configs\console_t"
set "dd=G:\GitSYNC\MapTextLang\maptext"
rem -2前天，-1昨天，0今天
set d=-1
for /f %%a in ('mshta VBScript:Execute("NewDate=date+(%d%):FmtDate=right(year(NewDate),4)&right(""0""&month(NewDate),2)&right(""0""&day(NewDate),2):CreateObject(""Scripting.FileSystemObject"").GetStandardStream(1).Write FmtDate:close"^)') do set yd=%%a
echo;昨天日期为%yd%
cd /d "%sd%"
if not exist "%dd%"  md "%dd%"
setlocal enabledelayedexpansion
for /f "delims=" %%i in ('dir *.*/a-d /b /s') do (
    set fd=%%~ti
    set fd=!fd:~,10!
    set fd=!fd:-=!
    set fd=!fd:/=!
    if "!fd!"=="%yd%" (
        copy "%%i" "%dd%" /y 2>nul||(attrib -r -s -h "%%i"& copy "%%i" "%dd%" /y >nul)
    )
)



@echo off
set "sd=F:\CSGOSERVER\csgoserverzev2\csgo\addons\sourcemod\configs\bosshit"
set "dd=G:\GitSYNC\MapTextLang\bosshit"
rem -2前天，-1昨天，0今天
set d=-1
for /f %%a in ('mshta VBScript:Execute("NewDate=date+(%d%):FmtDate=right(year(NewDate),4)&right(""0""&month(NewDate),2)&right(""0""&day(NewDate),2):CreateObject(""Scripting.FileSystemObject"").GetStandardStream(1).Write FmtDate:close"^)') do set yd=%%a
echo;昨天日期为%yd%
cd /d "%sd%"
if not exist "%dd%"  md "%dd%"
setlocal enabledelayedexpansion
for /f "delims=" %%i in ('dir *.*/a-d /b /s') do (
    set fd=%%~ti
    set fd=!fd:~,10!
    set fd=!fd:-=!
    set fd=!fd:/=!
    if "!fd!"=="%yd%" (
        copy "%%i" "%dd%" /y 2>nul||(attrib -r -s -h "%%i"& copy "%%i" "%dd%" /y >nul)
    )
)






cd /d "G:\GitSYNC\MapTextLang"
git add . && git commit -m autoupdate && git push origin master


