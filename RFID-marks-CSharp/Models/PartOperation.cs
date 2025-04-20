using System;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель операции над деталью
    /// </summary>
    public class PartOperation
    {
        /// <summary>
        /// Идентификатор операции
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Идентификатор сессии
        /// </summary>
        public int SessionId { get; set; }

        /// <summary>
        /// Идентификатор детали
        /// </summary>
        public int PartId { get; set; }

        /// <summary>
        /// Деталь, над которой выполняется операция
        /// </summary>
        public Part Part { get; set; }

        /// <summary>
        /// Тип операции (например, "Сборка", "Маркировка", "Тестирование", "Упаковка")
        /// </summary>
        public string OperationType { get; set; }

        /// <summary>
        /// Подтип операции или шаг (например, "Установка платы", "Проверка кабелей", "Финальное тестирование")
        /// </summary>
        public string OperationSubtype { get; set; }
        
        /// <summary>
        /// Время начала операции
        /// </summary>
        public DateTime StartTime { get; set; }

        /// <summary>
        /// Время окончания операции
        /// </summary>
        public DateTime? EndTime { get; set; }

        /// <summary>
        /// Статус операции (например, "В процессе", "Завершена", "Отменена", "Ошибка")
        /// </summary>
        public string Status { get; set; }

        /// <summary>
        /// Результат операции (например, "Успешно", "Брак", "Требуется проверка")
        /// </summary>
        public string Result { get; set; }

        /// <summary>
        /// Продолжительность операции в секундах
        /// </summary>
        public double DurationSeconds
        {
            get
            {
                if (EndTime.HasValue)
                {
                    return (EndTime.Value - StartTime).TotalSeconds;
                }
                else
                {
                    return (DateTime.Now - StartTime).TotalSeconds;
                }
            }
        }

        /// <summary>
        /// Индикатор успешности операции
        /// </summary>
        public bool IsSuccessful { get; set; }

        /// <summary>
        /// Код ошибки (если есть)
        /// </summary>
        public string ErrorCode { get; set; }

        /// <summary>
        /// Описание ошибки
        /// </summary>
        public string ErrorDescription { get; set; }

        /// <summary>
        /// Идентификатор сотрудника, выполнившего операцию
        /// </summary>
        public int EmployeeId { get; set; }

        /// <summary>
        /// Примечания к операции
        /// </summary>
        public string Notes { get; set; }

        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public PartOperation()
        {
            StartTime = DateTime.Now;
            Status = "В процессе";
            IsSuccessful = false;
        }
    }
} 