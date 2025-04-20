using System;
using System.Collections.Generic;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель детали/изделия, проходящего через процесс производства
    /// </summary>
    public class Part
    {
        /// <summary>
        /// Уникальный идентификатор детали
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Артикул детали
        /// </summary>
        public string ArticleNumber { get; set; }

        /// <summary>
        /// Наименование детали
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Серийный номер детали
        /// </summary>
        public string SerialNumber { get; set; }

        /// <summary>
        /// Номер партии
        /// </summary>
        public string BatchNumber { get; set; }

        /// <summary>
        /// Дата создания записи о детали
        /// </summary>
        public DateTime CreatedAt { get; set; }

        /// <summary>
        /// Текущее состояние детали (например, "Сборка", "Маркировка", "Тестирование", "Упаковка", "Готово")
        /// </summary>
        public string Status { get; set; }

        /// <summary>
        /// Текущий этап производства (по номеру операции)
        /// </summary>
        public int CurrentStage { get; set; }

        /// <summary>
        /// RFID-метка, связанная с деталью
        /// </summary>
        public string RfidTag { get; set; }

        /// <summary>
        /// QR-код для маркировки
        /// </summary>
        public string QrCode { get; set; }

        /// <summary>
        /// История операций, выполненных с данной деталью
        /// </summary>
        public List<Operation> Operations { get; set; }

        /// <summary>
        /// История взаимодействий с деталью
        /// </summary>
        public List<PartHistory> History { get; set; }

        /// <summary>
        /// Список компонентов, используемых в данной детали
        /// </summary>
        public List<Component> Components { get; set; }

        /// <summary>
        /// Результаты тестирования детали
        /// </summary>
        public List<TestResult> TestResults { get; set; }

        /// <summary>
        /// Флаг, указывающий, прошла ли деталь проверку качества
        /// </summary>
        public bool QualityChecked { get; set; }

        /// <summary>
        /// Флаг, указывающий, имеет ли деталь маркировку
        /// </summary>
        public bool IsMarked { get; set; }

        /// <summary>
        /// Флаг, указывающий, упакована ли деталь
        /// </summary>
        public bool IsPacked { get; set; }

        /// <summary>
        /// Время, затраченное на производство детали (в минутах)
        /// </summary>
        public double ProductionTimeMinutes { get; set; }

        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public Part()
        {
            CreatedAt = DateTime.Now;
            Status = "Новая";
            CurrentStage = 0;
            Operations = new List<Operation>();
            History = new List<PartHistory>();
            Components = new List<Component>();
            TestResults = new List<TestResult>();
            QualityChecked = false;
            IsMarked = false;
            IsPacked = false;
            ProductionTimeMinutes = 0;
        }

        /// <summary>
        /// Добавляет новую операцию к детали
        /// </summary>
        /// <param name="operation">Операция для добавления</param>
        public void AddOperation(Operation operation)
        {
            Operations.Add(operation);
            
            // Обновляем статус и этап детали в зависимости от операции
            if (operation.OperationType == "Сборка")
            {
                Status = "Сборка";
                CurrentStage = Math.Max(CurrentStage, operation.StageNumber);
            }
            else if (operation.OperationType == "Маркировка")
            {
                Status = "Маркировка";
                IsMarked = true;
            }
            else if (operation.OperationType == "Тестирование")
            {
                Status = "Тестирование";
                QualityChecked = true;
            }
            else if (operation.OperationType == "Упаковка")
            {
                Status = "Упаковка";
                IsPacked = true;
            }

            // Добавляем запись в историю
            History.Add(new PartHistory
            {
                PartId = Id,
                OperationId = operation.Id,
                EmployeeId = operation.EmployeeId,
                Timestamp = DateTime.Now,
                Description = $"Выполнена операция: {operation.Name}"
            });
        }

        /// <summary>
        /// Проверяет, завершена ли работа с деталью
        /// </summary>
        /// <returns>True, если деталь прошла все этапы производства</returns>
        public bool IsCompleted()
        {
            return IsMarked && QualityChecked && IsPacked;
        }

        /// <summary>
        /// Генерирует QR-код для детали
        /// </summary>
        public void GenerateQrCode()
        {
            // В реальном приложении здесь будет логика генерации QR-кода
            QrCode = $"{ArticleNumber}-{SerialNumber}-{BatchNumber}";
        }

        /// <summary>
        /// Добавляет компонент к детали
        /// </summary>
        /// <param name="component">Компонент для добавления</param>
        public void AddComponent(Component component)
        {
            Components.Add(component);
            
            // Добавляем запись в историю
            History.Add(new PartHistory
            {
                PartId = Id,
                ComponentId = component.Id,
                Timestamp = DateTime.Now,
                Description = $"Добавлен компонент: {component.Name} (SN: {component.SerialNumber})"
            });
        }

        /// <summary>
        /// Добавляет результат тестирования
        /// </summary>
        /// <param name="result">Результат тестирования</param>
        public void AddTestResult(TestResult result)
        {
            TestResults.Add(result);
            
            // Добавляем запись в историю
            History.Add(new PartHistory
            {
                PartId = Id,
                TestResultId = result.Id,
                Timestamp = DateTime.Now,
                Description = $"Тест: {result.TestName}, Результат: {(result.Passed ? "Пройден" : "Не пройден")}"
            });
        }
    }

    /// <summary>
    /// Модель операции над изделием
    /// </summary>
    public class PartOperation
    {
        /// <summary>
        /// Идентификатор операции
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Идентификатор изделия
        /// </summary>
        public int PartId { get; set; }

        /// <summary>
        /// Наименование операции
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Описание операции
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Идентификатор сотрудника, выполнившего операцию
        /// </summary>
        public int EmployeeId { get; set; }

        /// <summary>
        /// Время начала операции
        /// </summary>
        public DateTime StartTime { get; set; }

        /// <summary>
        /// Время завершения операции
        /// </summary>
        public DateTime? EndTime { get; set; }

        /// <summary>
        /// Статус операции (В процессе, Завершено, Ошибка)
        /// </summary>
        public string Status { get; set; }

        /// <summary>
        /// Результат операции в формате JSON
        /// </summary>
        public string Result { get; set; }

        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public PartOperation()
        {
            StartTime = DateTime.Now;
            Status = "В процессе";
        }
    }
} 