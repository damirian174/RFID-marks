using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using RFID_marks.Models;

namespace RFID_marks.Services
{
    /// <summary>
    /// Сервис для работы с деталями, аналог detail_work.py
    /// </summary>
    public class DetailService
    {
        private static readonly Logger _logger = new Logger();
        private static readonly DatabaseService _databaseService = new DatabaseService();

        // Ссылки на пользовательские интерфейсы
        private static object _markUI;
        private static object _workUI;
        private static object _packingUI;
        private static object _testsUI;

        /// <summary>
        /// Установить ссылки на интерфейсы
        /// </summary>
        public static void SetUIReferences(object markUI, object workUI, object packingUI, object testsUI)
        {
            _markUI = markUI;
            _workUI = workUI;
            _packingUI = packingUI;
            _testsUI = testsUI;
            
            _logger.LogEvent("Установлены ссылки на пользовательские интерфейсы");
        }

        /// <summary>
        /// Получить информацию о детали по штрихкоду
        /// </summary>
        public static async Task<bool> GetDetailAsync(string barcode)
        {
            try
            {
                _logger.LogEvent($"Запрос информации о детали по штрихкоду: {barcode}");
                
                JObject data = new JObject
                {
                    ["type"] = "Detail",
                    ["id"] = barcode
                };
                
                JObject response = await Task.Run(() => _databaseService.ExecuteRequest(data));
                
                _logger.LogEvent($"Ответ сервера: {response}");
                
                if (response != null && response["status"]?.ToString() == "ok")
                {
                    JObject detailData = response["data"] as JObject;
                    
                    if (detailData != null)
                    {
                        string detailName = detailData["name"]?.ToString();
                        string serialNumber = detailData["serial"]?.ToString();
                        
                        if (!string.IsNullOrEmpty(detailName) && !string.IsNullOrEmpty(serialNumber))
                        {
                            _logger.LogEvent($"Получены данные о детали: {detailName}, серийный номер: {serialNumber}");
                            
                            // Обновляем информацию о детали в конфигурации
                            Config.DetailName = detailName;
                            Config.DetailSerial = serialNumber;
                            
                            // Обновляем все интерфейсы
                            Update(detailName, serialNumber);
                            
                            return true;
                        }
                        else
                        {
                            _logger.LogError("Отсутствуют обязательные поля в данных о детали");
                            return false;
                        }
                    }
                    else
                    {
                        _logger.LogError("Данные о детали не получены или имеют неверный формат");
                        return false;
                    }
                }
                else
                {
                    _logger.LogError($"Ошибка получения данных о детали: {response?["message"]?.ToString() ?? "Неизвестная ошибка"}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Исключение при получении данных о детали: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Синхронная версия получения информации о детали
        /// </summary>
        public static bool GetDetail(string barcode)
        {
            return GetDetailAsync(barcode).GetAwaiter().GetResult();
        }

        /// <summary>
        /// Обновить информацию о детали на всех интерфейсах
        /// </summary>
        public static void Update(string name, string serial)
        {
            try
            {
                _logger.LogEvent($"Обновление информации о детали на всех интерфейсах: {name}, {serial}");
                
                // Метод будет вызывать соответствующие методы обновления в UI
                // Реализация будет добавлена после создания всех интерфейсов
                
                // Если интерфейсы поддерживают обновление детали, вызываем соответствующие методы
                if (_workUI != null && _workUI is dynamic workUI)
                {
                    try { workUI.UpdateDetail(name, serial); } catch { }
                }
                
                if (_markUI != null && _markUI is dynamic markUI)
                {
                    try { markUI.UpdateDetail(name, serial); } catch { }
                }
                
                if (_packingUI != null && _packingUI is dynamic packingUI)
                {
                    try { packingUI.UpdateDetail(name, serial); } catch { }
                }
                
                if (_testsUI != null && _testsUI is dynamic testsUI)
                {
                    try { testsUI.UpdateDetail(name, serial); } catch { }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Ошибка при обновлении информации о детали на интерфейсах: {ex.Message}");
            }
        }

        /// <summary>
        /// Начать работу с деталью
        /// </summary>
        public static async Task<bool> StartWorkAsync(string workDescription)
        {
            try
            {
                if (string.IsNullOrEmpty(Config.Name) || !Config.Auth)
                {
                    _logger.LogError("Невозможно начать работу: пользователь не авторизован");
                    return false;
                }
                
                if (string.IsNullOrEmpty(Config.DetailName) || string.IsNullOrEmpty(Config.DetailSerial))
                {
                    _logger.LogError("Невозможно начать работу: не выбрана деталь");
                    return false;
                }
                
                _logger.LogEvent($"Начало работы с деталью: {Config.DetailName}, {Config.DetailSerial}");
                
                // Разбиваем полное имя на части
                string[] nameParts = Config.Name.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                string lastName = nameParts.Length > 0 ? nameParts[0] : "";
                string firstName = nameParts.Length > 1 ? nameParts[1] : "";
                
                JObject data = new JObject
                {
                    ["type"] = "startWork",
                    ["name"] = firstName,
                    ["surname"] = lastName,
                    ["detail_name"] = Config.DetailName,
                    ["detail_id"] = Config.DetailSerial,
                    ["work_description"] = workDescription
                };
                
                _logger.LogEvent($"Запрос на начало работы: {data}");
                
                JObject response = await Task.Run(() => _databaseService.ExecuteRequest(data));
                
                _logger.LogEvent($"Ответ сервера: {response}");
                
                if (response != null && response["status"]?.ToString() == "ok")
                {
                    _logger.LogEvent("Работа успешно начата");
                    return true;
                }
                else
                {
                    _logger.LogError($"Ошибка при начале работы: {response?["message"]?.ToString() ?? "Неизвестная ошибка"}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Исключение при начале работы: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Синхронная версия начала работы
        /// </summary>
        public static bool StartWork(string workDescription)
        {
            return StartWorkAsync(workDescription).GetAwaiter().GetResult();
        }

        /// <summary>
        /// Завершить работу с деталью
        /// </summary>
        public static async Task<bool> EndWorkAsync()
        {
            try
            {
                if (string.IsNullOrEmpty(Config.Name) || !Config.Auth)
                {
                    _logger.LogError("Невозможно завершить работу: пользователь не авторизован");
                    return false;
                }
                
                _logger.LogEvent("Завершение работы с деталью");
                
                // Разбиваем полное имя на части
                string[] nameParts = Config.Name.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                string lastName = nameParts.Length > 0 ? nameParts[0] : "";
                string firstName = nameParts.Length > 1 ? nameParts[1] : "";
                
                JObject data = new JObject
                {
                    ["type"] = "endWork",
                    ["name"] = firstName,
                    ["surname"] = lastName
                };
                
                _logger.LogEvent($"Запрос на завершение работы: {data}");
                
                JObject response = await Task.Run(() => _databaseService.ExecuteRequest(data));
                
                _logger.LogEvent($"Ответ сервера: {response}");
                
                if (response != null && response["status"]?.ToString() == "ok")
                {
                    _logger.LogEvent("Работа успешно завершена");
                    return true;
                }
                else
                {
                    _logger.LogError($"Ошибка при завершении работы: {response?["message"]?.ToString() ?? "Неизвестная ошибка"}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Исключение при завершении работы: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Синхронная версия завершения работы
        /// </summary>
        public static bool EndWork()
        {
            return EndWorkAsync().GetAwaiter().GetResult();
        }

        /// <summary>
        /// Приостановить работу с деталью
        /// </summary>
        public static async Task<bool> PauseWorkAsync()
        {
            try
            {
                if (string.IsNullOrEmpty(Config.Name) || !Config.Auth)
                {
                    _logger.LogError("Невозможно приостановить работу: пользователь не авторизован");
                    return false;
                }
                
                _logger.LogEvent("Приостановление работы с деталью");
                
                // Разбиваем полное имя на части
                string[] nameParts = Config.Name.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                string lastName = nameParts.Length > 0 ? nameParts[0] : "";
                string firstName = nameParts.Length > 1 ? nameParts[1] : "";
                
                JObject data = new JObject
                {
                    ["type"] = "pauseWork",
                    ["name"] = firstName,
                    ["surname"] = lastName
                };
                
                _logger.LogEvent($"Запрос на приостановление работы: {data}");
                
                JObject response = await Task.Run(() => _databaseService.ExecuteRequest(data));
                
                _logger.LogEvent($"Ответ сервера: {response}");
                
                if (response != null && response["status"]?.ToString() == "ok")
                {
                    _logger.LogEvent("Работа успешно приостановлена");
                    return true;
                }
                else
                {
                    _logger.LogError($"Ошибка при приостановлении работы: {response?["message"]?.ToString() ?? "Неизвестная ошибка"}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Исключение при приостановлении работы: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Синхронная версия приостановления работы
        /// </summary>
        public static bool PauseWork()
        {
            return PauseWorkAsync().GetAwaiter().GetResult();
        }

        /// <summary>
        /// Продолжить работу с деталью
        /// </summary>
        public static async Task<bool> ContinueWorkAsync()
        {
            try
            {
                if (string.IsNullOrEmpty(Config.Name) || !Config.Auth)
                {
                    _logger.LogError("Невозможно продолжить работу: пользователь не авторизован");
                    return false;
                }
                
                _logger.LogEvent("Продолжение работы с деталью");
                
                // Разбиваем полное имя на части
                string[] nameParts = Config.Name.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                string lastName = nameParts.Length > 0 ? nameParts[0] : "";
                string firstName = nameParts.Length > 1 ? nameParts[1] : "";
                
                JObject data = new JObject
                {
                    ["type"] = "continueWork",
                    ["name"] = firstName,
                    ["surname"] = lastName
                };
                
                _logger.LogEvent($"Запрос на продолжение работы: {data}");
                
                JObject response = await Task.Run(() => _databaseService.ExecuteRequest(data));
                
                _logger.LogEvent($"Ответ сервера: {response}");
                
                if (response != null && response["status"]?.ToString() == "ok")
                {
                    _logger.LogEvent("Работа успешно продолжена");
                    return true;
                }
                else
                {
                    _logger.LogError($"Ошибка при продолжении работы: {response?["message"]?.ToString() ?? "Неизвестная ошибка"}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError($"Исключение при продолжении работы: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Синхронная версия продолжения работы
        /// </summary>
        public static bool ContinueWork()
        {
            return ContinueWorkAsync().GetAwaiter().GetResult();
        }

        /// <summary>
        /// Сбросить сессию работы
        /// </summary>
        public static void ResetSession()
        {
            _logger.LogEvent("Сброс сессии работы");
            
            // Сбрасываем все данные о детали
            Config.DetailName = null;
            Config.DetailSerial = null;
            
            // Обновляем интерфейсы
            Update("", "");
        }
    }
} 