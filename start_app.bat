@echo off
python -m pip install -r ./setUp/requirements.txt
cd ./src
start "" pythonw main.py