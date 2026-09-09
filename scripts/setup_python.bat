@echo off

cd /d "%~dp0"

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing packages...
pip install -r requirements.txt

echo Done!
pause
