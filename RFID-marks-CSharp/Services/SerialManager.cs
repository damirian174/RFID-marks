using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RFID_marks.Models;

namespace RFID_marks.Services
{
    /// <summary>
    /// Класс для управления последовательным портом и работы с RFID-устройством
    /// </summary>
    public class SerialManager : IDisposable
    {
        private SerialPort _serialPort;
        private bool _isConnected;
        private string _portName;
        private int _baudRate;
        private byte[] _buffer;
        private const int BUFFER_SIZE = 1024;

        /// <summary>
        /// Событие получения данных с устройства
        /// </summary>
        public event EventHandler<SerialDataEventArgs> DataReceived;

        /// <summary>
        /// Событие потери соединения
        /// </summary>
        public event EventHandler ConnectionLost;

        /// <summary>
        /// Проверяет, подключен ли порт
        /// </summary>
        public bool IsConnected => _isConnected && _serialPort != null && _serialPort.IsOpen;

        /// <summary>
        /// Имя используемого порта
        /// </summary>
        public string PortName => _portName;

        /// <summary>
        /// Скорость связи
        /// </summary>
        public int BaudRate => _baudRate;

        /// <summary>
        /// Конструктор класса
        /// </summary>
        public SerialManager()
        {
            _buffer = new byte[BUFFER_SIZE];
            _isConnected = false;
        }

        /// <summary>
        /// Получает список доступных COM-портов
        /// </summary>
        /// <returns>Список имен портов</returns>
        public List<string> GetAvailablePorts()
        {
            return SerialPort.GetPortNames().ToList();
        }

        /// <summary>
        /// Подключается к указанному COM-порту
        /// </summary>
        /// <param name="portName">Имя порта</param>
        /// <param name="baudRate">Скорость передачи</param>
        /// <param name="parity">Четность</param>
        /// <param name="dataBits">Биты данных</param>
        /// <param name="stopBits">Стоповые биты</param>
        /// <returns>Результат операции</returns>
        public bool Connect(string portName, int baudRate = 9600, Parity parity = Parity.None, int dataBits = 8, StopBits stopBits = StopBits.One)
        {
            try
            {
                if (_serialPort != null && _serialPort.IsOpen)
                {
                    Disconnect();
                }

                _portName = portName;
                _baudRate = baudRate;

                _serialPort = new SerialPort(portName, baudRate, parity, dataBits, stopBits)
                {
                    ReadTimeout = 500,
                    WriteTimeout = 500,
                    DtrEnable = true,
                    RtsEnable = true
                };

                _serialPort.DataReceived += SerialPort_DataReceived;
                _serialPort.ErrorReceived += SerialPort_ErrorReceived;
                _serialPort.Open();

                _isConnected = true;
                Logger.Info("SerialManager", $"Соединение с портом {portName} установлено. Скорость: {baudRate}");
                return true;
            }
            catch (Exception ex)
            {
                Logger.Error("SerialManager", ex, $"Ошибка при подключении к порту {portName}");
                _isConnected = false;
                return false;
            }
        }

        /// <summary>
        /// Отключается от COM-порта
        /// </summary>
        public void Disconnect()
        {
            try
            {
                if (_serialPort != null && _serialPort.IsOpen)
                {
                    _serialPort.DataReceived -= SerialPort_DataReceived;
                    _serialPort.ErrorReceived -= SerialPort_ErrorReceived;
                    _serialPort.Close();
                    _serialPort.Dispose();
                    _serialPort = null;
                    _isConnected = false;
                    Logger.Info("SerialManager", "Соединение с портом закрыто");
                }
            }
            catch (Exception ex)
            {
                Logger.Error("SerialManager", ex, "Ошибка при отключении от порта");
            }
        }

