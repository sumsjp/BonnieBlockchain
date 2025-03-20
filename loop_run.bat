@echo off
FOR /L %%i IN (1,1,25) DO (
    echo This is iteration %%i
    daily_run.bat
    timeout /t 60
)
