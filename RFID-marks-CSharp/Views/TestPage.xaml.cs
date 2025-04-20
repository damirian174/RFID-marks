using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;
using RFID_marks.Models;
using RFID_marks.Services;

namespace RFID_marks.Views
{
    /// <summary>
    /// Логика взаимодействия для TestPage.xaml
    /// </summary>
    public partial class TestPage : Page
    {
        private readonly DatabaseService _databaseService;
        private Detail _currentDetail;
        private User _currentUser;
        private DispatcherTimer _timer;
        private Stopwatch _stopwatch;
        private bool _isTestRunning = false;
        
        // История операций
        private List<string> _operationHistory = new List<string>();
        
        // Журнал тестов
        private List<TestRecord> _testLog = new List<TestRecord>();

        public TestPage()
        {
            InitializeComponent();
            
            _databaseService = new DatabaseService();
            _stopwatch = new Stopwatch();
            
            // Инициализация таймера
            _timer = new DispatcherTimer();
            _timer.Tick += TimerTick;
            _timer.Interval = TimeSpan.FromSeconds(1);
            
            // Инициализация UI
            TestTypeComboBox.SelectedIndex = 0;
            TestPassedRadio.IsChecked = true;
            
            // Загрузка журнала тестов (если есть)
            LoadTestLogs();
            
            // Блокировка кнопок до выбора детали
            UpdateUIState(false);
        }
        
        #region Обработчики событий таймера

