@echo off
cd /d C:/Users/Pucha/playground/python_general/manga_tracker
call venv\Scripts\activate.bat
python src\Manga_Tracker.py
if %ERRORLEVEL% NEQ 0 (
    echo [%date% %time%] Error: %ERRORLEVEL% >> error.log
)