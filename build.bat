@echo off

pip install pyinstaller
cd src
copy main.py main.pyw
pyinstaller --onefile main.pyw
del main.pyw
