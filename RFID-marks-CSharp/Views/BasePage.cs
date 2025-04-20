using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using RFID_marks.Models;
using RFID_marks.Services;

namespace RFID_marks.Views
{
    /// <summary>
    /// Базовый класс для всех страниц приложения
    /// </summary>
    public class BasePage : Page
    {
        protected readonly Logger _logger = new Logger();
        protected readonly SerialManager _serialManager;

        private string _userName;
        private string _detailName;
        private string _detailSerial;

        /// <summary>
        /// Конструктор базовой страницы
        /// </summary>
        public BasePage()
        {
            try
            {
                // Пытаемся получить экземпляр SerialManager
                _serialManager = SerialManager.Instance;
            }
            catch (Exception ex)
            {
                _logger.LogError($"Ошибка при получении экземпляра SerialManager: {ex.Message}");
            }

            // Устанавливаем данные из конфигурации
            _userName = Config.User;
            _detailName = Config.DetailName;
            _detailSerial = Config.DetailSerial;
        }

        /// <summary>
        /// Обновить имя пользователя
        /// </summary>
        public virtual void UpdateName(string name)
        {
            _userName = name;
            _logger.LogEvent($"Обновлено имя пользователя: {name}");
        }

        /// <summary>
        /// Обновить информацию о детали
        /// </summary>
        public virtual void UpdateDetail(string name, string serial)
        {
            _detailName = name;
            _detailSerial = serial;
            _logger.LogEvent($"Обновлена информация о детали: {name}, {serial}");
        }

        /// <summary>
        /// Получить информацию о пользователе
        /// </summary>
        protected string UserName => _userName ?? Config.User ?? "Не авторизован";

        /// <summary>
        /// Получить название детали
        /// </summary>
        protected string DetailName => _detailName ?? Config.DetailName ?? "Нет данных";

        /// <summary>
        /// Получить серийный номер детали
        /// </summary>
        protected string DetailSerial => _detailSerial ?? Config.DetailSerial ?? "Нет данных";

        /// <summary>
        /// Подтвердить завершение сессии
        /// </summary>
        public virtual bool ConfirmEndSession()
        {
            MessageBoxResult result = MessageBox.Show(
                "Вы хотите закончить работу?",
                "Подтверждение",
                MessageBoxButton.YesNo,
                MessageBoxImage.Question,
                MessageBoxResult.No);

            return result == MessageBoxResult.Yes;
        }

        /// <summary>
        /// Изменить цвет индикатора подключения
        /// </summary>
        public virtual void ChangeConnectionColor(int status)
        {
            // Реализация в дочерних классах
        }

        /// <summary>
        /// Получить цвет в зависимости от статуса подключения
        /// </summary>
        protected SolidColorBrush GetConnectionColor(int status)
        {
            switch (status)
            {
                case 0: // Подключено
                    return new SolidColorBrush(Colors.Green);
                case 1: // Отключено
                    return new SolidColorBrush(Colors.Red);
                case 2: // Ожидание
                    return new SolidColorBrush(Colors.Orange);
                default:
                    return new SolidColorBrush(Colors.Gray);
            }
        }

        /// <summary>
        /// Стилизовать диалоговое окно
        /// </summary>
        public void StyleMessageBox(MessageBox messageBox)
        {
            if (messageBox != null)
            {
                // В WPF прямое стилизование MessageBox невозможно, 
                // для подобной функциональности нужно создать свой пользовательский диалог
            }
        }
    }
} 