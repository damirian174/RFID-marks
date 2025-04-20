using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Threading;
using RFID_marks_CSharp.Models;
using RFID_marks_CSharp.Services;

namespace RFID_marks_CSharp.Views
{
    /// <summary>
    /// Логика взаимодействия для PackingPage.xaml
    /// </summary>
    public partial class PackingPage : Page
    {
        private DatabaseService _databaseService;
        private SerialManager _serialManager;
        private Employee _currentEmployee;
        private Package _currentPackage;
        private ObservableCollection<PackageItem> _packageItems;
        private DispatcherTimer _sessionTimer;
        private DateTime _sessionStartTime;
        private bool _isPackingStarted;

        public PackingPage(DatabaseService databaseService, SerialManager serialManager, Employee employee)
        {
            InitializeComponent();

            _databaseService = databaseService;
            _serialManager = serialManager;
            _currentEmployee = employee;
            _packageItems = new ObservableCollection<PackageItem>();
            PackageContentsDataGrid.ItemsSource = _packageItems;

            // Инициализация таймера сессии
            _sessionTimer = new DispatcherTimer();
            _sessionTimer.Interval = TimeSpan.FromSeconds(1);
            _sessionTimer.Tick += SessionTimer_Tick;
            _sessionStartTime = DateTime.Now;
            _sessionTimer.Start();

            // Отображение имени сотрудника
            EmployeeNameTextBlock.Text = _currentEmployee.FullName;

            // Инициализация типов упаковки
            InitializePackageTypes();

            // Подписка на события RFID считывателя
            _serialManager.DataReceived += SerialManager_DataReceived;

            // Инициализация состояния элементов управления
            UpdateControlState(false);
            
            // Добавление записи в историю операций
            AddToHistory("Страница упаковки открыта");
        }

        private void InitializePackageTypes()
        {
            // Загрузка типов упаковки из базы данных
            var packageTypes = _databaseService.GetPackageTypes();
            PackageTypeComboBox.ItemsSource = packageTypes;
            
            if (packageTypes.Count > 0)
                PackageTypeComboBox.SelectedIndex = 0;
        }

        private void SerialManager_DataReceived(object sender, DataReceivedEventArgs e)
        {
            // Обработка данных от RFID считывателя в потоке UI
            Dispatcher.Invoke(() =>
            {
                try
                {
                    string cardId = e.Data.Trim();
                    
                    // Проверяем, что это карта детали, а не сотрудника
                    if (cardId.StartsWith("P") && _isPackingStarted)
                    {
                        ProcessPartCard(cardId);
                    }
                    else
                    {
                        StatusBarTextBlock.Text = "Неверный формат карты или упаковка не начата";
                    }
                }
                catch (Exception ex)
                {
                    StatusBarTextBlock.Text = $"Ошибка обработки данных: {ex.Message}";
                    AddToHistory($"Ошибка: {ex.Message}");
                }
            });
        }

        private void ProcessPartCard(string cardId)
        {
            try
            {
                // Получение информации о детали по ID карты
                var part = _databaseService.GetPartByCardId(cardId);
                
                // Проверка, что деталь существует и прошла предыдущие этапы
                if (part != null && part.Status == "Готово к упаковке")
                {
                    // Проверка, не добавлена ли деталь уже в текущую упаковку
                    if (_packageItems.Any(p => p.SerialNumber == part.SerialNumber))
                    {
                        StatusBarTextBlock.Text = $"Деталь {part.SerialNumber} уже добавлена в упаковку";
                        AddToHistory($"Повторное сканирование: {part.Name} ({part.SerialNumber})");
                        return;
                    }

                    // Добавление детали в список
                    var packageItem = new PackageItem
                    {
                        Index = _packageItems.Count + 1,
                        PartName = part.Name,
                        SerialNumber = part.SerialNumber,
                        Status = "Добавлено",
                        PartId = part.Id
                    };
                    
                    _packageItems.Add(packageItem);
                    
                    // Обновление информации о последней добавленной детали
                    ProductNameTextBlock.Text = part.Name;
                    SerialNumberTextBlock.Text = part.SerialNumber;
                    StatusTextBlock.Text = "Добавлено в упаковку";
                    
                    StatusBarTextBlock.Text = $"Деталь {part.SerialNumber} добавлена в упаковку";
                    AddToHistory($"Добавлена деталь: {part.Name} ({part.SerialNumber})");
                }
                else if (part != null)
                {
                    StatusBarTextBlock.Text = $"Деталь {part.SerialNumber} имеет недопустимый статус: {part.Status}";
                    AddToHistory($"Отклонено: {part.Name} ({part.SerialNumber}) - {part.Status}");
                }
                else
                {
                    StatusBarTextBlock.Text = "Деталь не найдена в базе данных";
                    AddToHistory($"Отклонено: Неизвестная деталь ({cardId})");
                }
            }
            catch (Exception ex)
            {
                StatusBarTextBlock.Text = $"Ошибка при обработке детали: {ex.Message}";
                AddToHistory($"Ошибка: {ex.Message}");
            }
        }

