using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RFID_marks.Services
{
    /// <summary>
    /// Статический класс для логирования системных событий и ошибок
    /// </summary>
    public static class Logger
    {
        private static readonly object _lock = new object();
        private static string _logFilePath;
        private static bool _isInitialized;
        private static bool _logToConsole;
        private static bool _logToFile;
        private static LogLevel _minLogLevel;

        /// <summary>
        /// Инициализирует логгер с указанными параметрами
        /// </summary>
        /// <param name="logFilePath">Путь к файлу лога</param>
        /// <param name="logToConsole">Логировать в консоль</param>
        /// <param name="logToFile">Логировать в файл</param>
        /// <param name="minLogLevel">Минимальный уровень логирования</param>
        public static void Initialize(string logFilePath, bool logToConsole = true, bool logToFile = true, LogLevel minLogLevel = LogLevel.Info)
        {
            lock (_lock)
            {
                _logFilePath = logFilePath;
                _logToConsole = logToConsole;
                _logToFile = logToFile;
                _minLogLevel = minLogLevel;
                _isInitialized = true;

                // Создаем директорию для логов, если она не существует
                if (_logToFile && !string.IsNullOrEmpty(_logFilePath))
                {
                    string directoryPath = Path.GetDirectoryName(_logFilePath);
                    if (!string.IsNullOrEmpty(directoryPath) && !Directory.Exists(directoryPath))
                    {
                        Directory.CreateDirectory(directoryPath);
                    }
                }

                Info("Logger", "Логгер инициализирован");
            }
        }

        /// <summary>
        /// Проверяет, инициализирован ли логгер
        /// </summary>
        private static void EnsureInitialized()
        {
            if (!_isInitialized)
            {
                // Используем значения по умолчанию
                Initialize(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs", "app.log"));
            }
        }

        /// <summary>
        /// Регистрирует информационное сообщение
        /// </summary>
        /// <param name="source">Источник сообщения</param>
        /// <param name="message">Сообщение</param>
        public static void Info(string source, string message)
        {
            Log(LogLevel.Info, source, message);
        }

        /// <summary>
        /// Регистрирует предупреждение
        /// </summary>
        /// <param name="source">Источник сообщения</param>
        /// <param name="message">Сообщение</param>
        public static void Warning(string source, string message)
        {
            Log(LogLevel.Warning, source, message);
        }

        /// <summary>
        /// Регистрирует ошибку
        /// </summary>
        /// <param name="source">Источник сообщения</param>
        /// <param name="message">Сообщение</param>
        public static void Error(string source, string message)
        {
            Log(LogLevel.Error, source, message);
        }

        /// <summary>
        /// Регистрирует ошибку с исключением
        /// </summary>
        /// <param name="source">Источник сообщения</param>
        /// <param name="ex">Исключение</param>
        /// <param name="message">Дополнительное сообщение</param>
        public static void Error(string source, Exception ex, string message = null)
        {
            string errorMessage = string.IsNullOrEmpty(message)
                ? $"Исключение: {ex.Message}\nСтек: {ex.StackTrace}"
                : $"{message}\nИсключение: {ex.Message}\nСтек: {ex.StackTrace}";

            Log(LogLevel.Error, source, errorMessage);
        }

        /// <summary>
        /// Регистрирует отладочное сообщение
        /// </summary>
        /// <param name="source">Источник сообщения</param>
        /// <param name="message">Сообщение</param>
        public static void Debug(string source, string message)
        {
            Log(LogLevel.Debug, source, message);
        }

        /// <summary>
        /// Регистрирует сообщение с указанным уровнем
        /// </summary>
        /// <param name="level">Уровень сообщения</param>
        /// <param name="source">Источник сообщения</param>
        /// <param name="message">Сообщение</param>
        public static void Log(LogLevel level, string source, string message)
        {
            if (level < _minLogLevel) return;

            EnsureInitialized();

            string formattedMessage = FormatLogMessage(level, source, message);

            if (_logToConsole)
            {
                WriteToConsole(level, formattedMessage);
            }

            if (_logToFile)
            {
                WriteToFile(formattedMessage);
            }
        }

        /// <summary>
        /// Форматирует сообщение для лога
        /// </summary>
        /// <param name="level">Уровень сообщения</param>
        /// <param name="source">Источник сообщения</param>
        /// <param name="message">Сообщение</param>
        /// <returns>Отформатированное сообщение</returns>
        private static string FormatLogMessage(LogLevel level, string source, string message)
        {
            return $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}] [{level}] [{source}] {message}";
        }

        /// <summary>
        /// Записывает сообщение в консоль с соответствующим цветом
        /// </summary>
        /// <param name="level">Уровень сообщения</param>
        /// <param name="message">Сообщение</param>
        private static void WriteToConsole(LogLevel level, string message)
        {
            ConsoleColor originalColor = Console.ForegroundColor;

            switch (level)
            {
                case LogLevel.Debug:
                    Console.ForegroundColor = ConsoleColor.Gray;
                    break;
                case LogLevel.Info:
                    Console.ForegroundColor = ConsoleColor.White;
                    break;
                case LogLevel.Warning:
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    break;
                case LogLevel.Error:
                    Console.ForegroundColor = ConsoleColor.Red;
                    break;
                default:
                    break;
            }

            Console.WriteLine(message);
            Console.ForegroundColor = originalColor;
        }

        /// <summary>
        /// Записывает сообщение в файл
        /// </summary>
        /// <param name="message">Сообщение</param>
        private static void WriteToFile(string message)
        {
            if (string.IsNullOrEmpty(_logFilePath)) return;

            lock (_lock)
            {
                try
                {
                    // Добавляем запись в файл
                    File.AppendAllText(_logFilePath, message + Environment.NewLine, Encoding.UTF8);
                }
                catch (Exception ex)
                {
                    // В случае ошибки записи в файл, выводим в консоль
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine($"Ошибка записи в лог-файл: {ex.Message}");
                    Console.ResetColor();
                }
            }
        }

        /// <summary>
        /// Очищает файл лога
        /// </summary>
        public static void ClearLogFile()
        {
            EnsureInitialized();

            if (string.IsNullOrEmpty(_logFilePath)) return;

            lock (_lock)
            {
                try
                {
                    File.WriteAllText(_logFilePath, string.Empty);
                    Info("Logger", "Файл лога очищен");
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine($"Ошибка при очистке лог-файла: {ex.Message}");
                    Console.ResetColor();
                }
            }
        }

        /// <summary>
        /// Получает последние N записей из файла лога
        /// </summary>
        /// <param name="count">Количество записей</param>
        /// <returns>Список записей</returns>
        public static List<string> GetLastLogEntries(int count)
        {
            EnsureInitialized();

            if (string.IsNullOrEmpty(_logFilePath) || !File.Exists(_logFilePath))
                return new List<string>();

            lock (_lock)
            {
                try
                {
                    string[] allLines = File.ReadAllLines(_logFilePath);
                    return allLines.Skip(Math.Max(0, allLines.Length - count)).ToList();
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.DarkRed;
                    Console.WriteLine($"Ошибка при чтении лог-файла: {ex.Message}");
                    Console.ResetColor();
                    return new List<string>();
                }
            }
        }
    }

    /// <summary>
    /// Уровни логирования
    /// </summary>
    public enum LogLevel
    {
        /// <summary>
        /// Отладочная информация
        /// </summary>
        Debug = 0,

        /// <summary>
        /// Информационные сообщения
        /// </summary>
        Info = 1,

        /// <summary>
        /// Предупреждения
        /// </summary>
        Warning = 2,

        /// <summary>
        /// Ошибки
        /// </summary>
        Error = 3
    }
} 