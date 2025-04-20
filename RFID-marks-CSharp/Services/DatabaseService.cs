using System;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;
using RFID_marks.Models;

namespace RFID_marks.Services
{
    /// <summary>
    /// Сервис для взаимодействия с базой данных через TCP/IP
    /// </summary>
    public class DatabaseService
    {
        private readonly string _serverAddress;
        private readonly int _serverPort;
        private readonly int _timeoutMs = 5000; // 5 секунд таймаут
        
        /// <summary>
        /// Конструктор сервиса базы данных
        /// </summary>
        /// <param name="serverAddress">Адрес сервера</param>
        /// <param name="serverPort">Порт сервера</param>
        public DatabaseService(string serverAddress, int serverPort)
        {
            _serverAddress = serverAddress;
            _serverPort = serverPort;
        }
        
        /// <summary>
        /// Конструктор с параметрами по умолчанию из конфигурации
        /// </summary>
        public DatabaseService()
        {
            _serverAddress = Config.ServerAddress;
            _serverPort = Config.ServerPort;
        }
        
        /// <summary>
        /// Проверяет доступность сервера, отправляя тестовый запрос
        /// </summary>
        /// <returns>True если сервер доступен, иначе False</returns>
        public async Task<bool> TestConnection()
        {
            try
            {
                // Создаем тестовый запрос
                var testData = new { type = "test" };
                
                // Отправляем запрос и ожидаем любой ответ
                var response = await SendRequest(testData);
                
                Logger.LogEvent("Сервер доступен");
                return response != null;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при подключении к серверу: {ex.Message}", ex);
                return false;
            }
        }
        
