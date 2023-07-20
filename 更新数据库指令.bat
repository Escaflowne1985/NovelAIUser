@echo off

..\myenv\python.exe manage.py makemigrations
..\myenv\python.exe manage.py migrate