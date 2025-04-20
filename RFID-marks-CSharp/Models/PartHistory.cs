using System;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель для отслеживания истории изменений детали
    /// </summary>
    public class PartHistory
    {
        /// <summary>
        /// Уникальный идентификатор записи истории
        /// </summary>
        public int Id { get; set; }
        
        /// <summary>
        /// Идентификатор детали
        /// </summary>
        public int PartId { get; set; }
        
        /// <summary>
        /// Идентификатор операции (опционально)
        /// </summary>
        public int? OperationId { get; set; }
        
        /// <summary>
        /// Идентификатор компонента (опционально)
        /// </summary>
        public int? ComponentId { get; set; }
        
        /// <summary>
        /// Идентификатор результата теста (опционально)
        /// </summary>
        public int? TestResultId { get; set; }
        
        /// <summary>
        /// Идентификатор сотрудника (опционально)
        /// </summary>
        public int? EmployeeId { get; set; }
        
        /// <summary>
        /// Временная метка события
        /// </summary>
        public DateTime Timestamp { get; set; }
        
        /// <summary>
        /// Описание события
        /// </summary>
        public string Description { get; set; }
        
        /// <summary>
        /// Дополнительные данные, связанные с событием (в JSON формате)
        /// </summary>
        public string ExtraData { get; set; }
        
        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public PartHistory()
        {
            Timestamp = DateTime.Now;
        }
        
        /// <summary>
        /// Форматирует информацию о событии для отображения в интерфейсе
        /// </summary>
        public string FormatDisplayInfo()
        {
            return $"{Timestamp:dd.MM.yyyy HH:mm:ss}: {Description}";
        }
    }
} 