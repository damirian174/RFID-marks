using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Threading;
using RFID_marks.Models;
using RFID_marks.Services;

namespace RFID_marks.Views
{
    /// <summary>
    /// Логика взаимодействия для страницы маркировки
    /// </summary>
    public partial class MarkPage : Page
    {
        private DatabaseService _databaseService;
        private SerialManager _serialManager;
        private Session _currentSession;
        private Detail _currentDetail;
        private Operation _currentOperation;
        private DispatcherTimer _sessionTimer;
        private DispatcherTimer _statusMessageTimer;
        private Dictionary<string, Operation> _operations;
        private List<OperationStep> _markingSteps;
        
        /// <summary>
        /// Конструктор страницы маркировки
        /// </summary>
        /// <param name="session">Текущая сессия пользователя</param>
        /// <param name="databaseService">Сервис работы с базой данных</param>
        /// <param name="serialManager">Менеджер для связи с RFID считывателем</param>
        public MarkPage(Session session, DatabaseService databaseService, SerialManager serialManager)
        {
            InitializeComponent();
            
            _databaseService = databaseService;
            _serialManager = serialManager;
            _currentSession = session;
            _operations = new Dictionary<string, Operation>();
            
            // Устанавливаем имя сотрудника
            EmployeeNameLabel.Content = $"Сотрудник: {_currentSession.EmployeeName}";
            
            // Настраиваем таймер сессии
            _sessionTimer = new DispatcherTimer();
            _sessionTimer.Interval = TimeSpan.FromSeconds(1);
            _sessionTimer.Tick += SessionTimer_Tick;
            _sessionTimer.Start();
            
            // Настраиваем таймер сообщений
            _statusMessageTimer = new DispatcherTimer();
            _statusMessageTimer.Interval = TimeSpan.FromSeconds(5);
            _statusMessageTimer.Tick += StatusMessageTimer_Tick;
            
            // Инициализируем шаги маркировки
            InitializeMarkingSteps();
            
            // Подписываемся на события
            _serialManager.DataReceived += SerialManager_DataReceived;
            
            // Устанавливаем начальное состояние
            UpdateStatusMessage("Страница маркировки загружена. Готова к работе.");
            UpdateControlsState();
            
            DetailIdTextBox.Focus();
        }
        