        /// <summary>
        /// Записывает данные в RFID-метку
        /// </summary>
        /// <param name="data">Данные для записи</param>
        /// <returns>Успешность операции</returns>
        public bool WriteToTag(string data)
        {
            if (!IsConnected)
            {
                Logger.Warning("SerialManager", "Невозможно записать данные: порт не подключен");
                return false;
            }

            try
            {
                // Преобразуем команду записи в формат RFID-считывателя
                // Пример: W:DATA - где W - команда записи, DATA - данные для записи
                string command = $"W:{data}\r\n";
                _serialPort.Write(command);
                Logger.Info("SerialManager", $"Отправлена команда записи: {command}");
                return true;
            }
            catch (Exception ex)
            {
                Logger.Error("SerialManager", ex, "Ошибка при записи данных в RFID-метку");
                CheckConnectionLost(ex);
                return false;
            }
        }

        /// <summary>
        /// Отправляет команду на чтение RFID-метки
        /// </summary>
        /// <returns>Успешность операции</returns>
        public bool ReadFromTag()
        {
            if (!IsConnected)
            {
                Logger.Warning("SerialManager", "Невозможно прочитать данные: порт не подключен");
                return false;
            }

            try
            {
                // Отправляем команду чтения RFID-метки
                // Пример: R - где R - команда чтения
                string command = "R\r\n";
                _serialPort.Write(command);
                Logger.Info("SerialManager", "Отправлена команда чтения RFID-метки");
                return true;
            }
            catch (Exception ex)
            {
                Logger.Error("SerialManager", ex, "Ошибка при отправке команды чтения RFID-метки");
                CheckConnectionLost(ex);
                return false;
            }
        }

        /// <summary>
        /// Отправляет произвольную команду на устройство
        /// </summary>
        /// <param name="command">Команда для отправки</param>
        /// <returns>Успешность операции</returns>
        public bool SendCommand(string command)
        {
            if (!IsConnected)
            {
                Logger.Warning("SerialManager", "Невозможно отправить команду: порт не подключен");
                return false;
            }

            try
            {
                if (!command.EndsWith("\r\n"))
                {
                    command += "\r\n";
                }

                _serialPort.Write(command);
                Logger.Info("SerialManager", $"Отправлена команда: {command.Trim()}");
                return true;
            }
            catch (Exception ex)
            {
                Logger.Error("SerialManager", ex, "Ошибка при отправке команды");
                CheckConnectionLost(ex);
                return false;
            }
        }

        /// <summary>
        /// Обрабатывает получение данных с COM-порта
        /// </summary>
        private void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            try
            {
                if (_serialPort == null || !_serialPort.IsOpen)
                {
                    return;
                }

                int bytesToRead = _serialPort.BytesToRead;
                if (bytesToRead > 0)
                {
                    byte[] buffer = new byte[bytesToRead];
                    int bytesRead = _serialPort.Read(buffer, 0, bytesToRead);

                    if (bytesRead > 0)
                    {
                        string data = Encoding.ASCII.GetString(buffer, 0, bytesRead);
                        Logger.Debug("SerialManager", $"Получены данные от устройства: {data.Trim()}");

                        // Вызываем событие получения данных
                        DataReceived?.Invoke(this, new SerialDataEventArgs(data));
                    }
                }
            }
            catch (Exception ex)
            {
                Logger.Error("SerialManager", ex, "Ошибка при чтении данных с COM-порта");
                CheckConnectionLost(ex);
            }
        }

        /// <summary>
        /// Обрабатывает ошибки COM-порта
        /// </summary>
        private void SerialPort_ErrorReceived(object sender, SerialErrorReceivedEventArgs e)
        {
            Logger.Error("SerialManager", $"Ошибка COM-порта: {e.EventType}");
            
            // Проверяем соединение после ошибки
            if (_serialPort != null)
            {
                try
                {
                    if (!_serialPort.IsOpen)
                    {
                        OnConnectionLost();
                    }
                }
                catch
                {
                    OnConnectionLost();
                }
            }
        }

        /// <summary>
        /// Проверяет, не потеряно ли соединение с устройством
        /// </summary>
        private void CheckConnectionLost(Exception ex)
        {
            // Проверяем, не связана ли ошибка с потерей соединения
            if (ex is InvalidOperationException || 
                ex is System.IO.IOException || 
                ex is TimeoutException)
            {
                OnConnectionLost();
            }
        }