        /// <summary>
        /// Отправляет запрос к базе данных
        /// </summary>
        /// <typeparam name="T">Тип возвращаемого объекта</typeparam>
        /// <param name="requestData">Данные запроса</param>
        /// <returns>Объект ответа или null при ошибке</returns>
        public async Task<T> SendRequestAsync<T>(object requestData) where T : class
        {
            try
            {
                var jsonResponse = await SendRequest(requestData);
                if (string.IsNullOrEmpty(jsonResponse))
                    return null;
                
                // Десериализуем JSON в объект указанного типа
                return JsonSerializer.Deserialize<T>(jsonResponse);
            }
            catch (JsonException ex)
            {
                Logger.LogError($"Ошибка десериализации JSON: {ex.Message}", ex);
                return null;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке запроса: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Отправляет запрос и получает ответ в виде динамического объекта
        /// </summary>
        /// <param name="requestData">Данные запроса</param>
        /// <returns>Динамический объект ответа или null при ошибке</returns>
        public async Task<dynamic> SendRequestAsync(object requestData)
        {
            try
            {
                var jsonResponse = await SendRequest(requestData);
                if (string.IsNullOrEmpty(jsonResponse))
                    return null;
                
                // Десериализуем JSON в dynamic
                return JsonSerializer.Deserialize<dynamic>(jsonResponse);
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке запроса: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Базовый метод для отправки запроса и получения ответа в виде строки JSON
        /// </summary>
        /// <param name="requestData">Данные запроса</param>
        /// <returns>Строка JSON с ответом или null при ошибке</returns>
        private async Task<string> SendRequest(object requestData)
        {
            // Если в запросе нет ID, добавляем его из конфигурации
            var requestDict = requestData as System.Collections.Generic.Dictionary<string, object>;
            if (requestDict != null && !requestDict.ContainsKey("id") && Config.Id != 0)
            {
                requestDict["id"] = Config.Id;
            }
            
            Logger.LogDatabaseRequest(requestData);
            
            TcpClient client = null;
            try
            {
                // Создаем соединение с сервером
                client = new TcpClient();
                var connectTask = client.ConnectAsync(_serverAddress, _serverPort);
                
                // Ограничиваем время ожидания соединения
                if (await Task.WhenAny(connectTask, Task.Delay(_timeoutMs)) != connectTask)
                {
                    throw new TimeoutException($"Превышено время ожидания соединения с сервером {_serverAddress}:{_serverPort}");
                }
                
                // Сериализуем объект в JSON
                string jsonRequest = JsonSerializer.Serialize(requestData);
                byte[] requestBytes = Encoding.UTF8.GetBytes(jsonRequest);
                
                // Отправляем данные
                using NetworkStream stream = client.GetStream();
                await stream.WriteAsync(requestBytes, 0, requestBytes.Length);
                
                // Получаем ответ
                byte[] buffer = new byte[4096];
                StringBuilder responseBuilder = new StringBuilder();
                int bytesRead;
                
                // Устанавливаем таймаут для чтения
                var readTask = Task.Run(async () =>
                {
                    do
                    {
                        bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                        if (bytesRead > 0)
                        {
                            responseBuilder.Append(Encoding.UTF8.GetString(buffer, 0, bytesRead));
                        }
                    } while (bytesRead > 0 && stream.DataAvailable);
                });
                
                // Проверяем таймаут чтения
                if (await Task.WhenAny(readTask, Task.Delay(_timeoutMs)) != readTask)
                {
                    throw new TimeoutException($"Превышено время ожидания ответа от сервера {_serverAddress}:{_serverPort}");
                }
                
                string response = responseBuilder.ToString();
                Logger.LogDatabaseResponse(response);
                
                return response;
            }
            catch (SocketException ex)
            {
                Logger.LogError($"Ошибка сокета при подключении к серверу: {ex.Message}", ex);
                return null;
            }
            catch (TimeoutException ex)
            {
                Logger.LogError($"Превышено время ожидания: {ex.Message}", ex);
                return null;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Непредвиденная ошибка: {ex.Message}", ex);
                return null;
            }
            finally
            {
                // Закрываем соединение
                client?.Close();
            }
        }
        
        #region Специализированные методы для работы с БД
        
        /// <summary>
        /// Получить пользователя по UID карты
        /// </summary>
        /// <param name="uid">UID карты пользователя</param>
        /// <returns>Объект пользователя или null при ошибке</returns>
        public async Task<User> GetUserByCardAsync(string uid)
        {
            var requestData = new 
            { 
                type = "user", 
                uid = uid 
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения пользователя по карте: {response?.message}");
                return null;
            }
            
            // Извлекаем данные пользователя из ответа
            dynamic userData = response.data ?? response;
            
            try
            {
                return new User
                {
                    Id = Convert.ToInt32(userData.id),
                    FirstName = userData.name?.ToString(),
                    LastName = userData.surname?.ToString(),
                    CardUID = uid,
                    HasActiveSession = userData.has_active_session == true
                };
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных пользователя: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Получить информацию о детали по штрих-коду или ID
        /// </summary>
        /// <param name="detailId">ID или штрих-код детали</param>
        /// <returns>Объект детали или null при ошибке</returns>
        public async Task<Detail> GetDetailAsync(string detailId)
        {
            var requestData = new 
            { 
                type = "details", 
                detail_id = detailId 
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения информации о детали: {response?.message}");
                return null;
            }
            
            // Извлекаем данные детали из ответа
            dynamic detailData = response.data ?? response;
            
            try
            {
                return new Detail
                {
                    Id = detailData.id?.ToString(),
                    Name = detailData.name?.ToString(),
                    SerialNumber = detailData.serial_number?.ToString(),
                    Status = detailData.stage?.ToString(),
                    Description = detailData.description?.ToString()
                };
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных детали: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Начать сессию работы пользователя
        /// </summary>
        /// <param name="firstName">Имя пользователя</param>
        /// <param name="lastName">Фамилия пользователя</param>
        /// <param name="workDescription">Описание работы</param>
        /// <returns>True, если сессия успешно начата</returns>
        public async Task<bool> StartSessionAsync(string firstName, string lastName, string workDescription = "Без детали")
        {
            var requestData = new 
            { 
                type = "startSession", 
                name = firstName, 
                surname = lastName,
                work_description = workDescription
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось начать сессию: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Сессия успешно начата: {lastName} {firstName}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось начать сессию: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Завершить сессию работы пользователя
        /// </summary>
        /// <param name="firstName">Имя пользователя</param>
        /// <param name="lastName">Фамилия пользователя</param>
        /// <returns>True, если сессия успешно завершена</returns>
        public async Task<bool> EndSessionAsync(string firstName, string lastName)
        {
            var requestData = new 
            { 
                type = "endSession", 
                name = firstName, 
                surname = lastName
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось завершить сессию: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Сессия успешно завершена: {lastName} {firstName}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось завершить сессию: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Начать работу с деталью
        /// </summary>
        /// <param name="userId">ID пользователя</param>
        /// <param name="detailId">ID детали</param>
        /// <returns>True, если работа успешно начата</returns>
        public async Task<bool> StartWorkAsync(int userId, string detailId)
        {
            var requestData = new 
            { 
                type = "startWork", 
                user_id = userId, 
                detail_id = detailId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            return response?.status?.ToString() == "ok";
        }
        
        /// <summary>
        /// Завершить работу с деталью
        /// </summary>
        /// <param name="userId">ID пользователя</param>
        /// <param name="detailId">ID детали</param>
        /// <returns>True, если работа успешно завершена</returns>
        public async Task<bool> EndWorkAsync(int userId, string detailId)
        {
            var requestData = new 
            { 
                type = "endWork", 
                user_id = userId, 
                detail_id = detailId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            return response?.status?.ToString() == "ok";
        }
        
        /// <summary>
        /// Приостановить работу с деталью
        /// </summary>
        /// <param name="userId">ID пользователя</param>
        /// <param name="detailId">ID детали</param>
        /// <returns>True, если работа успешно приостановлена</returns>
        public async Task<bool> PauseWorkAsync(int userId, string detailId)
        {
            var requestData = new 
            { 
                type = "pauseWork", 
                user_id = userId, 
                detail_id = detailId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            return response?.status?.ToString() == "ok";
        }
        
        /// <summary>
        /// Продолжить работу с деталью
        /// </summary>
        /// <param name="userId">ID пользователя</param>
        /// <param name="detailId">ID детали</param>
        /// <returns>True, если работа успешно продолжена</returns>
        public async Task<bool> ContinueWorkAsync(int userId, string detailId)
        {
            var requestData = new 
            { 
                type = "continueWork", 
                user_id = userId, 
                detail_id = detailId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            return response?.status?.ToString() == "ok";
        }
        
        #endregion
        
        #region Методы для работы с сотрудниками
        
        /// <summary>
        /// Получить список всех сотрудников
        /// </summary>
        /// <returns>Список сотрудников или null при ошибке</returns>
        public async Task<List<User>> GetAllEmployeesAsync()
        {
            var requestData = new
            {
                type = "getAllEmployees"
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения списка сотрудников: {response?.message}");
                return null;
            }
            
            try
            {
                List<User> employees = new List<User>();
                
                // Проверяем, где находятся данные в ответе
                var employeesData = response.data != null ? response.data : response;
                
                foreach (var item in employeesData.EnumerateArray())
                {
                    employees.Add(new User
                    {
                        Id = Convert.ToInt32(item.GetProperty("id").GetInt32()),
                        FirstName = item.GetProperty("name").GetString(),
                        LastName = item.GetProperty("surname").GetString(),
                        CardUID = item.TryGetProperty("card_uid", out var cardUid) ? cardUid.GetString() : null,
                        HasActiveSession = item.TryGetProperty("has_active_session", out var hasSession) && hasSession.GetBoolean()
                    });
                }
                
                return employees;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных сотрудников: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Получить информацию о сотруднике по ID
        /// </summary>
        /// <param name="employeeId">ID сотрудника</param>
        /// <returns>Объект сотрудника или null при ошибке</returns>
        public async Task<User> GetEmployeeByIdAsync(int employeeId)
        {
            var requestData = new
            {
                type = "getEmployee",
                employee_id = employeeId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения информации о сотруднике: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем данные сотрудника из ответа
                dynamic userData = response.data ?? response;
                
                return new User
                {
                    Id = Convert.ToInt32(userData.id),
                    FirstName = userData.name?.ToString(),
                    LastName = userData.surname?.ToString(),
                    CardUID = userData.card_uid?.ToString(),
                    HasActiveSession = userData.has_active_session == true
                };
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных сотрудника: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Добавить нового сотрудника
        /// </summary>
        /// <param name="employee">Объект сотрудника для добавления</param>
        /// <returns>ID нового сотрудника или null при ошибке</returns>
        public async Task<int?> AddEmployeeAsync(User employee)
        {
            var requestData = new
            {
                type = "addEmployee",
                name = employee.FirstName,
                surname = employee.LastName,
                card_uid = employee.CardUID
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка добавления сотрудника: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем ID нового сотрудника
                return Convert.ToInt32(response.employee_id ?? response.data?.employee_id);
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке ответа на добавление сотрудника: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Обновить информацию о сотруднике
        /// </summary>
        /// <param name="employee">Объект сотрудника с обновленными данными</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        public async Task<bool> UpdateEmployeeAsync(User employee)
        {
            var requestData = new
            {
                type = "updateEmployee",
                employee_id = employee.Id,
                name = employee.FirstName,
                surname = employee.LastName,
                card_uid = employee.CardUID
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось обновить данные сотрудника: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Данные сотрудника успешно обновлены: ID={employee.Id}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось обновить данные сотрудника: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Удалить сотрудника
        /// </summary>
        /// <param name="employeeId">ID сотрудника для удаления</param>
        /// <returns>True, если удаление выполнено успешно</returns>
        public async Task<bool> DeleteEmployeeAsync(int employeeId)
        {
            var requestData = new
            {
                type = "deleteEmployee",
                employee_id = employeeId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось удалить сотрудника: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Сотрудник успешно удален: ID={employeeId}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось удалить сотрудника: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Получить активные сессии сотрудников
        /// </summary>
        /// <returns>Список активных сессий или null при ошибке</returns>
        public async Task<List<Session>> GetActiveSessionsAsync()
        {
            var requestData = new
            {
                type = "getActiveSessions"
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения активных сессий: {response?.message}");
                return null;
            }
            
            try
            {
                List<Session> sessions = new List<Session>();
                
                // Проверяем, где находятся данные в ответе
                var sessionsData = response.data != null ? response.data : response;
                
                foreach (var item in sessionsData.EnumerateArray())
                {
                    int employeeId = item.GetProperty("employee_id").GetInt32();
                    string firstName = item.GetProperty("name").GetString();
                    string lastName = item.GetProperty("surname").GetString();
                    
                    var session = new Session
                    {
                        Id = item.GetProperty("session_id").GetInt32(),
                        EmployeeId = employeeId,
                        StartTime = DateTime.Parse(item.GetProperty("start_time").GetString()),
                        Employee = new User
                        {
                            Id = employeeId,
                            FirstName = firstName,
                            LastName = lastName
                        }
                    };
                    
                    if (item.TryGetProperty("work_description", out var workDesc))
                    {
                        session.Description = workDesc.GetString();
                    }
                    
                    sessions.Add(session);
                }
                
                return sessions;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных активных сессий: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Принудительно завершить сессию сотрудника
        /// </summary>
        /// <param name="sessionId">ID сессии</param>
        /// <returns>True, если сессия успешно завершена</returns>
        public async Task<bool> ForceEndSessionAsync(int sessionId)
        {
            var requestData = new
            {
                type = "forceEndSession",
                session_id = sessionId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось принудительно завершить сессию: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Сессия успешно завершена принудительно: ID={sessionId}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось принудительно завершить сессию: {response.message}");
                return false;
            }
        }
        
        #endregion
        
        #region Дополнительные методы для работы с пользователями и деталями
        
        /// <summary>
        /// Добавить нового пользователя с указанием профессии
        /// </summary>
        /// <param name="firstName">Имя пользователя</param>
        /// <param name="lastName">Фамилия пользователя</param>
        /// <param name="profession">Профессия пользователя</param>
        /// <returns>ID нового пользователя или null при ошибке</returns>
        public async Task<int?> AddUserAsync(string firstName, string lastName, string profession)
        {
            var requestData = new
            {
                type = "addUser",
                name = firstName,
                surname = lastName,
                prof = profession
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка добавления пользователя: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем ID нового пользователя
                return Convert.ToInt32(response.user_id ?? response.data?.user_id);
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке ответа на добавление пользователя: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Получить список всех операций для детали
        /// </summary>
        /// <param name="detailId">ID детали</param>
        /// <returns>Список операций или null при ошибке</returns>
        public async Task<List<Operation>> GetDetailOperationsAsync(string detailId)
        {
            var requestData = new
            {
                type = "getDetailOperations",
                detail_id = detailId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения операций для детали: {response?.message}");
                return null;
            }
            
            try
            {
                List<Operation> operations = new List<Operation>();
                
                // Проверяем, где находятся данные в ответе
                var operationsData = response.data != null ? response.data : response;
                
                foreach (var item in operationsData.EnumerateArray())
                {
                    operations.Add(new Operation
                    {
                        Id = item.GetProperty("id").GetInt32(),
                        DetailId = detailId,
                        Type = item.GetProperty("type").GetString(),
                        Status = item.GetProperty("status").GetString(),
                        StartTime = item.TryGetProperty("start_time", out var startTime) ? 
                            DateTime.Parse(startTime.GetString()) : DateTime.MinValue,
                        EndTime = item.TryGetProperty("end_time", out var endTime) ? 
                            DateTime.Parse(endTime.GetString()) : DateTime.MinValue,
                        EmployeeId = item.TryGetProperty("employee_id", out var employeeId) ? 
                            employeeId.GetInt32() : 0,
                        Description = item.TryGetProperty("description", out var description) ? 
                            description.GetString() : null
                    });
                }
                
                return operations;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных операций: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Получить список всех деталей
        /// </summary>
        /// <returns>Список деталей или null при ошибке</returns>
        public async Task<List<Detail>> GetAllDetailsAsync()
        {
            var requestData = new
            {
                type = "getAllDetails"
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения списка деталей: {response?.message}");
                return null;
            }
            
            try
            {
                List<Detail> details = new List<Detail>();
                
                // Проверяем, где находятся данные в ответе
                var detailsData = response.data != null ? response.data : response;
                
                foreach (var item in detailsData.EnumerateArray())
                {
                    details.Add(new Detail
                    {
                        Id = item.GetProperty("id").ToString(),
                        Name = item.GetProperty("name").GetString(),
                        SerialNumber = item.TryGetProperty("serial_number", out var serialNumber) ? 
                            serialNumber.GetString() : null,
                        Status = item.TryGetProperty("stage", out var stage) ? 
                            stage.GetString() : null,
                        Description = item.TryGetProperty("description", out var description) ? 
                            description.GetString() : null
                    });
                }
                
                return details;
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных деталей: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Добавить новую деталь
        /// </summary>
        /// <param name="detail">Объект детали для добавления</param>
        /// <returns>ID новой детали или null при ошибке</returns>
        public async Task<string> AddDetailAsync(Detail detail)
        {
            var requestData = new
            {
                type = "addDetail",
                name = detail.Name,
                serial_number = detail.SerialNumber,
                description = detail.Description
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка добавления детали: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем ID новой детали
                return (response.detail_id ?? response.data?.detail_id)?.ToString();
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке ответа на добавление детали: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Обновить информацию о детали
        /// </summary>
        /// <param name="detail">Объект детали с обновленными данными</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        public async Task<bool> UpdateDetailAsync(Detail detail)
        {
            var requestData = new
            {
                type = "updateDetail",
                detail_id = detail.Id,
                name = detail.Name,
                serial_number = detail.SerialNumber,
                stage = detail.Status,
                description = detail.Description
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось обновить данные детали: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Данные детали успешно обновлены: ID={detail.Id}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось обновить данные детали: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Добавить операцию для детали
        /// </summary>
        /// <param name="detailId">ID детали</param>
        /// <param name="operationType">Тип операции</param>
        /// <param name="description">Описание операции</param>
        /// <returns>ID новой операции или null при ошибке</returns>
        public async Task<int?> AddOperationAsync(string detailId, string operationType, string description)
        {
            var requestData = new
            {
                type = "addOperation",
                detail_id = detailId,
                operation_type = operationType,
                description = description
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка добавления операции: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем ID новой операции
                return Convert.ToInt32(response.operation_id ?? response.data?.operation_id);
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке ответа на добавление операции: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Получить статистику работы пользователя
        /// </summary>
        /// <param name="userId">ID пользователя</param>
        /// <param name="startDate">Дата начала периода</param>
        /// <param name="endDate">Дата окончания периода</param>
        /// <returns>Объект статистики или null при ошибке</returns>
        public async Task<dynamic> GetUserStatisticsAsync(int userId, DateTime startDate, DateTime endDate)
        {
            var requestData = new
            {
                type = "getUserStatistics",
                user_id = userId,
                start_date = startDate.ToString("yyyy-MM-dd"),
                end_date = endDate.ToString("yyyy-MM-dd")
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения статистики пользователя: {response?.message}");
                return null;
            }
            
            return response.data ?? response;
        }
        
        /// <summary>
        /// Получить статистику по деталям
        /// </summary>
        /// <param name="startDate">Дата начала периода</param>
        /// <param name="endDate">Дата окончания периода</param>
        /// <returns>Объект статистики или null при ошибке</returns>
        public async Task<dynamic> GetDetailsStatisticsAsync(DateTime startDate, DateTime endDate)
        {
            var requestData = new
            {
                type = "getDetailsStatistics",
                start_date = startDate.ToString("yyyy-MM-dd"),
                end_date = endDate.ToString("yyyy-MM-dd")
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения статистики по деталям: {response?.message}");
                return null;
            }
            
            return response.data ?? response;
        }
        
        /// <summary>
        /// Отметить деталь как дефектную
        /// </summary>
        /// <param name="detailId">ID детали</param>
        /// <param name="defectDescription">Описание дефекта</param>
        /// <param name="userId">ID пользователя, обнаружившего дефект</param>
        /// <returns>True, если операция выполнена успешно</returns>
        public async Task<bool> MarkDetailAsDefectiveAsync(string detailId, string defectDescription, int userId)
        {
            var requestData = new
            {
                type = "markAsDefective",
                detail_id = detailId,
                defect_description = defectDescription,
                user_id = userId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось отметить деталь как дефектную: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Деталь успешно отмечена как дефектная: ID={detailId}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось отметить деталь как дефектную: {response.message}");
                return false;
            }
        }
        
        #endregion
        
        #region Методы для работы с RFID-метками
        
        /// <summary>
        /// Записать данные в RFID-метку
        /// </summary>
        /// <param name="data">Данные для записи</param>
        /// <returns>True, если запись выполнена успешно</returns>
        public async Task<bool> WriteRfidTagAsync(string data)
        {
            var requestData = new
            {
                type = "writeRfid",
                data = data
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось записать данные в RFID-метку: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"Данные успешно записаны в RFID-метку: {data}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось записать данные в RFID-метку: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Прочитать данные с RFID-метки
        /// </summary>
        /// <returns>Прочитанные данные или null при ошибке</returns>
        public async Task<string> ReadRfidTagAsync()
        {
            var requestData = new
            {
                type = "readRfid"
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка чтения RFID-метки: {response?.message}");
                return null;
            }
            
            try
            {
                return response.data?.ToString() ?? response.rfid_data?.ToString();
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных RFID-метки: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Ассоциировать RFID-метку с деталью
        /// </summary>
        /// <param name="rfidUid">UID RFID-метки</param>
        /// <param name="detailId">ID детали</param>
        /// <returns>True, если ассоциация выполнена успешно</returns>
        public async Task<bool> AssociateRfidWithDetailAsync(string rfidUid, string detailId)
        {
            var requestData = new
            {
                type = "associateRfid",
                rfid_uid = rfidUid,
                detail_id = detailId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось ассоциировать RFID-метку с деталью: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"RFID-метка успешно ассоциирована с деталью: UID={rfidUid}, DetailID={detailId}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось ассоциировать RFID-метку с деталью: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Ассоциировать RFID-метку с сотрудником
        /// </summary>
        /// <param name="rfidUid">UID RFID-метки</param>
        /// <param name="employeeId">ID сотрудника</param>
        /// <returns>True, если ассоциация выполнена успешно</returns>
        public async Task<bool> AssociateRfidWithEmployeeAsync(string rfidUid, int employeeId)
        {
            var requestData = new
            {
                type = "associateRfidEmployee",
                rfid_uid = rfidUid,
                employee_id = employeeId
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null)
            {
                Logger.LogError("Не удалось ассоциировать RFID-метку с сотрудником: нет ответа от сервера");
                return false;
            }
            
            bool success = response.status?.ToString() == "ok";
            if (success)
            {
                Logger.LogEvent($"RFID-метка успешно ассоциирована с сотрудником: UID={rfidUid}, EmployeeID={employeeId}");
                return true;
            }
            else
            {
                Logger.LogError($"Не удалось ассоциировать RFID-метку с сотрудником: {response.message}");
                return false;
            }
        }
        
        /// <summary>
        /// Получить информацию о детали по RFID-метке
        /// </summary>
        /// <param name="rfidUid">UID RFID-метки</param>
        /// <returns>Объект детали или null при ошибке</returns>
        public async Task<Detail> GetDetailByRfidAsync(string rfidUid)
        {
            var requestData = new
            {
                type = "getDetailByRfid",
                rfid_uid = rfidUid
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения информации о детали по RFID: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем данные детали из ответа
                dynamic detailData = response.data ?? response;
                
                return new Detail
                {
                    Id = detailData.id?.ToString(),
                    Name = detailData.name?.ToString(),
                    SerialNumber = detailData.serial_number?.ToString(),
                    Status = detailData.stage?.ToString(),
                    Description = detailData.description?.ToString()
                };
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных детали по RFID: {ex.Message}", ex);
                return null;
            }
        }
        
        /// <summary>
        /// Получить информацию о сотруднике по RFID-метке
        /// </summary>
        /// <param name="rfidUid">UID RFID-метки</param>
        /// <returns>Объект сотрудника или null при ошибке</returns>
        public async Task<User> GetEmployeeByRfidAsync(string rfidUid)
        {
            var requestData = new
            {
                type = "getEmployeeByRfid",
                rfid_uid = rfidUid
            };
            
            var response = await SendRequestAsync<dynamic>(requestData);
            if (response == null || response.status?.ToString() != "ok")
            {
                Logger.LogError($"Ошибка получения информации о сотруднике по RFID: {response?.message}");
                return null;
            }
            
            try
            {
                // Извлекаем данные сотрудника из ответа
                dynamic userData = response.data ?? response;
                
                return new User
                {
                    Id = Convert.ToInt32(userData.id),
                    FirstName = userData.name?.ToString(),
                    LastName = userData.surname?.ToString(),
                    CardUID = rfidUid,
                    HasActiveSession = userData.has_active_session == true
                };
            }
            catch (Exception ex)
            {
                Logger.LogError($"Ошибка при обработке данных сотрудника по RFID: {ex.Message}", ex);
                return null;
            }
        }
        
        #endregion
    }
} 