using System;

namespace RFID_marks.Models
{
    /// <summary>
    /// Класс для хранения глобальных настроек приложения
    /// </summary>
    public static class Config
    {
        // Информация о пользователе
        public static string User { get; set; }
        public static string Name { get; set; }
        public static int Id { get; set; }
        public static bool Auth { get; set; }
        public static bool Data { get; set; }
        public static bool ConnectStatus { get; set; }
        public static bool SessionOn { get; set; }
        
        // Информация о детали
        public static string DetailName { get; set; }
        public static string DetailSerial { get; set; }
        
        // Информация о соединении
        public static string Port { get; set; }
        public static int BaudRate { get; set; } = 9600;
        
        // Настройки сервера
        public static string ServerAddress { get; set; } = "localhost";
        public static int ServerPort { get; set; } = 12345;
        
        // Пути к ресурсам
        public static string ResourcesPath { get; set; } = "Resources";
        public static string ImagesPath { get; set; } = "Resources/Images";
        public static string LogsPath { get; set; } = "Logs";
        
        // Настройки логирования
        public static bool EnableLogging { get; set; } = true;
        public static bool EnableDebugLogging { get; set; } = false;
        
        static Config()
        {
            // Инициализация конфигурации при первом обращении
            Auth = false;
            ConnectStatus = false;
            Data = false;
            SessionOn = false;
        }
        
        /// <summary>
        /// Сбросить все состояния приложения
        /// </summary>
        public static void ResetAll()
        {
            User = null;
            Name = null;
            Id = 0;
            Auth = false;
            Data = false;
            SessionOn = false;
            DetailName = null;
            DetailSerial = null;
        }
    }
} 