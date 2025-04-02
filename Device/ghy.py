import psutil
import time
import subprocess
import threading
from win32gui import GetWindowText, GetForegroundWindow, EnumWindows, GetClassName
from win32api import MessageBox
from win32con import MB_ICONWARNING, MB_OK, MB_SYSTEMMODAL, MB_TASKMODAL
from datetime import datetime
import socket
from collections import defaultdict
import re
import tkinter as tk
from tkinter import font as tkfont
import os
import sys
import win32com.client
import winreg

# Список блокируемых URL
BLOCKED_URLS = [
    "yandex.ru/games",
    "yandex.ru/igry",
    "yandex.ru/play",
    "games.yandex",
    "yandex.games",
    "ya.ru/games"
]

# Список браузеров для мониторинга
BROWSERS = [
    "chrome.exe",
    "firefox.exe",
    "msedge.exe",
    "opera.exe",
    "brave.exe",
    "browser.exe",  # Яндекс браузер
    "yabrowser.exe"  # Альтернативное имя Яндекс браузера
]

# Кэш для хранения результатов проверки URL
url_cache = defaultdict(lambda: {"url": None, "timestamp": 0})
CACHE_DURATION = 5  # секунды

# Выключение режима отладки
DEBUG_MODE = False

# Дополнительные регулярные выражения для блокировки
REGEX_PATTERNS = [
    r'(yandex|яндекс).*?(игры|games|play)'
]

def debug_print(message):
    if DEBUG_MODE:
        pass  # Ничего не выводим