        /// <summary>
        /// Вызывает событие потери соединения
        /// </summary>
        private void OnConnectionLost()
        {
            if (_isConnected)
            {
                _isConnected = false;
                Logger.Warning("SerialManager", "Соединение с устройством потеряно");
                
                try
                {
                    if (_serialPort != null && _serialPort.IsOpen)
                    {
                        _serialPort.Close();
                    }
                }
                catch (Exception ex)
                {
                    Logger.Error("SerialManager", ex, "Ошибка при закрытии порта после потери соединения");
                }

                // Вызываем событие потери соединения
                ConnectionLost?.Invoke(this, EventArgs.Empty);
            }
        }

        /// <summary>
        /// Освобождает ресурсы
        /// </summary>
        public void Dispose()
        {
            Disconnect();
        }
    }

    /// <summary>
    /// Класс аргументов события получения данных
    /// </summary>
    public class SerialDataEventArgs : EventArgs
    {
        /// <summary>
        /// Данные, полученные с устройства
        /// </summary>
        public string Data { get; }

        /// <summary>
        /// Пытается разобрать данные как ответ от RFID-устройства
        /// </summary>
        public RfidResponse Response
        {
            get
            {
                // Пытаемся разобрать ответ от RFID-устройства
                if (string.IsNullOrEmpty(Data))
                {
                    return null;
                }

                try
                {
                    return RfidResponse.Parse(Data);
                }
                catch
                {
                    return null;
                }
            }
        }

        /// <summary>
        /// Конструктор класса
        /// </summary>
        /// <param name="data">Полученные данные</param>
        public SerialDataEventArgs(string data)
        {
            Data = data;
        }
    }

    /// <summary>
    /// Класс для представления ответа от RFID-устройства
    /// </summary>
    public class RfidResponse
    {
        /// <summary>
        /// Тип операции
        /// </summary>
        public RfidOperationType OperationType { get; set; }

        /// <summary>
        /// Успешность выполнения
        /// </summary>
        public bool IsSuccess { get; set; }

        /// <summary>
        /// Сообщение об ошибке (если есть)
        /// </summary>
        public string ErrorMessage { get; set; }

        /// <summary>
        /// Данные (если есть)
        /// </summary>
        public string Data { get; set; }

        /// <summary>
        /// Разбирает строку ответа от RFID-устройства
        /// </summary>
        /// <param name="responseString">Строка ответа</param>
        /// <returns>Объект ответа от RFID-устройства</returns>
        public static RfidResponse Parse(string responseString)
        {
            // Примеры форматов ответов:
            // R:OK:DATA - успешное чтение
            // R:ERR:ERROR_MESSAGE - ошибка чтения
            // W:OK - успешная запись
            // W:ERR:ERROR_MESSAGE - ошибка записи

            if (string.IsNullOrEmpty(responseString))
            {
                throw new ArgumentException("Пустая строка ответа", nameof(responseString));
            }

            string[] parts = responseString.Trim().Split(':');
            if (parts.Length < 2)
            {
                throw new FormatException("Неверный формат ответа от RFID-устройства");
            }

            RfidResponse response = new RfidResponse();

            // Определяем тип операции
            switch (parts[0].ToUpper())
            {
                case "R":
                    response.OperationType = RfidOperationType.Read;
                    break;
                case "W":
                    response.OperationType = RfidOperationType.Write;
                    break;
                default:
                    response.OperationType = RfidOperationType.Unknown;
                    break;
            }

            // Определяем успешность
            response.IsSuccess = parts[1].ToUpper() == "OK";

            // Если неуспешно, получаем сообщение об ошибке
            if (!response.IsSuccess && parts.Length > 2)
            {
                response.ErrorMessage = parts[2];
            }

            // Если это чтение и оно успешно, получаем данные
            if (response.OperationType == RfidOperationType.Read && response.IsSuccess && parts.Length > 2)
            {
                response.Data = parts[2];
            }

            return response;
        }
    }

    /// <summary>
    /// Типы операций с RFID-устройством
    /// </summary>
    public enum RfidOperationType
    {
        /// <summary>
        /// Неизвестная операция
        /// </summary>
        Unknown,

        /// <summary>
        /// Чтение
        /// </summary>
        Read,

        /// <summary>
        /// Запись
        /// </summary>
        Write
    }
} 