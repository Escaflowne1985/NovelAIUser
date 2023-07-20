@echo off

start http://127.0.0.1

..\myenv\python.exe manage.py runserver 0.0.0.0:80 --insecure


