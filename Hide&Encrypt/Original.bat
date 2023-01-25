cls
@ECHO OFF
title Folder
if EXIST "Encrypted Folder" goto UNLOCK
if NOT EXIST Folder goto MDLOCKER
:CONFIRM
echo Are you sure to lock the folder?(Y/N)
set/p "cho= "
if %cho%==Y goto LOCK
if %cho%==y goto LOCK
if %cho%==n goto END
if %cho%==N goto END
echo Invaild Choice.
pause>nul
goto CONFIRM
:LOCK
ren Folder "Encrypted Folder"
attrib +h +s "Encrypted Folder"
echo The Folder was locked.
pause>nul
goto End
:UNLOCK
echo Enter the password:
set/p "pass= "
if NOT %pass%==originalpassword goto FAIL
attrib -h -s "Encrypted Folder"
ren "Encrypted Folder" Folder
echo Folder was unlocked.
pause>nul
goto End
:FAIL
echo Invaild Password
pause>nul
goto end
:MDLOCKER
md Folder
echo Successfully create Folder.
pause>nul
goto End
:End