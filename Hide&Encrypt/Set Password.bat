@echo off
echo Input your password:
set/p "pass= "
(For /f "delims=" %%i in (Original.bat) do (Set str=%%i
SetLocal EnableDelayedExpansion
Set str=!Str:originalpassword=%pass%!
echo !str!
EndLocal
))>HideAndEncrypt.bat
echo Successfully set!
pause>nul