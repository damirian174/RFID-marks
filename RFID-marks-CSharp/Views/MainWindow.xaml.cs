using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Threading;
using Newtonsoft.Json.Linq;
using RFID_marks.Models;
using RFID_marks.Services;

namespace RFID_marks.Views
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private readonly Logger _logger = new Logger();
        private readonly DatabaseService _databaseService = new DatabaseService();
        private SerialManager _serialManager;
        private SerialListener _serialListener;
        private DispatcherTimer _rotationTimer;
        private double _angle = 0;
        private bool _isVerified = false;
        private string _uid;

        // Правильный хеш пароля администратора
        private readonly string _correctPasswordHash = GetHashString("Метран");

        // Основные страницы приложения
        private WorkPage _workPage;
        private MarkPage _markPage;
        private TestPage _testPage;
        private PackingPage _packingPage;
        private AdminPage _adminPage;

        public MainWindow()
        {
            InitializeComponent();
            
            _logger.LogEvent("Главное окно приложения создано");

            // Инициализация МЭТР
            InitializeMetr();

            // Запускаем анимацию загрузочного экрана
            SetupLoadingAnimation();

            // Обработчик события закрытия окна
            Closing += MainWindow_Closing;
        }

        /// <summary>
        /// Обработчик закрытия главного окна
        /// </summary>
        private void MainWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _logger.LogEvent("Закрытие приложения");
            
            try
            {
                if (Config.SessionOn)
                {
                    _logger.LogEvent($"Завершаем сессию пользователя: {Config.Name}");
                    
                    // Разбиваем полное имя на части
                    string[] nameParts = Config.Name.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                    string lastName = nameParts.Length > 0 ? nameParts[0] : "";
                    string firstName = nameParts.Length > 1 ? nameParts[1] : "";
                    
                    JObject data = new JObject
                    {
                        ["type"] = "endSession",
                        ["name"] = firstName,
                        ["surname"] = lastName
                    };
                    
                    JObject worker = _databaseService.ExecuteRequest(data);
                    
                    if (worker != null && worker["status"]?.ToString() == "ok")
                    {
                        _logger.LogEvent($"Сессия успешно завершена: {lastName} {firstName}");
                        Config.SessionOn = false;
                    }
                    else
                    {
                        _logger.LogError($"Не удалось завершить сессию: {lastName} {firstName}");
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Ошибка при завершении сессии: {ex.Message}");
            }

            // Останавливаем слушатель COM-порта
            _serialListener?.Stop();
            
            // Закрываем COM-порт
            if (_serialManager != null)
            {
                _serialManager.Close();
                SerialManager.ResetInstance();
            }
        }

        /// <summary>
        /// Инициализация МЭТР
        /// </summary>
        private void InitializeMetr()
        {
            try
            {
                string port = SerialManager.FindMetrPort();
                
                if (!string.IsNullOrEmpty(port))
                {
                    _serialManager = SerialManager.Initialize(port, 9600);
                    
                    if (_serialManager != null)
                    {
                        _serialListener = new SerialListener(_serialManager);
                        _serialListener.DataReceived += SerialListener_DataReceived;
                        _serialListener.ConnectionLost += SerialListener_ConnectionLost;
                        _serialListener.Start();
                        
                        _logger.LogEvent($"Подключен к МЭТР через порт {port}");
                        Config.ConnectStatus = true;
                    }
                }
                else
                {
                    _logger.LogError("Не найден подходящий COM-порт");
                    Config.ConnectStatus = false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Ошибка при инициализации МЭТР: {ex.Message}");
                Config.ConnectStatus = false;
            }
        }

        /// <summary>
        /// Обработчик события получения данных с COM-порта
        /// </summary>
        private void SerialListener_DataReceived(object sender, string[] data)
        {
            // Выполняем в потоке UI
            Dispatcher.Invoke(() =>
            {
                HandleSerialData(data);
            });
        }

        /// <summary>
        /// Обработчик события потери соединения с COM-портом
        /// </summary>
        private void SerialListener_ConnectionLost(object sender, EventArgs e)
        {
            // Выполняем в потоке UI
            Dispatcher.Invoke(() =>
            {
                _logger.LogError("Потеряно соединение с МЭТР");
                
                MessageBox.Show(
                    "Потеряно соединение с МЭТР.\nНачинается автоматическое переподключение...",
                    "Потеря соединения",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);
                
                // Пытаемся переподключиться через 2 секунды
                Task.Delay(2000).ContinueWith(_ =>
                {
                    Dispatcher.Invoke(() =>
                    {
                        ReconnectMetr();
                    });
                });
            });
        }

        /// <summary>
        /// Переподключение к МЭТР
        /// </summary>
        private void ReconnectMetr()
        {
            try
            {
                // Показываем информационное сообщение
                MessageBox.Show(
                    "Выполняется переподключение к МЭТР...",
                    "Переподключение",
                    MessageBoxButton.OK,
                    MessageBoxImage.Information);
                
                // Останавливаем слушатель COM-порта
                _serialListener?.Stop();
                
                // Закрываем COM-порт
                if (_serialManager != null)
                {
                    _serialManager.Close();
                    SerialManager.ResetInstance();
                }
                
                // Находим МЭТР
                string metrPort = SerialManager.FindMetrPort();
                
                if (!string.IsNullOrEmpty(metrPort))
                {
                    // Создаем новый SerialManager
                    _serialManager = SerialManager.Initialize(metrPort, 9600);
                    
                    if (_serialManager != null)
                    {
                        // Создаем и запускаем новый слушатель
                        _serialListener = new SerialListener(_serialManager);
                        _serialListener.DataReceived += SerialListener_DataReceived;
                        _serialListener.ConnectionLost += SerialListener_ConnectionLost;
                        _serialListener.Start();
                        
                        _logger.LogEvent($"МЭТР успешно подключен через порт {metrPort}");
                        Config.ConnectStatus = true;
                        
                        MessageBox.Show(
                            $"МЭТР успешно подключен через порт {metrPort}",
                            "Переподключение",
                            MessageBoxButton.OK,
                            MessageBoxImage.Information);
                    }
                    else
                    {
                        _logger.LogError("Не удалось создать SerialManager");
                        Config.ConnectStatus = false;
                        
                        MessageBox.Show(
                            "Не удалось подключиться к МЭТР",
                            "Ошибка",
                            MessageBoxButton.OK,
                            MessageBoxImage.Error);
                    }
                }
                else
                {
                    _logger.LogError("МЭТР не найден при попытке переподключения");
                    Config.ConnectStatus = false;
                    
                    MessageBox.Show(
                        "МЭТР не найден. Проверьте подключение",
                        "Ошибка",
                        MessageBoxButton.OK,
                        MessageBoxImage.Warning);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Ошибка при переподключении к МЭТР: {ex.Message}");
                Config.ConnectStatus = false;
                
                MessageBox.Show(
                    $"Ошибка при переподключении: {ex.Message}",
                    "Ошибка",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error);
            }
        }

        /// <summary>
        /// Обработка данных с COM-порта
        /// </summary>
        private void HandleSerialData(string[] data)
        {
            if (data == null || data.Length < 2)
            {
                _logger.LogEvent($"Ошибка: Данные пришли в неверном формате или пустые: {string.Join(", ", data ?? new string[0])}");
                return;
            }

            _logger.LogEvent($"Данные перед очисткой: {string.Join(", ", data)}");

            // Очистка данных и проверка
            string[] cleanedData = data;
            
            _logger.LogEvent($"Очищенные данные: {string.Join(", ", cleanedData)}");

            if (cleanedData.Length < 2)
            {
                _logger.LogEvent($"Ошибка: Данные после очистки все еще неверные: {string.Join(", ", cleanedData)}");
                return;
            }

            if (cleanedData[1] == "detail")
            {
                if (Config.Auth)
                {
                    _logger.LogEvent($"Получены данные из порта: {cleanedData[0]}");
                    // Здесь будет вызов GetDetail из DetailService
                    // DetailService.GetDetail(cleanedData[0]);
                }
            }
            else if (cleanedData[1] == "user")
            {
                _logger.LogEvent($"Пользователь с UID: {cleanedData[0]}");
                _uid = cleanedData[0];
                Verify();
            }
            else
            {
                _logger.LogEvent($"Неизвестный формат данных: {string.Join(", ", cleanedData)}");
            }
        }

        /// <summary>
        /// Проверка пользователя
        /// </summary>
        private async void Verify()
        {
            // Проверяем, прошел ли пользователь верификацию
            if (_isVerified || Config.Data)
            {
                return;
            }

            JObject data = new JObject
            {
                ["type"] = "user",
                ["uid"] = string.IsNullOrEmpty(ManualInput.Text) ? _uid : ManualInput.Text
            };
            
            _logger.LogEvent($"Попытка аутентификации пользователя с UID: {data["uid"]}");
            
            // Показываем индикатор загрузки
            SplashScreen.Visibility = Visibility.Visible;
            
            try
            {
                JObject response = await Task.Run(() => _databaseService.ExecuteRequest(data));
                
                // Скрываем индикатор загрузки
                SplashScreen.Visibility = Visibility.Collapsed;
                
                _logger.LogEvent($"Ответ сервера: {response}");
                
                if (response != null && response["status"]?.ToString() == "ok")
                {
                    // Проверяем, в каком формате приходят данные
                    JObject userData;
                    
                    if (response["data"] != null)
                    {
                        userData = (JObject)response["data"];
                        _logger.LogEvent($"Данные пользователя в поле data: {userData}");
                    }
                    else
                    {
                        userData = response;
                        _logger.LogEvent($"Данные пользователя в корне ответа: {userData}");
                    }
                    
                    // Проверяем наличие необходимых полей
                    string surname = userData["surname"]?.ToString();
                    string name = userData["name"]?.ToString();
                    
                    if (string.IsNullOrEmpty(surname) || string.IsNullOrEmpty(name))
                    {
                        _logger.LogError($"Отсутствуют обязательные поля в ответе: {userData}");
                        
                        MessageBox.Show(
                            "Не удалось получить данные пользователя. Попробуйте еще раз.",
                            "Ошибка",
                            MessageBoxButton.OK,
                            MessageBoxImage.Error);
                        
                        return;
                    }
                    
                    string fullName = $"{surname} {name}";
                    _isVerified = true;
                    
                    MessageBoxResult result = MessageBox.Show(
                        $"Вы {fullName}?",
                        "Подтверждение",
                        MessageBoxButton.YesNo,
                        MessageBoxImage.Question,
                        MessageBoxResult.No);
                    
                    if (result == MessageBoxResult.Yes)
                    {
                        Config.Data = true;
                        
                        // Создаем сессию, если есть соединение с сервером
                        if (Config.ConnectStatus)
                        {
                            JObject sessionData = new JObject
                            {
                                ["type"] = "startSession",
                                ["name"] = name,
                                ["surname"] = surname,
                                ["work_description"] = "Без детали"
                            };
                            
                            _logger.LogEvent($"Запрос на создание сессии: {sessionData}");
                            
                            JObject sessionResponse = await Task.Run(() => _databaseService.ExecuteRequest(sessionData));
                            
                            _logger.LogEvent($"Ответ на создание сессии: {sessionResponse}");
                            
                            if (sessionResponse != null && sessionResponse["status"]?.ToString() == "ok")
                            {
                                _logger.LogEvent($"Сессия успешно начата: {fullName}");
                                Config.SessionOn = true;
                            }
                            else
                            {
                                _logger.LogError($"Не удалось начать сессию: {fullName}, ответ: {sessionResponse}");
                            }
                        }
                        
                        // Устанавливаем переменные для пользователя
                        _logger.LogEvent($"Устанавливаем переменную Config.User: {fullName}");
                        Config.User = fullName;
                        
                        _logger.LogEvent($"Устанавливаем переменную Config.Name: {surname} {name}");
                        Config.Name = $"{surname} {name}";
                        
                        _logger.LogEvent($"Установлено значение Config.Name: {Config.Name}");
                        
                        // Устанавливаем ID пользователя
                        Config.Id = userData["id"] != null ? Convert.ToInt32(userData["id"]) : 0;
                        
                        // Переход на рабочую страницу
                        // TODO: Здесь будет создание и переход на страницу Work
                        // MainFrame.Navigate(new WorkPage());
                        
                        _logger.LogEvent($"Успешная аутентификация пользователя: {fullName}");
                        Config.Auth = true;
                        _isVerified = false;
                    }
                    else
                    {
                        Config.Auth = false;
                        Config.Data = null;
                        Config.User = null;
                        _isVerified = false;
                        _logger.LogError($"Не удалось аутентифицировать пользователя: {_uid}");
                    }
                }
                else if (response != null && response["status"]?.ToString() == "error" && 
                         response["message"]?.ToString().Contains("У пользователя уже есть активная сессия") == true)
                {
                    _logger.LogError($"У пользователя уже есть активная сессия: {_uid}");
                    
                    MessageBoxResult result = MessageBox.Show(
                        "У пользователя уже есть активная сессия",
                        "Предупреждение",
                        MessageBoxButton.OKCancel,
                        MessageBoxImage.Warning,
                        MessageBoxResult.Cancel,
                        MessageBoxOptions.DefaultDesktopOnly);
                    
                    if (result == MessageBoxResult.OK)
                    {
                        // Получаем данные о пользователе без создания новой сессии
                        JObject userDataRequest = new JObject
                        {
                            ["type"] = "user",
                            ["uid"] = _uid
                        };
                        
                        JObject userDataResponse = await Task.Run(() => _databaseService.ExecuteRequest(userDataRequest));
                        
                        if (userDataResponse != null)
                        {
                            JObject userData = userDataResponse["data"] != null 
                                ? (JObject)userDataResponse["data"] 
                                : userDataResponse;
                                
                            string surname = userData["surname"]?.ToString();
                            string name = userData["name"]?.ToString();
                            
                            if (!string.IsNullOrEmpty(surname) && !string.IsNullOrEmpty(name))
                            {
                                string fullName = $"{surname} {name}";
                                Config.Data = true;
                                
                                // Устанавливаем необходимые переменные без отправки startSession
                                Config.User = fullName;
                                Config.Name = $"{surname} {name}";
                                Config.Id = userData["id"] != null ? Convert.ToInt32(userData["id"]) : 0;
                                Config.SessionOn = true;  // Считаем сессию активной
                                
                                // Переход на рабочую страницу
                                // TODO: Здесь будет создание и переход на страницу Work
                                // MainFrame.Navigate(new WorkPage());
                                
                                _logger.LogEvent($"Пользователь {fullName} вошел с существующей сессией");
                                Config.Auth = true;
                                _isVerified = false;
                            }
                            else
                            {
                                _logger.LogError($"Не удалось получить данные пользователя: {userData}");
                                
                                MessageBox.Show(
                                    "Не удалось получить данные пользователя",
                                    "Ошибка",
                                    MessageBoxButton.OK,
                                    MessageBoxImage.Error);
                            }
                        }
                        else
                        {
                            _logger.LogError($"Ошибка получения данных пользователя: {userDataResponse}");
                            
                            MessageBox.Show(
                                "Ошибка получения данных пользователя",
                                "Ошибка",
                                MessageBoxButton.OK,
                                MessageBoxImage.Error);
                        }
                    }
                }
                else
                {
                    _logger.LogError($"Ошибка аутентификации: {response}");
                    
                    MessageBox.Show(
                        "Ошибка аутентификации. Проверьте ID или попробуйте позже.",
                        "Ошибка",
                        MessageBoxButton.OK,
                        MessageBoxImage.Error);
                }
            }
            catch (Exception ex)
            {
                // Скрываем индикатор загрузки
                SplashScreen.Visibility = Visibility.Collapsed;
                
                _logger.LogError($"Ошибка при проверке пользователя: {ex.Message}");
                
                MessageBox.Show(
                    $"Произошла ошибка при проверке пользователя: {ex.Message}",
                    "Ошибка",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error);
            }
        }

        /// <summary>
        /// Настройка анимации загрузочного экрана
        /// </summary>
        private void SetupLoadingAnimation()
        {
            // Создаем таймер
            _rotationTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(10)
            };
            
            // Добавляем обработчик события таймера
            _rotationTimer.Tick += (s, e) =>
            {
                // Увеличиваем угол для поворота
                _angle = (_angle + 5) % 360;
                
                // Применяем поворот к изображению
                LoadingImage.RenderTransform = new RotateTransform(_angle, LoadingImage.ActualWidth / 2, LoadingImage.ActualHeight / 2);
            };
        }

        /// <summary>
        /// Обработчик события нажатия клавиши в поле ввода
        /// </summary>
        private void ManualInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                Verify();
            }
        }

        /// <summary>
        /// Обработчик события нажатия кнопки подтверждения
        /// </summary>
        private void ConfirmButton_Click(object sender, RoutedEventArgs e)
        {
            _uid = ManualInput.Text;
            Verify();
        }

        /// <summary>
        /// Получить хеш строки
        /// </summary>
        private static string GetHashString(string input)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(input));
                StringBuilder builder = new StringBuilder();
                
                foreach (byte b in bytes)
                {
                    builder.Append(b.ToString("x2"));
                }
                
                return builder.ToString();
            }
        }
    }
} 