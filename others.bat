@echo off
pause
notepad food.csv
timeout /t 10 /nobreak >nul
taskkill /im notepad.exe
notepad users.txt
timeout /t 10 /nobreak >nul
taskkill /im notepad.exe
explorer .\Users