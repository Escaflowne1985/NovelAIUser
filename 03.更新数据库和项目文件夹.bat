@echo off
chcp 65001

echo 正在执行项目数据库迁移...

..\myenv\python.exe .\manage.py makemigrations
..\myenv\python.exe .\manage.py migrate

echo 项目数据库迁移已完成。


echo 正在创建文件夹结构...

mkdir MovieProcess
mkdir MovieProcess\base
mkdir MovieProcess\models
mkdir MovieProcess\result
mkdir VideoProcess
mkdir VideoProcess\video
mkdir VideoProcess\result
mkdir VideoProcess\video\base
mkdir VideoProcess\video\image

echo 文件夹结构创建完成。

pause