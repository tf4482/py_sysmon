@echo off

if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

set "project=py_sysmon"

set "projects_dir=<projects_dir>"

set "target_dir=%projects_dir%\backups"

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "fullstamp=%YYYY%-%MM%-%DD%-%HH%%Min%%Sec%"

mkdir "%target_dir%\%project%_backup_%fullstamp%"

set "exclude_dirs="
set "exclude_files="

call :RobocopyTask "%projects_dir%\%project%" "%target_dir%\%project%_backup_%fullstamp%"

exit

:RobocopyTask

setlocal

set "source_dir=%~1"
set "dest_dir=%~2"
set "options=/UNILOG+:%target_dir%\%project%_backup_%fullstamp%\backup_%fullstamp%.log /MIR /MT:16 /W:2 /R:10 /XJ /XC /ETA /TEE /XD %exclude_dirs% /XF %exclude_files%"

robocopy "%source_dir%" "%dest_dir%" %options%

endlocal

:eof