        private void SessionTimer_Tick(object sender, EventArgs e)
        {
            TimeSpan elapsed = DateTime.Now - _sessionStartTime;
            SessionTimeTextBlock.Text = elapsed.ToString(@"hh\:mm\:ss");
            StatusBarTimeTextBlock.Text = elapsed.ToString(@"hh\:mm\:ss");
        }

        private void AddToHistory(string message)
        {
            string timeStamp = DateTime.Now.ToString("HH:mm:ss");
            OperationsHistoryListBox.Items.Add($"[{timeStamp}] {message}");
            OperationsHistoryListBox.ScrollIntoView(OperationsHistoryListBox.Items[OperationsHistoryListBox.Items.Count - 1]);
        }

        private void UpdateControlState(bool isPackingStarted)
        {
            _isPackingStarted = isPackingStarted;
            
            // Кнопки действий
            StartPackingButton.IsEnabled = !isPackingStarted;
            FinishPackingButton.IsEnabled = isPackingStarted && _packageItems.Count > 0;
            ScanPartButton.IsEnabled = isPackingStarted;
            RemovePartButton.IsEnabled = isPackingStarted && PackageContentsDataGrid.SelectedItem != null;
            ClearListButton.IsEnabled = isPackingStarted && _packageItems.Count > 0;
            PrintLabelButton.IsEnabled = isPackingStarted && _packageItems.Count > 0;
            
            // Поля для ввода
            PackageTypeComboBox.IsEnabled = !isPackingStarted;
            PackageNumberTextBox.IsEnabled = !isPackingStarted;
        }