def get_domain_from_ip(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return ip

def get_browser_url(pid):
    current_time = time.time()
    
    # Проверяем кэш
    if current_time - url_cache[pid]["timestamp"] < CACHE_DURATION:
        return url_cache[pid]["url"]
    
    try:
        # Получаем все сетевые соединения
        connections = psutil.net_connections(kind='inet')
        
        # Фильтруем соединения для конкретного процесса
        for conn in connections:
            if conn.pid == pid and conn.status == 'ESTABLISHED' and conn.raddr:
                # Получаем домен из IP
                domain = get_domain_from_ip(conn.raddr.ip)
                debug_print(f"Найдено соединение для PID {pid}: {domain} (IP: {conn.raddr.ip})")
                
                # Обновляем кэш
                url_cache[pid]["url"] = domain
                url_cache[pid]["timestamp"] = current_time
                
                return domain
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        debug_print(f"Ошибка при получении соединений для PID {pid}: {e}")
    
    return None

def get_all_browser_windows():
    """Получает заголовки всех окон браузеров"""
    windows = []
    
    def enum_windows_callback(hwnd, results):
        class_name = GetClassName(hwnd)
        if class_name and ("Chrome" in class_name or "Mozilla" in class_name or "Edge" in class_name):
            title = GetWindowText(hwnd)
            if title:
                results.append(title)
        return True
    
    EnumWindows(enum_windows_callback, windows)
    return windows

def is_url_blocked(url):
    if not url:
        return False
    
    url = url.lower()
    debug_print(f"Проверка URL: {url}")
    
    for blocked_url in BLOCKED_URLS:
        if blocked_url.lower() in url:
            debug_print(f"URL содержит блокируемый URL: {blocked_url}")
            return True
    
    # Ищем по регулярному выражению
    for pattern in REGEX_PATTERNS:
        if re.search(pattern, url):
            debug_print(f"URL соответствует регулярному выражению для Яндекс.Игр")
            return True
        
    return False

def block_browser(browser_name, window_title, count):
    """Функция для отображения полноэкранного предупреждения о блокировке"""
    blocked_type = "Яндекс.Игры"
    
    # Создаем полноэкранное окно с предупреждением
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(background="red")
    root.title("ВНИМАНИЕ: НАРУШЕНИЕ ЗАКОНОДАТЕЛЬСТВА!")
    
    # Делаем окно поверх всех других окон
    root.attributes("-topmost", True)
    
    # Заголовок
    header_font = tkfont.Font(family="Arial", size=36, weight="bold")
    header = tk.Label(root, text="ВНИМАНИЕ! НАРУШЕНИЕ ЗАКОНОДАТЕЛЬСТВА РФ", 
                     bg="red", fg="white", font=header_font)
    header.pack(pady=50)
    
    # Статья УК РФ
    law_font = tkfont.Font(family="Arial", size=24, weight="bold")
    law_text = tk.Label(root, 
                       text="Статья 134 УК РФ: Половое сношение и иные действия\nсексуального характера с лицом, не достигшим 16 лет",
                       bg="red", fg="white", font=law_font)
    law_text.pack(pady=30)
    
    # Информация о нарушении
    info_font = tkfont.Font(family="Arial", size=20)
    
    info_text = f"""
    Зафиксирована попытка доступа к запрещенному ресурсу: {blocked_type}
    
    Время нарушения: {datetime.now().strftime('%H:%M:%S  %d.%m.%Y')}
    Браузер: {browser_name}
    URL: {window_title}
    
    Данный инцидент зарегистрирован в системе.
    Количество нарушений: {count + 1}
    
    В соответствии с законодательством РФ, доступ к данному ресурсу запрещен.
    """
    
    info = tk.Label(root, text=info_text, bg="red", fg="white", font=info_font, justify="left")
    info.pack(pady=30)
    
    # Кнопка подтверждения
    button_font = tkfont.Font(family="Arial", size=16, weight="bold")
    confirm_button = tk.Button(root, text="Я ОСОЗНАЮ ОТВЕТСТВЕННОСТЬ И ОБЯЗУЮСЬ НЕ ПОВТОРЯТЬ", 
                              font=button_font, command=root.destroy,
                              bg="white", fg="red", padx=20, pady=10)
    confirm_button.pack(pady=50)
    
    # Обработка нажатий клавиш для предотвращения закрытия окна
    def disable_event(event):
        return "break"
    
    # Блокируем закрытие окна через Alt+F4 и другие комбинации
    root.bind("<Alt-F4>", disable_event)
    root.bind("<Escape>", disable_event)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Запускаем окно
    root.mainloop()

def kill_browsers():
    """Закрывает все браузеры"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if any(browser in proc.info['name'].lower() for browser in BROWSERS):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def block_browser_with_yandex_games():
    blocked_count = 0
    last_print_time = 0
    last_warning_time = 0  # Время последнего предупреждения
    
    while True:
        try:
            current_time = time.time()
            
            # Очищаем старые записи из кэша каждые 60 секунд
            if current_time - last_print_time > 60:
                url_cache.clear()
                debug_print("Кэш очищен")
                last_print_time = current_time
            
            # Проверяем, прошло ли достаточно времени с последнего предупреждения (минимум 5 секунд)
            if current_time - last_warning_time < 5:
                time.sleep(1)
                continue
            
            # Получаем все окна браузеров
            browser_windows = get_all_browser_windows()
            debug_print(f"Найдено окон браузеров: {len(browser_windows)}")
            
            # Список для хранения процессов, которые нужно закрыть
            procs_to_kill = []
            block_info = None
            
            # Проверяем заголовки окон
            for window_title in browser_windows:
                debug_print(f"Проверка окна: {window_title}")
                if is_url_blocked(window_title):
                    debug_print(f"Заблокировано по заголовку окна: {window_title}")
                    # Запоминаем информацию о блокировке
                    block_info = (window_title, "заголовок окна")
                    break
            
            # Если не нашли по заголовкам, ищем по соединениям
            if not block_info:
                for proc in psutil.process_iter(['pid', 'name', 'username']):
                    try:
                        proc_name = proc.info['name'].lower()
                        if any(browser in proc_name for browser in BROWSERS):
                            debug_print(f"Проверка браузера: {proc_name} (PID: {proc.info['pid']})")
                            
                            # Проверяем активное окно
                            window_title = GetWindowText(GetForegroundWindow())
                            debug_print(f"Заголовок активного окна: {window_title}")
                            
                            # Проверяем URL через сетевые соединения
                            current_url = get_browser_url(proc.info['pid'])
                            debug_print(f"Обнаруженный URL: {current_url}")
                            
                            if is_url_blocked(window_title) or is_url_blocked(current_url):
                                # Запоминаем информацию о блокировке
                                block_info = (window_title, proc_name)
                                procs_to_kill.append(proc)
                                break
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        debug_print(f"Ошибка при проверке процесса: {e}")
                        continue
            
            # Если нашли что-то для блокировки
            if block_info:
                window_title, browser_name = block_info
                blocked_count += 1
                last_warning_time = time.time()
                
                # СНАЧАЛА закрываем все браузеры с запрещенными URL
                kill_browsers()
                
                # ПОТОМ показываем предупреждение
                block_browser(browser_name, window_title, blocked_count)
                        
        except Exception as e:
            debug_print(f"Ошибка: {e}")
        
        time.sleep(1)

# Функция для добавления программы в автозапуск
def add_to_startup():
    try:
        # Получаем путь к исполняемому файлу
        if getattr(sys, 'frozen', False):
            # Для exe-файла, созданного PyInstaller
            app_path = sys.executable
        else:
            # Для скрипта Python
            app_path = os.path.abspath(__file__)
        
        # Имя программы для автозапуска
        app_name = "BrowserMonitor"
        
        # Открываем ключ реестра для автозапуска
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        
        # Проверяем, существует ли уже такая запись
        try:
            value, _ = winreg.QueryValueEx(key, app_name)
            if value == app_path:
                # Запись уже существует
                return
        except:
            # Записи нет, добавляем
            pass
        
        # Добавляем программу в автозапуск через реестр
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
        
        # Также создадим ярлык в папке автозагрузки для надежности
        startup_folder = os.path.join(
            os.environ["APPDATA"], 
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        
        shortcut_path = os.path.join(startup_folder, f"{app_name}.lnk")
        
        # Проверяем, существует ли уже ярлык
        if not os.path.exists(shortcut_path):
            # Создаем ярлык
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.Description = "Монитор браузеров для защиты от нежелательного контента"
            shortcut.IconLocation = app_path
            shortcut.save()
    
    except Exception as e:
        debug_print(f"Ошибка при добавлении в автозапуск: {e}")

if __name__ == "__main__":
    try:
        # Добавляем программу в автозапуск при первом запуске
        add_to_startup()
        
        # Запускаем основной мониторинг
        block_browser_with_yandex_games()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        debug_print(f"Критическая ошибка: {e}")