@echo off
rem SaadAI Labs - Live Clipper: runs the job in output\job.json. Log: output\pipeline.log
cd /d "%~dp0scripts"
where py >nul 2>nul && (py -3 run_pipeline.py %* & goto :eof)
where python >nul 2>nul && (python run_pipeline.py %* & goto :eof)
echo Python is not installed. Install it from python.org (tick "Add python.exe to PATH"), then try again.
pause
