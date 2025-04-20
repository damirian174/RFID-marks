using System;
using System.Collections.Generic;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель сессии пользователя, представляющая рабочий период
    /// </summary>
    public class Session
    {
        /// <summary>
        /// Уникальный идентификатор сессии
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Идентификатор сотрудника, открывшего сессию
        /// </summary>
        public int EmployeeId { get; set; }

        /// <summary>
        /// Ссылка на сотрудника, открывшего сессию
        /// </summary>
        public Employee Employee { get; set; }

        /// <summary>
        /// Время начала сессии
        /// </summary>
        public DateTime StartTime { get; set; }

        /// <summary>
        /// Время окончания сессии (null, если сессия активна)
        /// </summary>
        public DateTime? EndTime { get; set; }

        /// <summary>
        /// Общее время сессии в формате строки ЧЧ:ММ:СС
        /// </summary>
        public string TotalTime
        {
            get
            {
                TimeSpan duration;
                if (EndTime.HasValue)
                {
                    duration = EndTime.Value - StartTime;
                }
                else
                {
                    duration = DateTime.Now - StartTime;
                }

                return $"{(int)duration.TotalHours:00}:{duration.Minutes:00}:{duration.Seconds:00}";
            }
        }

        /// <summary>
        /// Список операций, выполненных в рамках сессии
        /// </summary>
        public List<Operation> Operations { get; set; }

        /// <summary>
        /// Список деталей, обработанных в рамках сессии
        /// </summary>
        public List<Part> ProcessedParts { get; set; }

        /// <summary>
        /// Текущая выбранная деталь
        /// </summary>
        public Part CurrentPart { get; set; }

        /// <summary>
        /// Текущая выполняемая операция
        /// </summary>
        public Operation CurrentOperation { get; set; }

        /// <summary>
        /// Проверяет, активна ли сессия в настоящее время
        /// </summary>
        public bool IsActive => !EndTime.HasValue;

        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public Session()
        {
            StartTime = DateTime.Now;
            Operations = new List<Operation>();
            ProcessedParts = new List<Part>();
        }

        /// <summary>
        /// Закрывает сессию, устанавливая время её окончания
        /// </summary>
        public void Close()
        {
            if (IsActive)
            {
                EndTime = DateTime.Now;
            }
        }

        /// <summary>
        /// Добавляет новую операцию в сессию
        /// </summary>
        /// <param name="operation">Операция для добавления</param>
        public void AddOperation(Operation operation)
        {
            Operations.Add(operation);
            CurrentOperation = operation;
        }

        /// <summary>
        /// Добавляет новую деталь в список обработанных
        /// </summary>
        /// <param name="part">Деталь для добавления</param>
        public void AddPart(Part part)
        {
            if (!ProcessedParts.Contains(part))
            {
                ProcessedParts.Add(part);
                CurrentPart = part;
            }
        }
    }
} 