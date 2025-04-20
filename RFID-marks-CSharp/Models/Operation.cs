using System;
using System.Collections.Generic;

namespace RFID_marks.Models
{
    /// <summary>
    /// Представляет операцию с деталью
    /// </summary>
    public class Operation
    {
        /// <summary>
        /// Уникальный идентификатор операции
        /// </summary>
        public string Id { get; set; }
        
        /// <summary>
        /// Тип операции (Сборка, Маркировка, Тестирование, Упаковка)
        /// </summary>
        public string Type { get; set; }
        
        /// <summary>
        /// Описание операции
        /// </summary>
        public string Description { get; set; }
        
        /// <summary>
        /// Текущий статус операции (Новая, Выполняется, Приостановлена, Завершена, Ошибка)
        /// </summary>
        public string Status { get; set; }
        
        /// <summary>
        /// Идентификатор детали, над которой выполняется операция
        /// </summary>
        public string DetailId { get; set; }
        
        /// <summary>
        /// Идентификатор пользователя, выполняющего операцию
        /// </summary>
        public int UserId { get; set; }
        
        /// <summary>
        /// Имя пользователя, выполняющего операцию
        /// </summary>
        public string UserName { get; set; }
        
        /// <summary>
        /// Дата начала операции
        /// </summary>
        public DateTime StartTime { get; set; }
        
        /// <summary>
        /// Дата завершения операции
        /// </summary>
        public DateTime? EndTime { get; set; }
        
        /// <summary>
        /// Длительность операции в формате "HH:MM:SS"
        /// </summary>
        public string Duration 
        { 
            get 
            {
                TimeSpan span;
                if (EndTime.HasValue)
                {
                    span = EndTime.Value - StartTime;
                }
                else
                {
                    span = DateTime.Now - StartTime;
                }
                
                return $"{(int)span.TotalHours:D2}:{span.Minutes:D2}:{span.Seconds:D2}";
            } 
        }
        
        /// <summary>
        /// Сообщение об ошибке (если есть)
        /// </summary>
        public string ErrorMessage { get; set; }
        
        /// <summary>
        /// Список шагов операции
        /// </summary>
        public List<OperationStep> Steps { get; set; }
        
        /// <summary>
        /// Текущий шаг операции
        /// </summary>
        public OperationStep CurrentStep { get; set; }
        
        /// <summary>
        /// Список параметров операции
        /// </summary>
        public Dictionary<string, string> Parameters { get; set; }
        
        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public Operation()
        {
            Id = Guid.NewGuid().ToString();
            StartTime = DateTime.Now;
            Status = "Новая";
            Steps = new List<OperationStep>();
            Parameters = new Dictionary<string, string>();
        }
        
        /// <summary>
        /// Создает новую операцию с указанным типом и описанием
        /// </summary>
        /// <param name="type">Тип операции</param>
        /// <param name="description">Описание операции</param>
        /// <param name="userId">Идентификатор пользователя</param>
        /// <param name="userName">Имя пользователя</param>
        /// <param name="detailId">Идентификатор детали</param>
        public Operation(string type, string description, int userId, string userName, string detailId)
            : this()
        {
            Type = type;
            Description = description;
            UserId = userId;
            UserName = userName;
            DetailId = detailId;
        }
        
        /// <summary>
        /// Начинает операцию
        /// </summary>
        public void Start()
        {
            Status = "Выполняется";
            StartTime = DateTime.Now;
            EndTime = null;
            
            // Если есть шаги, активируем первый
            if (Steps.Count > 0)
            {
                CurrentStep = Steps[0];
                CurrentStep.Start();
            }
        }
        
        /// <summary>
        /// Приостанавливает операцию
        /// </summary>
        public void Pause()
        {
            Status = "Приостановлена";
            
            // Приостанавливаем текущий шаг
            CurrentStep?.Pause();
        }
        
        /// <summary>
        /// Возобновляет операцию
        /// </summary>
        public void Resume()
        {
            Status = "Выполняется";
            
            // Возобновляем текущий шаг
            CurrentStep?.Resume();
        }
        
        /// <summary>
        /// Завершает операцию
        /// </summary>
        public void Complete()
        {
            Status = "Завершена";
            EndTime = DateTime.Now;
            
            // Завершаем текущий шаг, если он активен
            CurrentStep?.Complete();
        }
        
        /// <summary>
        /// Отмечает операцию как ошибочную
        /// </summary>
        /// <param name="errorMessage">Сообщение об ошибке</param>
        public void MarkError(string errorMessage)
        {
            Status = "Ошибка";
            ErrorMessage = errorMessage;
            EndTime = DateTime.Now;
            
            // Отмечаем текущий шаг как ошибочный, если он активен
            CurrentStep?.MarkError(errorMessage);
        }
        