        private void TimerTick(object sender, EventArgs e)
        {
            UpdateTimerDisplay();
            
            if (_isTestRunning)
            {
                // Проверка, не вышло ли время теста (если задано)
                if (int.TryParse(TestTimeTextBox.Text, out int testTimeSeconds) && 
                    _stopwatch.Elapsed.TotalSeconds >= testTimeSeconds)
                {
                    // Автоматическое завершение теста по таймеру
                    StopTest();
                    MessageBox.Show("Время теста истекло.", "Завершение теста", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }
        }
        
        private void UpdateTimerDisplay()
        {
            TimeSpan ts = _stopwatch.Elapsed;
            TimerBlock.Text = string.Format("{0:00}:{1:00}:{2:00}", 
                ts.Hours, ts.Minutes, ts.Seconds);
            SessionTimeBlock.Text = TimerBlock.Text;
        }
        
        private void StartTimer()
        {
            _stopwatch.Start();
            _timer.Start();
            UpdateTimerDisplay();
        }
        
        private void StopTimer()
        {
            _stopwatch.Stop();
            _timer.Stop();
            UpdateTimerDisplay();
        }
        
        private void ResetTimer()
        {
            _stopwatch.Reset();
            UpdateTimerDisplay();
        }

        #endregion
        
        #region Взаимодействие с БД
        
        private void LoadTestLogs()
        {
            try
            {
                // Получение журнала тестов из БД
                _testLog = _databaseService.GetTestRecords();
                
                // Обновление UI
                TestLogListBox.Items.Clear();
                foreach (var test in _testLog)
                {
                    TestLogListBox.Items.Add($"{test.DateTime.ToString("dd.MM.yyyy HH:mm")} - {test.DetailName} ({test.TestType}) - {(test.Passed ? "Пройден" : "Не пройден")}");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при загрузке журнала тестов: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        
        private void SaveTestRecord(bool passed)
        {
            if (_currentDetail == null) return;
            
            var testRecord = new TestRecord
            {
                DetailId = _currentDetail.Id,
                DetailName = _currentDetail.Name,
                UserId = _currentUser?.Id ?? 0,
                UserName = _currentUser?.Username ?? "Неавторизованный пользователь",
                TestType = TestTypeComboBox.Text,
                Params = TestParamsTextBox.Text,
                Requirements = TestRequirementsTextBox.Text,
                Conclusion = ConclusionTextBox.Text,
                Passed = passed,
                DateTime = DateTime.Now
            };
            
            try
            {
                // Сохранение в БД
                _databaseService.SaveTestRecord(testRecord);
                
                // Обновление журнала
                LoadTestLogs();
                
                // Добавление записи в историю операций
                string result = passed ? "пройден" : "не пройден";
                AddOperationHistoryRecord($"Тест '{testRecord.TestType}' {result}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сохранении результатов теста: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        
        #endregion
        
        #region Управление UI
        
        /// <summary>
        /// Обновление состояния элементов интерфейса
        /// </summary>
        private void UpdateUIState(bool detailSelected)
        {
            // Управление доступностью кнопок
            StartTestButton.IsEnabled = detailSelected && !_isTestRunning;
            SaveResultsButton.IsEnabled = detailSelected && _isTestRunning;
            CompleteTestButton.IsEnabled = detailSelected && _isTestRunning;
            
            // Управление полями ввода
            bool editEnabled = detailSelected && _isTestRunning;
            TestParamsTextBox.IsEnabled = editEnabled;
            TestRequirementsTextBox.IsEnabled = editEnabled;
            Measurement1TextBox.IsEnabled = editEnabled;
            Measurement2TextBox.IsEnabled = editEnabled;
            Measurement3TextBox.IsEnabled = editEnabled;
            Threshold1TextBox.IsEnabled = editEnabled;
            Threshold2TextBox.IsEnabled = editEnabled;
            Threshold3TextBox.IsEnabled = editEnabled;
            ConclusionTextBox.IsEnabled = editEnabled;
            TestPassedRadio.IsEnabled = editEnabled;
            TestFailedRadio.IsEnabled = editEnabled;
            
            // Настройка индикатора статуса
            if (!detailSelected)
            {
                StatusIndicator.Fill = Brushes.Gray;
                StatusTextBlock.Text = "Ожидание";
            }
            else if (_isTestRunning)
            {
                StatusIndicator.Fill = Brushes.Green;
                StatusTextBlock.Text = "Тестирование";
            }
            else
            {
                StatusIndicator.Fill = Brushes.Orange;
                StatusTextBlock.Text = "Готов";
            }
        }
        
        /// <summary>
        /// Обновление информации о пользователе
        /// </summary>
        public void UpdateUserInfo(User user)
        {
            _currentUser = user;
            
            if (user != null)
            {
                UserNameBlock.Text = $"{user.Username} ({user.Role})";
            }
            else
            {
                UserNameBlock.Text = "Не авторизован";
            }
        }
        
        /// <summary>
        /// Обновление информации о детали
        /// </summary>
        private void UpdateDetailInfo(Detail detail)
        {
            if (detail != null)
            {
                DetailNameBlock.Text = detail.Name;
                SerialNumberBlock.Text = detail.SerialNumber;
                
                // Обновление истории операций
                LoadOperationHistory(detail.Id);
                
                // Обновление UI
                UpdateUIState(true);
                
                // Добавление записи в историю
                AddOperationHistoryRecord("Деталь отсканирована");
                
                // Статус
                StatusMessageBlock.Text = "Деталь готова к тестированию";
            }
            else
            {
                DetailNameBlock.Text = "Не выбрана";
                SerialNumberBlock.Text = "Не задан";
                
                // Очистка истории операций
                OperationHistoryList.Items.Clear();
                
                // Обновление UI
                UpdateUIState(false);
                
                // Статус
                StatusMessageBlock.Text = "Необходимо отсканировать деталь";
            }
        }
        
        /// <summary>
        /// Загрузка истории операций для детали
        /// </summary>
        private void LoadOperationHistory(int detailId)
        {
            try
            {
                // Получение истории операций из БД
                _operationHistory = _databaseService.GetDetailOperationHistory(detailId);
                
                // Обновление UI
                OperationHistoryList.Items.Clear();
                foreach (var operation in _operationHistory)
                {
                    OperationHistoryList.Items.Add(operation);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при загрузке истории операций: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        
        /// <summary>
        /// Добавление новой записи в историю операций
        /// </summary>
        private void AddOperationHistoryRecord(string operation)
        {
            if (_currentDetail == null) return;
            
            try
            {
                // Сохранение в БД
                _databaseService.AddDetailOperation(_currentDetail.Id, operation);
                
                // Добавление в локальный список
                string record = $"{DateTime.Now.ToString("dd.MM.yyyy HH:mm:ss")} - {operation}";
                _operationHistory.Add(record);
                
                // Обновление UI
                OperationHistoryList.Items.Add(record);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при добавлении записи в историю операций: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        
        /// <summary>
        /// Запуск процесса тестирования
        /// </summary>
        private void StartTest()
        {
            if (_currentDetail == null) return;
            
            _isTestRunning = true;
            
            // Обновление UI
            UpdateUIState(true);
            
            // Запуск таймера
            ResetTimer();
            StartTimer();
            
            // Добавление записи в историю операций
            AddOperationHistoryRecord($"Начато тестирование: {TestTypeComboBox.Text}");
            
            // Статус
            StatusMessageBlock.Text = $"Выполняется тест: {TestTypeComboBox.Text}";
        }
        
        /// <summary>
        /// Остановка процесса тестирования
        /// </summary>
        private void StopTest()
        {
            _isTestRunning = false;
            
            // Обновление UI
            UpdateUIState(true);
            
            // Остановка таймера
            StopTimer();
            
            // Добавление записи в историю операций
            AddOperationHistoryRecord($"Завершено тестирование: {TestTypeComboBox.Text}");
            
            // Статус
            StatusMessageBlock.Text = "Тестирование завершено";
        }
        
        #endregion
        
        #region Обработчики событий UI
        
        private void ScanDetailButton_Click(object sender, RoutedEventArgs e)
        {
            // В реальном приложении здесь был бы код для сканирования RFID-метки
            // В демо-версии просто создаем тестовую деталь
            
            _currentDetail = new Detail
            {
                Id = 1,
                Name = "Тестовая деталь",
                SerialNumber = "SN-" + DateTime.Now.ToString("yyyyMMddHHmmss"),
                Stage = "Тестирование"
            };
            
            // Обновление UI
            UpdateDetailInfo(_currentDetail);
        }
        
        private void StartTestButton_Click(object sender, RoutedEventArgs e)
        {
            StartTest();
        }
        
        private void SaveResultsButton_Click(object sender, RoutedEventArgs e)
        {
            bool passed = TestPassedRadio.IsChecked ?? false;
            SaveTestRecord(passed);
            
            MessageBox.Show("Результаты тестирования сохранены.", "Сохранение", MessageBoxButton.OK, MessageBoxImage.Information);
        }
        
        private void CompleteTestButton_Click(object sender, RoutedEventArgs e)
        {
            StopTest();
            
            // Показываем диалог сохранения результатов
            MessageBoxResult result = MessageBox.Show(
                "Сохранить результаты тестирования?", 
                "Завершение теста", 
                MessageBoxButton.YesNo, 
                MessageBoxImage.Question);
                
            if (result == MessageBoxResult.Yes)
            {
                bool passed = TestPassedRadio.IsChecked ?? false;
                SaveTestRecord(passed);
            }
        }
        
        private void TestTypeComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // Настройка формы в зависимости от выбранного типа теста
            string testType = ((ComboBoxItem)TestTypeComboBox.SelectedItem).Content.ToString();
            
            switch (testType)
            {
                case "Функциональный тест":
                    TestTimeTextBox.Text = "120";
                    TestParamsTextBox.Text = "Проверка основных функций";
                    TestRequirementsTextBox.Text = "Все функции должны работать без ошибок";
                    break;
                    
                case "Тест RF-метки":
                    TestTimeTextBox.Text = "30";
                    TestParamsTextBox.Text = "Проверка считывания/записи RF-метки";
                    TestRequirementsTextBox.Text = "Метка должна успешно считываться и записываться";
                    break;
                    
                case "Тест маркировки":
                    TestTimeTextBox.Text = "60";
                    TestParamsTextBox.Text = "Проверка качества маркировки";
                    TestRequirementsTextBox.Text = "Маркировка должна быть четкой и соответствовать требованиям";
                    break;
                    
                case "Комплексный тест":
                    TestTimeTextBox.Text = "180";
                    TestParamsTextBox.Text = "Полная проверка всех функций и компонентов";
                    TestRequirementsTextBox.Text = "Все тесты должны быть пройдены успешно";
                    break;
            }
        }
        
        private void TestLogListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            int selectedIndex = TestLogListBox.SelectedIndex;
            if (selectedIndex >= 0 && selectedIndex < _testLog.Count)
            {
                var selectedTest = _testLog[selectedIndex];
                
                // Заполнение полей выбранного теста
                foreach (ComboBoxItem item in TestTypeComboBox.Items)
                {
                    if (item.Content.ToString() == selectedTest.TestType)
                    {
                        TestTypeComboBox.SelectedItem = item;
                        break;
                    }
                }
                
                TestParamsTextBox.Text = selectedTest.Params;
                TestRequirementsTextBox.Text = selectedTest.Requirements;
                ConclusionTextBox.Text = selectedTest.Conclusion;
                
                if (selectedTest.Passed)
                    TestPassedRadio.IsChecked = true;
                else
                    TestFailedRadio.IsChecked = true;
            }
        }
        
        #endregion
    }
    
    /// <summary>
    /// Класс для хранения информации о тесте
    /// </summary>
    public class TestRecord
    {
        public int Id { get; set; }
        public int DetailId { get; set; }
        public string DetailName { get; set; }
        public int UserId { get; set; }
        public string UserName { get; set; }
        public string TestType { get; set; }
        public string Params { get; set; }
        public string Requirements { get; set; }
        public string Conclusion { get; set; }
        public bool Passed { get; set; }
        public DateTime DateTime { get; set; }
    }
} 