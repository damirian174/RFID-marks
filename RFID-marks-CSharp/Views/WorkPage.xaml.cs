using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;
using RFID_marks.Models;
using RFID_marks.Services;

namespace RFID_marks.Views
{
    /// <summary>
    /// Логика взаимодействия для WorkPage.xaml
    /// </summary>
    public partial class WorkPage : Page
    {
        private readonly DatabaseService _databaseService;
        private DispatcherTimer _timer;
        private DateTime _startTime;
        private TimeSpan _elapsedTime;
        private bool _isRunning = false;
        private string _detailId;

        /// <summary>
        /// Конструктор страницы сборки
        /// </summary>
        public WorkPage()
        {
            InitializeComponent();
            
            // Инициализация сервисов
            _databaseService = new DatabaseService();
            
            // Инициализация таймера
            _timer = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(1)
            };
            
            _timer.Tick += Timer_Tick;
            
            // Инициализация UI элементов
            UpdateUI();
        }
        
        /// <summary>
        /// Обработчик события таймера
        /// </summary>
        private void Timer_Tick(object sender, EventArgs e)
        {
            if (_isRunning)
            {
                _elapsedTime = DateTime.Now - _startTime;
                UpdateTimerDisplay();
            }
        }
        
        /// <summary>
        /// Обновляет отображение таймера
        /// </summary>
        private void UpdateTimerDisplay()
        {
            TimerBlock.Text = $"{_elapsedTime.Hours:00}:{_elapsedTime.Minutes:00}:{_elapsedTime.Seconds:00}";
            SessionTimeBlock.Text = TimerBlock.Text;
        }
        
        /// <summary>
        /// Запускает таймер работы
        /// </summary>
        public void StartTimer()
        {
            if (!_isRunning)
            {
                _startTime = DateTime.Now;
                _timer.Start();
                _isRunning = true;
            }
        }
        
        /// <summary>
        /// Останавливает таймер работы
        /// </summary>
        public void StopTimer()
        {
            if (_isRunning)
            {
                _timer.Stop();
                _isRunning = false;
            }
        }
        
        /// <summary>
        /// Продолжает таймер работы
        /// </summary>
        public void ContinueTimer()
        {
            if (!_isRunning)
            {
                _startTime = DateTime.Now - _elapsedTime;
                _timer.Start();
                _isRunning = true;
            }
        }
        
        /// <summary>
        /// Сбрасывает таймер работы
        /// </summary>
        public void ResetTimer()
        {
            StopTimer();
            _elapsedTime = TimeSpan.Zero;
            UpdateTimerDisplay();
        }
        
        /// <summary>
        /// Обновляет имя пользователя на странице
        /// </summary>
        /// <param name="userName">Имя пользователя</param>
        public void UpdateUserName(string userName)
        {
            UserNameBlock.Text = userName ?? "Не авторизован";
        }
        
        /// <summary>
        /// Обновляет информацию о детали
        /// </summary>
        /// <param name="detail">Объект детали</param>
        public void UpdateDetailInfo(Detail detail)
        {
            if (detail != null)
            {
                DetailNameBlock.Text = detail.Name ?? "Не указано";
                SerialNumberBlock.Text = detail.SerialNumber ?? "Не указано";
                StageBlock.Text = detail.Status ?? "Сборка";
                _detailId = detail.Id;
                
                // Добавляем запись в историю операций
                AddOperationToHistory($"Деталь {detail.Name} (SN: {detail.SerialNumber}) отсканирована");
                
                StatusMessageBlock.Text = $"Деталь {detail.Name} готова к сборке";
                StartWorkButton.IsEnabled = true;
            }
            else
            {
                DetailNameBlock.Text = "Не выбрана";
                SerialNumberBlock.Text = "Не задан";
                StageBlock.Text = "Сборка";
                _detailId = null;
                
                StatusMessageBlock.Text = "Деталь не выбрана";
                StartWorkButton.IsEnabled = false;
            }
            
            UpdateUI();
        }
        
        /// <summary>
        /// Обновляет состояние элементов интерфейса
        /// </summary>
        private void UpdateUI()
        {
            bool detailSelected = !string.IsNullOrEmpty(_detailId);
            
            switch (StatusTextBlock.Text)
            {
                case "В работе":
                    StatusIndicator.Fill = Brushes.Green;
                    StartWorkButton.IsEnabled = false;
                    PauseWorkButton.IsEnabled = true;
                    ContinueWorkButton.IsEnabled = false;
                    CompleteWorkButton.IsEnabled = true;
                    break;
                    
                case "Приостановлено":
                    StatusIndicator.Fill = Brushes.Orange;
                    StartWorkButton.IsEnabled = false;
                    PauseWorkButton.IsEnabled = false;
                    ContinueWorkButton.IsEnabled = true;
                    CompleteWorkButton.IsEnabled = true;
                    break;
                    
                case "Завершено":
                    StatusIndicator.Fill = Brushes.Red;
                    StartWorkButton.IsEnabled = false;
                    PauseWorkButton.IsEnabled = false;
                    ContinueWorkButton.IsEnabled = false;
                    CompleteWorkButton.IsEnabled = false;
                    break;
                    
                default: // "Ожидание"
                    StatusIndicator.Fill = Brushes.Gray;
                    StartWorkButton.IsEnabled = detailSelected;
                    PauseWorkButton.IsEnabled = false;
                    ContinueWorkButton.IsEnabled = false;
                    CompleteWorkButton.IsEnabled = false;
                    break;
            }
            
            ScanDetailButton.IsEnabled = true;
        }
        