        /// <summary>
        /// Добавляет шаг к операции
        /// </summary>
        /// <param name="step">Шаг операции</param>
        public void AddStep(OperationStep step)
        {
            Steps.Add(step);
            
            // Если это первый шаг и операция выполняется, активируем его
            if (Steps.Count == 1 && Status == "Выполняется")
            {
                CurrentStep = step;
                CurrentStep.Start();
            }
        }
        
        /// <summary>
        /// Переходит к следующему шагу операции
        /// </summary>
        /// <returns>True, если переход выполнен успешно, иначе False</returns>
        public bool NextStep()
        {
            if (CurrentStep == null)
            {
                if (Steps.Count > 0)
                {
                    CurrentStep = Steps[0];
                    CurrentStep.Start();
                    return true;
                }
                return false;
            }
            
            int currentIndex = Steps.IndexOf(CurrentStep);
            if (currentIndex >= 0 && currentIndex < Steps.Count - 1)
            {
                // Завершаем текущий шаг
                CurrentStep.Complete();
                
                // Переходим к следующему шагу
                CurrentStep = Steps[currentIndex + 1];
                CurrentStep.Start();
                return true;
            }
            
            return false;
        }
        
        /// <summary>
        /// Добавляет параметр к операции
        /// </summary>
        /// <param name="key">Ключ параметра</param>
        /// <param name="value">Значение параметра</param>
        public void AddParameter(string key, string value)
        {
            Parameters[key] = value;
        }
        
        /// <summary>
        /// Возвращает строковое представление операции
        /// </summary>
        /// <returns>Строковое представление операции</returns>
        public override string ToString()
        {
            return $"{Type} - {Description} ({Status})";
        }
    }
    
    /// <summary>
    /// Представляет шаг операции
    /// </summary>
    public class OperationStep
    {
        /// <summary>
        /// Уникальный идентификатор шага
        /// </summary>
        public string Id { get; set; }
        
        /// <summary>
        /// Название шага
        /// </summary>
        public string Name { get; set; }
        
        /// <summary>
        /// Описание шага
        /// </summary>
        public string Description { get; set; }
        
        /// <summary>
        /// Порядковый номер шага
        /// </summary>
        public int Order { get; set; }
        
        /// <summary>
        /// Статус шага (Новый, Выполняется, Приостановлен, Завершен, Ошибка)
        /// </summary>
        public string Status { get; set; }
        
        /// <summary>
        /// Время начала шага
        /// </summary>
        public DateTime? StartTime { get; set; }
        
        /// <summary>
        /// Время завершения шага
        /// </summary>
        public DateTime? EndTime { get; set; }
        
        /// <summary>
        /// Сообщение об ошибке (если есть)
        /// </summary>
        public string ErrorMessage { get; set; }
        
        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public OperationStep()
        {
            Id = Guid.NewGuid().ToString();
            Status = "Новый";
        }
        
        /// <summary>
        /// Создает новый шаг с указанным названием и описанием
        /// </summary>
        /// <param name="name">Название шага</param>
        /// <param name="description">Описание шага</param>
        /// <param name="order">Порядковый номер шага</param>
        public OperationStep(string name, string description, int order)
            : this()
        {
            Name = name;
            Description = description;
            Order = order;
        }
        
        /// <summary>
        /// Начинает выполнение шага
        /// </summary>
        public void Start()
        {
            Status = "Выполняется";
            StartTime = DateTime.Now;
            EndTime = null;
        }
        
        /// <summary>
        /// Приостанавливает выполнение шага
        /// </summary>
        public void Pause()
        {
            Status = "Приостановлен";
        }
        
        /// <summary>
        /// Возобновляет выполнение шага
        /// </summary>
        public void Resume()
        {
            Status = "Выполняется";
        }
        
        /// <summary>
        /// Завершает выполнение шага
        /// </summary>
        public void Complete()
        {
            Status = "Завершен";
            EndTime = DateTime.Now;
        }
        
        /// <summary>
        /// Отмечает шаг как ошибочный
        /// </summary>
        /// <param name="errorMessage">Сообщение об ошибке</param>
        public void MarkError(string errorMessage)
        {
            Status = "Ошибка";
            ErrorMessage = errorMessage;
            EndTime = DateTime.Now;
        }
        
        /// <summary>
        /// Возвращает строковое представление шага
        /// </summary>
        /// <returns>Строковое представление шага</returns>
        public override string ToString()
        {
            return $"{Order}. {Name} ({Status})";
        }
    }
} 