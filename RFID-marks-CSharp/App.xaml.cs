using System;
using System.IO;
using System.Windows;
using RFID_marks.Services;

namespace RFID_marks
{
    /// <summary>
    /// Логика взаимодействия для App.xaml
    /// </summary>
    public partial class App : Application
    {
        private readonly Logger _logger = new Logger();

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            
            _logger.LogEvent("Приложение запущено");
            
            AppDomain.CurrentDomain.UnhandledException += CurrentDomain_UnhandledException;
            
            // Проверка соединения с сервером при запуске
            CheckServerConnection();
        }

        protected override void OnExit(ExitEventArgs e)
        {
            _logger.LogEvent("Приложение завершено");
            
            base.OnExit(e);
        }

        private void CurrentDomain_UnhandledException(object sender, UnhandledExceptionEventArgs e)
        {
            Exception ex = e.ExceptionObject as Exception;
            _logger.LogError($"Необработанное исключение: {ex?.Message}");
            _logger.LogError($"Стек вызовов: {ex?.StackTrace}");
            
            MessageBox.Show($"Произошла непредвиденная ошибка:\n{ex?.Message}\n\nПриложение будет закрыто.", 
                "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            
            if (e.IsTerminating)
            {
                Environment.Exit(1);
            }
        }

        private void CheckServerConnection()
        {
            try
            {
                DatabaseService databaseService = new DatabaseService();
                bool isConnected = databaseService.TestConnection();
                
                if (isConnected)
                {
                    _logger.LogEvent("Соединение с сервером установлено");
                    Models.Config.ConnectStatus = true;
                }
                else
                {
                    _logger.LogError("Ошибка соединения с сервером");
                    
                    MessageBoxResult result = MessageBox.Show(
                        "Нет соединения с сервером!\nПроверьте подключение к Wi-Fi или обратитесь к системному администратору.",
                        "Ошибка соединения",
                        MessageBoxButton.OKCancel,
                        MessageBoxImage.Warning);
                    
                    if (result == MessageBoxResult.Cancel)
                    {
                        _logger.LogEvent("Пользователь выбрал выход из программы");
                        Shutdown(1);
                    }
                    else
                    {
                        _logger.LogEvent("Пользователь выбрал продолжить без соединения");
                        Models.Config.ConnectStatus = false;
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Ошибка при проверке соединения: {ex.Message}");
                
                MessageBoxResult result = MessageBox.Show(
                    $"Ошибка при подключении к серверу: {ex.Message}\nПродолжить работу без соединения?",
                    "Ошибка соединения",
                    MessageBoxButton.OKCancel,
                    MessageBoxImage.Warning);
                
                if (result == MessageBoxResult.Cancel)
                {
                    Shutdown(1);
                }
                else
                {
                    Models.Config.ConnectStatus = false;
                }
            }
        }
    }
} 