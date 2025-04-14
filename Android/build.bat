@echo off
setlocal enabledelayedexpansion

REM Установка переменных окружения
set ANDROID_HOME=C:\Users\user\AppData\Local\Android\Sdk
set ANDROID_NDK_HOME=C:\Users\user\AppData\Local\Android\Sdk\ndk\25.1.8937393
set JAVA_HOME=C:\Program Files\Java\jdk-11
set ANT_HOME=C:\apache-ant-1.9.4

REM Добавление в PATH
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools;%ANT_HOME%\bin;%PATH%

REM Создание виртуального окружения
python -m venv venv
call venv\Scripts\activate.bat

REM Установка необходимых пакетов
pip install --upgrade pip
pip install buildozer
pip install cython
pip install python-for-android

REM Создание директории для логов
if not exist logs mkdir logs

REM Запуск сборки
buildozer android debug > logs\build_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log 2>&1

pause 