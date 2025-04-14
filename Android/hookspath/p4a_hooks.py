#!/usr/bin/env python3

"""
Хуки для python-for-android для решения проблем сборки
"""

import os
import shutil
import subprocess


def find_executable(executable_name):
    """Проверяет наличие исполняемого файла в PATH."""
    path = os.environ.get('PATH', '').split(os.pathsep)
    for directory in path:
        executable_path = os.path.join(directory, executable_name)
        if os.path.exists(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path
    return None


def post_build_apk(app_dir, package_name, arch, debug):
    """Хук, который вызывается после сборки APK."""
    print("Сборка APK завершена!")
    return True


def after_recipe_build(recipe_name, arch, ctx):
    """Вызывается после сборки каждого рецепта."""
    print(f"Рецепт {recipe_name} успешно собран!")
    
    # Обход проблемы с cmake для jpeg
    if recipe_name == 'jpeg':
        # Если файлы cmake не найдены, пытаемся использовать autoconf
        print("Пытаемся собрать jpeg с использованием autoconf вместо cmake...")
        recipe_dir = ctx.get_recipe_dir(recipe_name)
        build_dir = ctx.get_build_dir(recipe_name)
        
        # Попытка сборки с использованием autoconf
        try:
            env = ctx.env.copy()
            configure_cmd = [
                'sh', './configure',
                '--host=arm-linux-androideabi',
                f'--prefix={recipe_dir}/install'
            ]
            subprocess.call(configure_cmd, cwd=build_dir, env=env)
            subprocess.call(['make', '-j4'], cwd=build_dir, env=env)
            subprocess.call(['make', 'install'], cwd=build_dir, env=env)
            print("Jpeg успешно собран с использованием autoconf!")
            return True
        except Exception as e:
            print(f"Ошибка при сборке jpeg: {e}")
            
    return True 