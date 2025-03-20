@echo off
FOR /L %%i IN (1,1,20) DO (
    echo This is iteration %%i
    daily_run.bat
)
