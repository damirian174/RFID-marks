using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using RFID_marks.Models;

namespace RFID_marks.Services
{
    /// <summary>
    /// Сервис для работы с базой данных, аналог database.py
    /// </summary>
    public class DatabaseService
    {
        private static readonly HttpClient Client = new HttpClient();
        private static readonly string BaseUrl = "http://192.168.100.127:8000/";
        private static readonly Logger _logger = new Logger();

        /// <summary>
        /// Конструктор сервиса базы данных
        /// </summary>
        public DatabaseService()
        {
            Client.Timeout = TimeSpan.FromSeconds(10);
        }

        /// <summary>
        /// Выполнить запрос к базе данных
        /// </summary>
        /// <param name="data">Данные для отправки</param>
        /// <returns>Ответ сервера в виде JSON-объекта</returns>
        public async Task<JObject> ExecuteRequestAsync(JObject data)
        {
            try
            {
                string json = JsonConvert.SerializeObject(data);
                StringContent content = new StringContent(json, Encoding.UTF8, "application/json");
                
                _logger.LogEvent($"Отправка запроса к серверу: {json}");
                
                HttpResponseMessage response = await Client.PostAsync(BaseUrl, content);
                response.EnsureSuccessStatusCode();
                
                string responseBody = await response.Content.ReadAsStringAsync();
                _logger.LogEvent($"Ответ сервера: {responseBody}");
                
                return JObject.Parse(responseBody);
            }
            catch (HttpRequestException e)
            {
                _logger.LogError($"Ошибка HTTP при запросе к серверу: {e.Message}");
                return new JObject
                {
                    ["status"] = "error",
                    ["message"] = $"Ошибка соединения: {e.Message}"
                };
            }
            catch (TaskCanceledException)
            {
                _logger.LogError("Таймаут запроса к серверу");
                return new JObject
                {
                    ["status"] = "error",
                    ["message"] = "Превышено время ожидания ответа сервера"
                };
            }
            catch (Exception e)
            {
                _logger.LogError($"Неизвестная ошибка при запросе к серверу: {e.Message}");
                return new JObject
                {
                    ["status"] = "error",
                    ["message"] = $"Неизвестная ошибка: {e.Message}"
                };
            }
        }

        /// <summary>
        /// Синхронная версия запроса к серверу
        /// </summary>
        /// <param name="data">Данные для отправки</param>
        /// <returns>Ответ сервера в виде JSON-объекта</returns>
        public JObject ExecuteRequest(JObject data)
        {
            return ExecuteRequestAsync(data).GetAwaiter().GetResult();
        }

        /// <summary>
        /// Проверить соединение с сервером
        /// </summary>
        /// <returns>true, если соединение установлено</returns>
        public bool TestConnection()
        {
            try
            {
                JObject pingData = new JObject
                {
                    ["type"] = "ping"
                };
                
                JObject response = ExecuteRequest(pingData);
                return response["status"]?.ToString() == "ok";
            }
            catch (Exception e)
            {
                _logger.LogError($"Ошибка при проверке соединения: {e.Message}");
                return false;
            }
        }
    }
} 