        /// <summary>
        /// Добавляет запись в историю операций
        /// </summary>
        /// <param name="operationText">Текст операции</param>
        private void AddOperationToHistory(string operationText)
        {
            OperationHistoryList.Items.Insert(0, $"[{DateTime.Now:HH:mm:ss}] {operationText}");
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку "Начать работу"
        /// </summary>
        private async void StartWorkButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusMessageBlock.Text = "Начало работы...";
                
                // Проверяем, что деталь выбрана
                if (string.IsNullOrEmpty(_detailId))
                {
                    MessageBox.Show("Сначала отсканируйте деталь", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                    StatusMessageBlock.Text = "Деталь не выбрана";
                    return;
                }
                
                // Отправляем запрос на начало работы
                bool success = await _databaseService.StartWorkAsync(Config.Id, _detailId);
                
                if (success)
                {
                    StatusTextBlock.Text = "В работе";
                    StartTimer();
                    AddOperationToHistory("Начало работы");
                    StatusMessageBlock.Text = "Работа начата";
                    
                    UpdateUI();
                }
                else
                {
                    MessageBox.Show("Не удалось начать работу. Попробуйте еще раз.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    StatusMessageBlock.Text = "Ошибка при начале работы";
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("Ошибка при начале работы", ex);
                MessageBox.Show($"Ошибка при начале работы: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusMessageBlock.Text = "Ошибка при начале работы";
            }
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку "Приостановить работу"
        /// </summary>
        private async void PauseWorkButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusMessageBlock.Text = "Приостановка работы...";
                
                // Отправляем запрос на приостановку работы
                bool success = await _databaseService.PauseWorkAsync(Config.Id, _detailId);
                
                if (success)
                {
                    StatusTextBlock.Text = "Приостановлено";
                    StopTimer();
                    AddOperationToHistory("Работа приостановлена");
                    StatusMessageBlock.Text = "Работа приостановлена";
                    
                    UpdateUI();
                }
                else
                {
                    MessageBox.Show("Не удалось приостановить работу. Попробуйте еще раз.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    StatusMessageBlock.Text = "Ошибка при приостановке работы";
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("Ошибка при приостановке работы", ex);
                MessageBox.Show($"Ошибка при приостановке работы: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusMessageBlock.Text = "Ошибка при приостановке работы";
            }
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку "Продолжить работу"
        /// </summary>
        private async void ContinueWorkButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusMessageBlock.Text = "Продолжение работы...";
                
                // Отправляем запрос на продолжение работы
                bool success = await _databaseService.ContinueWorkAsync(Config.Id, _detailId);
                
                if (success)
                {
                    StatusTextBlock.Text = "В работе";
                    ContinueTimer();
                    AddOperationToHistory("Работа продолжена");
                    StatusMessageBlock.Text = "Работа продолжена";
                    
                    UpdateUI();
                }
                else
                {
                    MessageBox.Show("Не удалось продолжить работу. Попробуйте еще раз.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    StatusMessageBlock.Text = "Ошибка при продолжении работы";
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("Ошибка при продолжении работы", ex);
                MessageBox.Show($"Ошибка при продолжении работы: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusMessageBlock.Text = "Ошибка при продолжении работы";
            }
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку "Завершить работу"
        /// </summary>
        private async void CompleteWorkButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Запрашиваем подтверждение
                MessageBoxResult result = MessageBox.Show(
                    "Вы уверены, что хотите завершить работу?",
                    "Подтверждение",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Question);
                    
                if (result == MessageBoxResult.No)
                {
                    return;
                }
                
                StatusMessageBlock.Text = "Завершение работы...";
                
                // Отправляем запрос на завершение работы
                bool success = await _databaseService.EndWorkAsync(Config.Id, _detailId);
                
                if (success)
                {
                    StatusTextBlock.Text = "Завершено";
                    StopTimer();
                    AddOperationToHistory($"Работа завершена. Общее время: {_elapsedTime.Hours:00}:{_elapsedTime.Minutes:00}:{_elapsedTime.Seconds:00}");
                    StatusMessageBlock.Text = "Работа завершена";
                    
                    UpdateUI();
                    
                    // Сбрасываем таймер и состояние через некоторое время
                    await System.Threading.Tasks.Task.Delay(3000);
                    ResetState();
                }
                else
                {
                    MessageBox.Show("Не удалось завершить работу. Попробуйте еще раз.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                    StatusMessageBlock.Text = "Ошибка при завершении работы";
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("Ошибка при завершении работы", ex);
                MessageBox.Show($"Ошибка при завершении работы: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusMessageBlock.Text = "Ошибка при завершении работы";
            }
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку "Отсканировать деталь"
        /// </summary>
        private void ScanDetailButton_Click(object sender, RoutedEventArgs e)
        {
            // Создаем диалог ввода штрих-кода
            var inputDialog = new InputDialog("Введите штрих-код детали");
            
            if (inputDialog.ShowDialog() == true)
            {
                // Пользователь ввел штрих-код
                string barcode = inputDialog.InputValue;
                
                if (!string.IsNullOrWhiteSpace(barcode))
                {
                    // Загружаем информацию о детали
                    GetDetailInfo(barcode);
                }
            }
        }
        
        /// <summary>
        /// Загружает информацию о детали по ID или штрих-коду
        /// </summary>
        /// <param name="detailIdentifier">ID или штрих-код детали</param>
        private async void GetDetailInfo(string detailIdentifier)
        {
            try
            {
                StatusMessageBlock.Text = "Получение информации о детали...";
                
                var detail = await _databaseService.GetDetailAsync(detailIdentifier);
                
                if (detail != null)
                {
                    UpdateDetailInfo(detail);
                }
                else
                {
                    MessageBox.Show("Деталь не найдена", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                    StatusMessageBlock.Text = "Деталь не найдена";
                    
                    DetailNameBlock.Text = "Не выбрана";
                    SerialNumberBlock.Text = "Не задан";
                    StageBlock.Text = "Сборка";
                    _detailId = null;
                    
                    UpdateUI();
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("Ошибка при получении информации о детали", ex);
                MessageBox.Show($"Ошибка при получении информации о детали: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusMessageBlock.Text = "Ошибка при получении информации о детали";
            }
        }
        
        /// <summary>
        /// Сбрасывает состояние страницы
        /// </summary>
        private void ResetState()
        {
            ResetTimer();
            StatusTextBlock.Text = "Ожидание";
            _detailId = null;
            DetailNameBlock.Text = "Не выбрана";
            SerialNumberBlock.Text = "Не задан";
            StageBlock.Text = "Сборка";
            StatusMessageBlock.Text = "Готов к работе";
            
            UpdateUI();
        }
        
        /// <summary>
        /// Запрашивает подтверждение завершения сессии
        /// </summary>
        /// <returns>True, если пользователь подтвердил</returns>
        public bool ConfirmEndSession()
        {
            if (_isRunning)
            {
                MessageBoxResult result = MessageBox.Show(
                    "У вас есть активная работа. Вы уверены, что хотите закончить сессию?",
                    "Подтверждение",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Warning);
                    
                return result == MessageBoxResult.Yes;
            }
            
            return true;
        }
    }
    
    /// <summary>
    /// Диалог для ввода значения
    /// </summary>
    public class InputDialog : Window
    {
        private TextBox _textBox;
        
        public string InputValue => _textBox.Text;
        
        public InputDialog(string prompt)
        {
            Title = "Ввод данных";
            Width = 400;
            Height = 150;
            WindowStartupLocation = WindowStartupLocation.CenterOwner;
            ResizeMode = ResizeMode.NoResize;
            
            Grid grid = new Grid();
            grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Auto) });
            grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Auto) });
            grid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Auto) });
            
            TextBlock promptBlock = new TextBlock
            {
                Text = prompt,
                Margin = new Thickness(10, 10, 10, 5),
                TextAlignment = TextAlignment.Center
            };
            
            _textBox = new TextBox
            {
                Margin = new Thickness(10),
                Padding = new Thickness(5),
                VerticalContentAlignment = VerticalAlignment.Center
            };
            
            StackPanel buttonPanel = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 5, 0, 10)
            };
            
            Button okButton = new Button
            {
                Content = "OK",
                Width = 75,
                Height = 30,
                Margin = new Thickness(5),
                IsDefault = true
            };
            
            Button cancelButton = new Button
            {
                Content = "Отмена",
                Width = 75,
                Height = 30,
                Margin = new Thickness(5),
                IsCancel = true
            };
            
            okButton.Click += (s, e) => 
            {
                DialogResult = true;
                Close();
            };
            
            buttonPanel.Children.Add(okButton);
            buttonPanel.Children.Add(cancelButton);
            
            Grid.SetRow(promptBlock, 0);
            Grid.SetRow(_textBox, 1);
            Grid.SetRow(buttonPanel, 2);
            
            grid.Children.Add(promptBlock);
            grid.Children.Add(_textBox);
            grid.Children.Add(buttonPanel);
            
            Content = grid;
            
            Loaded += (s, e) => _textBox.Focus();
        }
    }
} 