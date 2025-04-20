using System;
using System.Threading.Tasks;

namespace RFID_marks_CSharp.Services
{
    /// <summary>
    /// Интерфейс сервиса для работы с RFID-считывателем
    /// </summary>
    public interface IRfidService
    {
        /// <summary>
        /// Событие, возникающее при считывании RFID-карты/метки
        /// </summary>
        event EventHandler<RfidReadEventArgs> RfidRead;

        /// <summary>
        /// Событие, возникающее при ошибке считывания RFID
        /// </summary>
        event EventHandler<RfidErrorEventArgs> RfidError;

        /// <summary>
        /// Событие, возникающее при изменении состояния подключения к считывателю
        /// </summary>
        event EventHandler<ConnectionStatusEventArgs> ConnectionStatusChanged;

        /// <summary>
        /// Инициализирует RFID-считыватель
        /// </summary>
        /// <param name="portName">Имя COM-порта</param>
        /// <param name="baudRate">Скорость передачи данных</param>
        /// <returns>True, если инициализация успешна</returns>
        Task<bool> InitializeAsync(string portName, int baudRate = 9600);

        /// <summary>
        /// Закрывает соединение с RFID-считывателем
        /// </summary>
        Task CloseAsync();

        /// <summary>
        /// Начинает сканирование RFID-меток
        /// </summary>
        Task StartScanningAsync();

        /// <summary>
        /// Останавливает сканирование RFID-меток
        /// </summary>
        Task StopScanningAsync();

        /// <summary>
        /// Записывает данные на RFID-метку
        /// </summary>
        /// <param name="data">Данные для записи</param>
        /// <returns>True, если запись успешна</returns>
        Task<bool> WriteDataAsync(string data);

        /// <summary>
        /// Считывает данные с RFID-метки
        /// </summary>
        /// <returns>Считанные данные</returns>
        Task<string> ReadDataAsync();

        /// <summary>
        /// Проверяет соединение с RFID-считывателем
        /// </summary>
        /// <returns>True, если соединение активно</returns>
        bool IsConnected();

        /// <summary>
        /// Получает список доступных COM-портов
        /// </summary>
        /// <returns>Массив имен доступных COM-портов</returns>
        string[] GetAvailablePorts();

        /// <summary>
        /// Устанавливает таймаут операций
        /// </summary>
        /// <param name="milliseconds">Таймаут в миллисекундах</param>
        void SetTimeout(int milliseconds);
    }

    /// <summary>
    /// Аргументы события считывания RFID-метки
    /// </summary>
    public class RfidReadEventArgs : EventArgs
    {
        /// <summary>
        /// Считанное значение RFID-метки
        /// </summary>
        public string TagValue { get; set; }

        /// <summary>
        /// Время считывания
        /// </summary>
        public DateTime ReadTime { get; set; }

        /// <summary>
        /// Сила сигнала (если поддерживается)
        /// </summary>
        public int SignalStrength { get; set; }

        /// <summary>
        /// Конструктор
        /// </summary>
        /// <param name="tagValue">Считанное значение RFID-метки</param>
        /// <param name="signalStrength">Сила сигнала</param>
        public RfidReadEventArgs(string tagValue, int signalStrength = 0)
        {
            TagValue = tagValue;
            ReadTime = DateTime.Now;
            SignalStrength = signalStrength;
        }
    }

    /// <summary>
    /// Аргументы события ошибки RFID
    /// </summary>
    public class RfidErrorEventArgs : EventArgs
    {
        /// <summary>
        /// Сообщение об ошибке
        /// </summary>
        public string ErrorMessage { get; set; }

        /// <summary>
        /// Исключение, вызвавшее ошибку
        /// </summary>
        public Exception Exception { get; set; }

        /// <summary>
        /// Код ошибки
        /// </summary>
        public int ErrorCode { get; set; }

        /// <summary>
        /// Время возникновения ошибки
        /// </summary>
        public DateTime ErrorTime { get; set; }

        /// <summary>
        /// Конструктор
        /// </summary>
        /// <param name="errorMessage">Сообщение об ошибке</param>
        /// <param name="exception">Исключение, вызвавшее ошибку</param>
        /// <param name="errorCode">Код ошибки</param>
        public RfidErrorEventArgs(string errorMessage, Exception exception = null, int errorCode = 0)
        {
            ErrorMessage = errorMessage;
            Exception = exception;
            ErrorCode = errorCode;
            ErrorTime = DateTime.Now;
        }
    }

    /// <summary>
    /// Аргументы события изменения состояния подключения
    /// </summary>
    public class ConnectionStatusEventArgs : EventArgs
    {
        /// <summary>
        /// Текущее состояние подключения
        /// </summary>
        public bool IsConnected { get; set; }

        /// <summary>
        /// Имя порта
        /// </summary>
        public string PortName { get; set; }

        /// <summary>
        /// Время изменения состояния
        /// </summary>
        public DateTime StatusChangeTime { get; set; }

        /// <summary>
        /// Причина изменения состояния
        /// </summary>
        public string Reason { get; set; }

        /// <summary>
        /// Конструктор
        /// </summary>
        /// <param name="isConnected">Состояние подключения</param>
        /// <param name="portName">Имя порта</param>
        /// <param name="reason">Причина изменения состояния</param>
        public ConnectionStatusEventArgs(bool isConnected, string portName, string reason = "")
        {
            IsConnected = isConnected;
            PortName = portName;
            StatusChangeTime = DateTime.Now;
            Reason = reason;
        }
    }
} 