        /// <summary>
        /// Инициализация шагов маркировки
        /// </summary>
        private void InitializeMarkingSteps()
        {
            _markingSteps = new List<OperationStep>
            {
                new OperationStep("Загрузка детали", "Загрузка информации о детали из базы данных", 1),
                new OperationStep("Сканирование RFID", "Сканирование метки RFID для получения идентификатора", 2),
                new OperationStep("Запись данных", "Запись информации о детали на метку RFID", 3),
                new OperationStep("Проверка записи", "Верификация правильности записи данных на метку RFID", 4),
                new OperationStep("Сохранение", "Сохранение информации о маркировке в базе данных", 5)
            };
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку сканирования
        /// </summary>
        private void ScanButton_Click(object sender, RoutedEventArgs e)
        {
            string detailId = DetailIdTextBox.Text.Trim();
            
            if (string.IsNullOrEmpty(detailId))
            {
                UpdateStatusMessage("Пожалуйста, введите идентификатор детали", true);
                DetailIdTextBox.Focus();
                return;
            }
            
            // Получаем деталь из базы данных
            try
            {
                _currentDetail = _databaseService.GetDetail(detailId);
                
                if (_currentDetail == null)
                {
                    UpdateStatusMessage($"Деталь с идентификатором {detailId} не найдена", true);
                    return;
                }
                
                // Показываем информацию о детали
                UpdateDetailInfo();
                
                // Создаем операцию маркировки
                _currentOperation = new Operation(
                    "Маркировка", 
                    $"Маркировка детали {_currentDetail.Name} (#{_currentDetail.SerialNumber})", 
                    _currentSession.EmployeeId, 
                    _currentSession.EmployeeName, 
                    _currentDetail.Id);
                
                // Добавляем шаги
                foreach (var step in _markingSteps)
                {
                    _currentOperation.AddStep(step);
                }
                
                // Начинаем операцию
                _currentOperation.Start();
                
                // Переходим к следующему шагу - сканированию RFID
                _currentOperation.NextStep();
                
                // Обновляем состояние элементов управления
                UpdateStatusMessage("Деталь загружена. Поднесите RFID метку к считывателю.");
                UpdateControlsState();
                
                // Запрашиваем чтение RFID
                _serialManager.SendCommand("READ");
            }
            catch (Exception ex)
            {
                UpdateStatusMessage($"Ошибка при загрузке детали: {ex.Message}", true);
            }
        }
        
        /// <summary>
        /// Обработчик получения данных от считывателя RFID
        /// </summary>
        private void SerialManager_DataReceived(object sender, string data)
        {
            // Выполняем действие в UI потоке
            Dispatcher.Invoke(() =>
            {
                try
                {
                    if (_currentOperation == null || _currentDetail == null)
                    {
                        UpdateStatusMessage("Сначала необходимо загрузить деталь", true);
                        return;
                    }
                    
                    // Проверяем текущий шаг
                    if (_currentOperation.CurrentStep.Order == 2) // Сканирование RFID
                    {
                        // Предполагаем, что данные содержат UID метки
                        string rfidUid = data.Trim();
                        
                        if (string.IsNullOrEmpty(rfidUid))
                        {
                            UpdateStatusMessage("Не удалось считать RFID метку. Попробуйте снова.", true);
                            return;
                        }
                        
                        // Проверяем, не используется ли эта метка для другой детали
                        Detail existingDetail = _databaseService.GetDetailByRfidUid(rfidUid);
                        if (existingDetail != null && existingDetail.Id != _currentDetail.Id)
                        {
                            UpdateStatusMessage($"Метка уже используется для детали {existingDetail.Name} (#{existingDetail.SerialNumber})", true);
                            return;
                        }
                        
                        // Сохраняем UID метки
                        _currentDetail.RfidUid = rfidUid;
                        
                        // Обновляем информацию о RFID
                        RfidUidTextBox.Text = rfidUid;
                        
                        // Завершаем текущий шаг и переходим к следующему - записи данных
                        _currentOperation.NextStep();
                        
                        // Подготавливаем данные для записи
                        string dataToWrite = PrepareRfidData();
                        
                        // Обновляем информацию
                        RfidDataTextBox.Text = dataToWrite;
                        
                        // Запрашиваем запись RFID
                        _serialManager.SendCommand($"WRITE:{dataToWrite}");
                        
                        UpdateStatusMessage("RFID метка обнаружена. Выполняется запись данных...");
                    }
                    else if (_currentOperation.CurrentStep.Order == 3) // Запись данных
                    {
                        // Проверяем ответ на запись
                        if (data.Contains("ERROR"))
                        {
                            UpdateStatusMessage("Ошибка при записи данных на RFID метку: " + data, true);
                            _currentOperation.MarkError("Ошибка записи RFID: " + data);
                            return;
                        }
                        
                        // Завершаем текущий шаг и переходим к следующему - проверке записи
                        _currentOperation.NextStep();
                        
                        // Запрашиваем чтение RFID для проверки
                        _serialManager.SendCommand("READ");
                        
                        UpdateStatusMessage("Данные записаны. Проверка записи...");
                    }
                    else if (_currentOperation.CurrentStep.Order == 4) // Проверка записи
                    {
                        // Получаем записанные данные
                        string readData = data.Trim();
                        
                        // Проверяем соответствие записанных данных
                        string expectedData = PrepareRfidData();
                        
                        if (readData != expectedData)
                        {
                            UpdateStatusMessage("Ошибка проверки данных. Записанные данные не соответствуют ожидаемым.", true);
                            _currentOperation.MarkError("Ошибка верификации RFID: несоответствие данных");
                            return;
                        }
                        
                        // Сохраняем данные метки
                        _currentDetail.RfidData = readData;
                        
                        // Завершаем текущий шаг и переходим к следующему - сохранению данных
                        _currentOperation.NextStep();
                        
                        // Сохраняем информацию в базе данных
                        _currentDetail.Stage = "Маркировка";
                        _currentDetail.Status = "Промаркирован";
                        
                        // Сохраняем деталь в базе данных
                        _databaseService.UpdateDetail(_currentDetail);
                        
                        // Завершаем операцию
                        _currentOperation.Complete();
                        
                        // Сохраняем операцию в базе данных
                        _databaseService.AddOperation(_currentOperation);
                        
                        // Добавляем операцию в сессию
                        _currentSession.AddOperation(_currentOperation);
                        
                        // Обновляем счетчик маркированных деталей
                        MarkedPartsCountLabel.Content = $"Маркировано: {_currentSession.ProcessedParts.Count}";
                        
                        // Обновляем состояние элементов управления
                        UpdateStatusMessage("Маркировка детали успешно завершена!");
                        UpdateControlsState();
                        
                        // Сбрасываем текущую деталь и операцию
                        _currentDetail = null;
                        _currentOperation = null;
                        
                        // Очищаем поля ввода
                        DetailIdTextBox.Clear();
                        DetailIdTextBox.Focus();
                    }
                }
                catch (Exception ex)
                {
                    UpdateStatusMessage($"Ошибка при обработке RFID данных: {ex.Message}", true);
                    
                    if (_currentOperation != null)
                    {
                        _currentOperation.MarkError(ex.Message);
                    }
                }
            });
        }
        
        /// <summary>
        /// Подготавливает данные для записи на RFID метку
        /// </summary>
        private string PrepareRfidData()
        {
            // Формируем строку данных в формате:
            // ID|NAME|SERIAL|STATUS|DATE
            return $"{_currentDetail.Id}|{_currentDetail.Name}|{_currentDetail.SerialNumber}|{_currentDetail.Status}|{DateTime.Now:yyyyMMddHHmmss}";
        }
        
        /// <summary>
        /// Обновляет информацию о детали на UI
        /// </summary>
        private void UpdateDetailInfo()
        {
            if (_currentDetail != null)
            {
                DetailNameTextBox.Text = _currentDetail.Name;
                SerialNumberTextBox.Text = _currentDetail.SerialNumber;
                ArticleNumberTextBox.Text = _currentDetail.ArticleNumber;
                StatusTextBox.Text = _currentDetail.Status;
                StageTextBox.Text = _currentDetail.Stage;
                RfidUidTextBox.Text = _currentDetail.RfidUid ?? "Не присвоен";
                RfidDataTextBox.Text = _currentDetail.RfidData ?? "Не записаны";
            }
            else
            {
                DetailNameTextBox.Clear();
                SerialNumberTextBox.Clear();
                ArticleNumberTextBox.Clear();
                StatusTextBox.Clear();
                StageTextBox.Clear();
                RfidUidTextBox.Clear();
                RfidDataTextBox.Clear();
            }
        }
        
        /// <summary>
        /// Обновляет статусное сообщение
        /// </summary>
        /// <param name="message">Сообщение</param>
        /// <param name="isError">Признак ошибки</param>
        private void UpdateStatusMessage(string message, bool isError = false)
        {
            StatusMessageTextBlock.Text = message;
            
            // Устанавливаем цвет в зависимости от типа сообщения
            StatusMessageTextBlock.Foreground = isError 
                ? System.Windows.Media.Brushes.Red 
                : System.Windows.Media.Brushes.Green;
            
            // Если это не ошибка, запускаем таймер для очистки сообщения
            if (!isError)
            {
                _statusMessageTimer.Stop();
                _statusMessageTimer.Start();
            }
            
            // Добавляем сообщение в историю операций
            OperationsListBox.Items.Add($"[{DateTime.Now:HH:mm:ss}] {message}");
            OperationsListBox.ScrollIntoView(OperationsListBox.Items[OperationsListBox.Items.Count - 1]);
        }
        
        /// <summary>
        /// Обработчик таймера сообщений
        /// </summary>
        private void StatusMessageTimer_Tick(object sender, EventArgs e)
        {
            _statusMessageTimer.Stop();
            StatusMessageTextBlock.Text = "Готов к работе";
            StatusMessageTextBlock.Foreground = System.Windows.Media.Brushes.Black;
        }
        
        /// <summary>
        /// Обработчик таймера сессии
        /// </summary>
        private void SessionTimer_Tick(object sender, EventArgs e)
        {
            SessionTimeLabel.Content = $"Время сессии: {_currentSession.TotalTime}";
        }
        
        /// <summary>
        /// Обновляет состояние элементов управления
        /// </summary>
        private void UpdateControlsState()
        {
            bool isDetailLoaded = _currentDetail != null;
            bool isOperationInProgress = _currentOperation != null && _currentOperation.Status == "Выполняется";
            
            // Настраиваем доступность контролов
            DetailIdTextBox.IsEnabled = !isOperationInProgress;
            ScanButton.IsEnabled = !isOperationInProgress;
            WriteManuallyButton.IsEnabled = isDetailLoaded && !isOperationInProgress;
            CancelButton.IsEnabled = isOperationInProgress;
            
            // Обновляем информацию о текущей операции
            if (isOperationInProgress && _currentOperation.CurrentStep != null)
            {
                CurrentStepTextBlock.Text = $"Текущий шаг: {_currentOperation.CurrentStep.Name}";
            }
            else
            {
                CurrentStepTextBlock.Text = "Текущий шаг: -";
            }
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку отмены
        /// </summary>
        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            if (_currentOperation != null)
            {
                // Отмечаем операцию как ошибочную
                _currentOperation.MarkError("Операция отменена пользователем");
                
                // Сохраняем операцию в базе данных
                _databaseService.AddOperation(_currentOperation);
                
                // Добавляем операцию в сессию
                _currentSession.AddOperation(_currentOperation);
                
                // Сбрасываем текущую операцию
                _currentOperation = null;
                
                // Обновляем состояние элементов управления
                UpdateStatusMessage("Операция отменена");
                UpdateControlsState();
                
                // Очищаем поля ввода
                DetailIdTextBox.Clear();
                DetailIdTextBox.Focus();
            }
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку ручной записи
        /// </summary>
        private void WriteManuallyButton_Click(object sender, RoutedEventArgs e)
        {
            if (_currentDetail == null)
            {
                UpdateStatusMessage("Сначала необходимо загрузить деталь", true);
                return;
            }
            
            // Открываем диалог для ввода RFID UID
            string rfidUid = Microsoft.VisualBasic.Interaction.InputBox(
                "Введите UID RFID метки:", 
                "Ручной ввод RFID", 
                "", 
                -1, 
                -1);
            
            if (string.IsNullOrEmpty(rfidUid))
            {
                return;
            }
            
            // Проверяем, не используется ли эта метка для другой детали
            Detail existingDetail = _databaseService.GetDetailByRfidUid(rfidUid);
            if (existingDetail != null && existingDetail.Id != _currentDetail.Id)
            {
                UpdateStatusMessage($"Метка уже используется для детали {existingDetail.Name} (#{existingDetail.SerialNumber})", true);
                return;
            }
            
            // Создаем операцию маркировки
            _currentOperation = new Operation(
                "Маркировка (ручная)", 
                $"Ручная маркировка детали {_currentDetail.Name} (#{_currentDetail.SerialNumber})", 
                _currentSession.EmployeeId, 
                _currentSession.EmployeeName, 
                _currentDetail.Id);
            
            // Начинаем операцию
            _currentOperation.Start();
            
            // Сохраняем UID метки
            _currentDetail.RfidUid = rfidUid;
            
            // Подготавливаем данные
            string dataToWrite = PrepareRfidData();
            _currentDetail.RfidData = dataToWrite;
            
            // Обновляем информацию о RFID
            RfidUidTextBox.Text = rfidUid;
            RfidDataTextBox.Text = dataToWrite;
            
            // Обновляем статус детали
            _currentDetail.Stage = "Маркировка";
            _currentDetail.Status = "Промаркирован";
            
            // Сохраняем деталь в базе данных
            _databaseService.UpdateDetail(_currentDetail);
            
            // Завершаем операцию
            _currentOperation.Complete();
            
            // Сохраняем операцию в базе данных
            _databaseService.AddOperation(_currentOperation);
            
            // Добавляем операцию в сессию
            _currentSession.AddOperation(_currentOperation);
            
            // Обновляем счетчик маркированных деталей
            MarkedPartsCountLabel.Content = $"Маркировано: {_currentSession.ProcessedParts.Count}";
            
            // Обновляем состояние элементов управления
            UpdateStatusMessage("Ручная маркировка детали успешно завершена!");
            UpdateControlsState();
            
            // Сбрасываем текущую деталь и операцию
            _currentDetail = null;
            _currentOperation = null;
            
            // Очищаем поля ввода
            DetailIdTextBox.Clear();
            DetailIdTextBox.Focus();
        }
        
        /// <summary>
        /// Обработчик нажатия на кнопку поиска
        /// </summary>
        private void SearchButton_Click(object sender, RoutedEventArgs e)
        {
            // Открываем диалог поиска детали
            SearchDialog searchDialog = new SearchDialog(_databaseService);
            if (searchDialog.ShowDialog() == true)
            {
                // Если деталь выбрана, загружаем ее
                Detail selectedDetail = searchDialog.SelectedDetail;
                if (selectedDetail != null)
                {
                    _currentDetail = selectedDetail;
                    DetailIdTextBox.Text = _currentDetail.Id;
                    UpdateDetailInfo();
                    UpdateStatusMessage($"Загружена деталь {_currentDetail.Name} (#{_currentDetail.SerialNumber})");
                    UpdateControlsState();
                }
            }
        }
        
        /// <summary>
        /// Обработчик события нажатия клавиши в поле ввода ID детали
        /// </summary>
        private void DetailIdTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                ScanButton_Click(sender, null);
            }
        }
        
        /// <summary>
        /// Освобождение ресурсов при выгрузке страницы
        /// </summary>
        public void Unload()
        {
            // Останавливаем таймеры
            _sessionTimer.Stop();
            _statusMessageTimer.Stop();
            
            // Отписываемся от событий
            _serialManager.DataReceived -= SerialManager_DataReceived;
        }
    }
} 