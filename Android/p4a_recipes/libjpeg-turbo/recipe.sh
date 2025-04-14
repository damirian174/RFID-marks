#!/bin/bash

# Рецепт для сборки libjpeg-turbo без использования cmake

VERSION_libjpeg="2.0.1"
URL_libjpeg="https://github.com/libjpeg-turbo/libjpeg-turbo/archive/${VERSION_libjpeg}.tar.gz"
MD5_libjpeg=""
BUILD_libjpeg=$BUILD_PATH/libjpeg/build
RECIPE_libjpeg=$RECIPES_PATH/libjpeg

function prebuild_libjpeg() {
    true
}

function build_libjpeg() {
    cd $BUILD_libjpeg

    # Конфигурирование
    ./configure --host=$HOSTARCH --prefix=$RECIPE_libjpeg/dist

    # Сборка
    make -j4

    # Установка
    make install
}

function postbuild_libjpeg() {
    true
} 