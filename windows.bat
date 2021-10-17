@ECHO OFF
ECHO. && ECHO Make sure you have activated your virtual environment if you have one. If you have not, then stop this script now by pressing Ctrl+C  && ECHO.
ping 127.0.0.1 -n 8 > nul
WHERE python
IF %ERRORLEVEL% NEQ 0 (ECHO. && ECHO Python wasn't found. Please install Python to proceed. && EXIT /B 1)
ECHO. && ECHO Installing dependencies, please wait... && ECHO.
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (ECHO An error occurred while installing dependencies. Please file an issue on our GitHub page.&& ECHO https://github.com/RishiRats/airtype-by-elpida) ELSE (ECHO. && ECHO Dependencies installed successfully. && ECHO.)
PAUSE