#!/bin/bash

echo "Установка системных зависимостей для сборки Android-приложения..."

# Проверка прав суперпользователя
if [ "$(id -u)" -ne 0 ]; then
   echo "Ошибка: этот скрипт должен быть запущен с правами суперпользователя (sudo)"
   echo "Пожалуйста, запустите: sudo ./install_dependencies.sh"
   exit 1
fi

# Обновление репозиториев пакетов
echo "Обновление репозиториев пакетов..."
apt-get update

# Установка необходимых пакетов
echo "Установка необходимых системных пакетов..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    openjdk-11-jdk \
    cmake \
    build-essential \
    git \
    unzip \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    wget

echo "Все системные зависимости успешно установлены!"
echo "Теперь можно запустить сборку приложения командой: ./build.sh" 