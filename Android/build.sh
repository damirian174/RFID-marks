#!/bin/bash

echo "Проверка наличия необходимых зависимостей..."

# Проверяем наличие cmake
if ! command -v cmake &> /dev/null; then
    echo "Ошибка: не найден пакет cmake, необходимый для сборки."
    echo "Установите его с помощью следующей команды:"
    echo "sudo apt-get install -y cmake build-essential"
    exit 1
fi

# Установка переменных окружения
echo "Настройка переменных окружения..."
export ANDROID_HOME="$HOME/Android/Sdk"
export ANDROID_NDK_HOME="$ANDROID_HOME/ndk/25.1.8937393"
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH"

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения Python..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source venv/bin/activate

# Установка необходимых пакетов
echo "Установка Python-зависимостей..."
pip install --upgrade pip
pip install buildozer
pip install cython
pip install python-for-android

# Создание директории для логов
mkdir -p logs

# Запуск сборки
echo "Запуск сборки приложения..."
buildozer -v android debug 2>&1 | tee logs/build_$(date +%Y%m%d_%H%M%S).log 