        private void StartPackingButton_Click(object sender, RoutedEventArgs e)
        {
            if (PackageTypeComboBox.SelectedItem == null)
            {
                MessageBox.Show("Выберите тип упаковки", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (string.IsNullOrWhiteSpace(PackageNumberTextBox.Text))
            {
                MessageBox.Show("Введите номер упаковки", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                // Создание новой упаковки
                _currentPackage = new Package
                {
                    Type = PackageTypeComboBox.SelectedItem.ToString(),
                    Number = PackageNumberTextBox.Text,
                    EmployeeId = _currentEmployee.Id,
                    StartTime = DateTime.Now,
                    Status = "В процессе"
                };

                // Сохранение упаковки в базе данных
                int packageId = _databaseService.CreatePackage(_currentPackage);
                _currentPackage.Id = packageId;

                StatusBarTextBlock.Text = "Упаковка начата";
                AddToHistory($"Упаковка начата: {_currentPackage.Type} #{_currentPackage.Number}");

                // Генерация маркировки упаковки
                string mark = GeneratePackageMark();
                PackageMarkTextBox.Text = mark;

                // Обновление состояния элементов управления
                UpdateControlState(true);
            }
            catch (Exception ex)
            {
                StatusBarTextBlock.Text = $"Ошибка при начале упаковки: {ex.Message}";
                AddToHistory($"Ошибка: {ex.Message}");
            }
        }

        private void FinishPackingButton_Click(object sender, RoutedEventArgs e)
        {
            if (_packageItems.Count == 0)
            {
                MessageBox.Show("Упаковка пуста. Добавьте детали перед завершением", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                // Обновление статуса упаковки
                _currentPackage.EndTime = DateTime.Now;
                _currentPackage.Status = "Завершено";
                _currentPackage.ItemCount = _packageItems.Count;
                
                // Обновление упаковки в базе данных
                _databaseService.UpdatePackage(_currentPackage);

                // Обновление статуса каждой детали
                foreach (var item in _packageItems)
                {
                    _databaseService.UpdatePartStatus(item.PartId, "Упаковано", _currentPackage.Id);
                }

                MessageBox.Show($"Упаковка {_currentPackage.Type} #{_currentPackage.Number} завершена успешно", 
                                "Упаковка завершена", MessageBoxButton.OK, MessageBoxImage.Information);

                StatusBarTextBlock.Text = "Упаковка завершена";
                AddToHistory($"Упаковка завершена: {_packageItems.Count} деталей");

                // Сброс состояния
                _packageItems.Clear();
                ProductNameTextBlock.Text = "-";
                SerialNumberTextBlock.Text = "-";
                StatusTextBlock.Text = "-";
                
                // Подготовка к новой упаковке
                PackageNumberTextBox.Text = "";
                PackageMarkTextBox.Text = "";
                UpdateControlState(false);
            }
            catch (Exception ex)
            {
                StatusBarTextBlock.Text = $"Ошибка при завершении упаковки: {ex.Message}";
                AddToHistory($"Ошибка: {ex.Message}");
            }
        }

        private void ScanPartButton_Click(object sender, RoutedEventArgs e)
        {
            if (!_isPackingStarted)
            {
                MessageBox.Show("Сначала начните процесс упаковки", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            // Открытие диалога для ручного ввода ID детали (для тестирования)
            var dialog = new ScanDialog("Сканирование детали", "Приложите RFID карту детали или введите ID вручную:");
            if (dialog.ShowDialog() == true)
            {
                string cardId = dialog.ResultText;
                ProcessPartCard(cardId);
            }
        }

        private void RemovePartButton_Click(object sender, RoutedEventArgs e)
        {
            var selectedItem = PackageContentsDataGrid.SelectedItem as PackageItem;
            if (selectedItem != null)
            {
                MessageBoxResult result = MessageBox.Show(
                    $"Вы уверены, что хотите удалить деталь {selectedItem.PartName} ({selectedItem.SerialNumber}) из упаковки?", 
                    "Подтверждение удаления", 
                    MessageBoxButton.YesNo, 
                    MessageBoxImage.Question);
                
                if (result == MessageBoxResult.Yes)
                {
                    _packageItems.Remove(selectedItem);
                    
                    // Перенумерация оставшихся элементов
                    for (int i = 0; i < _packageItems.Count; i++)
                    {
                        _packageItems[i].Index = i + 1;
                    }
                    
                    StatusBarTextBlock.Text = $"Деталь {selectedItem.SerialNumber} удалена из упаковки";
                    AddToHistory($"Удалена деталь: {selectedItem.PartName} ({selectedItem.SerialNumber})");
                    
                    // Обновление состояния кнопок
                    UpdateControlState(_isPackingStarted);
                }
            }
        }

        private void ClearListButton_Click(object sender, RoutedEventArgs e)
        {
            if (_packageItems.Count > 0)
            {
                MessageBoxResult result = MessageBox.Show(
                    "Вы уверены, что хотите очистить весь список деталей?", 
                    "Подтверждение очистки", 
                    MessageBoxButton.YesNo, 
                    MessageBoxImage.Question);
                
                if (result == MessageBoxResult.Yes)
                {
                    _packageItems.Clear();
                    
                    StatusBarTextBlock.Text = "Список деталей очищен";
                    AddToHistory("Список деталей очищен");
                    
                    // Обновление состояния кнопок
                    UpdateControlState(_isPackingStarted);
                }
            }
        }

        private void PrintLabelButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(PackageMarkTextBox.Text))
                {
                    MessageBox.Show("Сначала сгенерируйте маркировку упаковки", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                // Отправка данных на печать (можно реализовать интеграцию с реальным принтером)
                string printInfo = $"Тип: {_currentPackage.Type}\n" +
                                   $"Номер: {_currentPackage.Number}\n" +
                                   $"Маркировка: {PackageMarkTextBox.Text}\n" +
                                   $"Количество деталей: {_packageItems.Count}\n" +
                                   $"Дата: {DateTime.Now:dd.MM.yyyy HH:mm}";
                
                // Вывод информации в виде превью (для демонстрации)
                var preview = new PrintPreviewWindow(printInfo);
                preview.ShowDialog();
                
                StatusBarTextBlock.Text = "Этикетка отправлена на печать";
                AddToHistory("Этикетка отправлена на печать");
            }
            catch (Exception ex)
            {
                StatusBarTextBlock.Text = $"Ошибка при печати: {ex.Message}";
                AddToHistory($"Ошибка печати: {ex.Message}");
            }
        }

        private void GenerateMarkButton_Click(object sender, RoutedEventArgs e)
        {
            PackageMarkTextBox.Text = GeneratePackageMark();
            StatusBarTextBlock.Text = "Маркировка сгенерирована";
            AddToHistory("Маркировка упаковки сгенерирована");
        }

        private string GeneratePackageMark()
        {
            // Генерация уникальной маркировки на основе типа упаковки, номера и даты
            string packageType = PackageTypeComboBox.SelectedItem?.ToString() ?? "BOX";
            string packageNumber = PackageNumberTextBox.Text;
            string dateCode = DateTime.Now.ToString("yyMMdd");
            
            // Сокращение типа упаковки до 3 символов
            string typeCode = packageType.Length > 3 ? packageType.Substring(0, 3).ToUpper() : packageType.ToUpper();
            
            return $"{typeCode}-{packageNumber}-{dateCode}";
        }

        private void PackageTypeComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // При изменении типа упаковки можно обновить маркировку
            if (_isPackingStarted && PackageTypeComboBox.SelectedItem != null)
            {
                PackageMarkTextBox.Text = GeneratePackageMark();
            }
        }
    }

    /// <summary>
    /// Класс, представляющий элемент в упаковке
    /// </summary>
    public class PackageItem
    {
        public int Index { get; set; }
        public string PartName { get; set; }
        public string SerialNumber { get; set; }
        public string Status { get; set; }
        public int PartId { get; set; }
    }
} 