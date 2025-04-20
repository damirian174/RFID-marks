using System;
using System.Collections.Generic;

namespace RFID_marks.Models
{
    /// <summary>
    /// Представляет информацию о детали
    /// </summary>
    public class Detail
    {
        /// <summary>
        /// Уникальный идентификатор детали
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Серийный номер детали
        /// </summary>
        public string SerialNumber { get; set; }

        /// <summary>
        /// Название детали
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Тип детали
        /// </summary>
        public string Type { get; set; }

        /// <summary>
        /// Модель детали
        /// </summary>
        public string Model { get; set; }

        /// <summary>
        /// Описание детали
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Дата производства детали
        /// </summary>
        public DateTime ManufactureDate { get; set; }

        /// <summary>
        /// Код партии
        /// </summary>
        public string BatchCode { get; set; }

        /// <summary>
        /// Текущий статус детали
        /// </summary>
        public DetailStatus Status { get; set; }

        /// <summary>
        /// Текущий этап производства
        /// </summary>
        public ProductionStage Stage { get; set; }

        /// <summary>
        /// Идентификатор RFID метки
        /// </summary>
        public string RfidTagId { get; set; }

        /// <summary>
        /// Список операций, выполненных над деталью
        /// </summary>
        public List<Operation> Operations { get; set; } = new List<Operation>();

        /// <summary>
        /// Текущая операция, выполняемая над деталью
        /// </summary>
        public Operation CurrentOperation { get; set; }

        /// <summary>
        /// Список компонентов детали
        /// </summary>
        public List<DetailComponent> Components { get; set; } = new List<DetailComponent>();

        /// <summary>
        /// Список результатов тестирования
        /// </summary>
        public List<TestResult> TestResults { get; set; } = new List<TestResult>();

        /// <summary>
        /// Список проблем, связанных с деталью
        /// </summary>
        public List<Issue> Issues { get; set; } = new List<Issue>();

        /// <summary>
        /// Конструктор с параметрами
        /// </summary>
        /// <param name="id">Идентификатор детали</param>
        /// <param name="serialNumber">Серийный номер</param>
        /// <param name="name">Название детали</param>
        public Detail(string id, string serialNumber, string name)
        {
            Id = id;
            SerialNumber = serialNumber;
            Name = name;
            ManufactureDate = DateTime.Now;
            Status = DetailStatus.Created;
            Stage = ProductionStage.Assembly;
            Operations = new List<Operation>();
            Components = new List<DetailComponent>();
            TestResults = new List<TestResult>();
            Issues = new List<Issue>();
        }

        /// <summary>
        /// Конструктор без параметров
        /// </summary>
        public Detail()
        {
            ManufactureDate = DateTime.Now;
            Status = DetailStatus.Created;
            Stage = ProductionStage.Assembly;
            Operations = new List<Operation>();
            Components = new List<DetailComponent>();
            TestResults = new List<TestResult>();
            Issues = new List<Issue>();
        }

        /// <summary>
        /// Добавляет новую операцию к детали
        /// </summary>
        /// <param name="operation">Операция</param>
        public void AddOperation(Operation operation)
        {
            Operations.Add(operation);
            CurrentOperation = operation;
        }

        /// <summary>
        /// Добавляет компонент к детали
        /// </summary>
        /// <param name="component">Компонент</param>
        public void AddComponent(DetailComponent component)
        {
            Components.Add(component);
        }

        /// <summary>
        /// Добавляет результат тестирования к детали
        /// </summary>
        /// <param name="testResult">Результат тестирования</param>
        public void AddTestResult(TestResult testResult)
        {
            TestResults.Add(testResult);
            
            // Обновление статуса детали в зависимости от результата теста
            if (testResult.IsPassed && Status != DetailStatus.Failed)
            {
                Status = DetailStatus.Tested;
            }
            else if (!testResult.IsPassed)
            {
                Status = DetailStatus.Failed;
            }
        }

        /// <summary>
        /// Добавляет проблему к детали
        /// </summary>
        /// <param name="issue">Проблема</param>
        public void AddIssue(Issue issue)
        {
            Issues.Add(issue);
            
            // Обновление статуса детали при обнаружении проблемы
            if (issue.Severity == IssueSeverity.Critical)
            {
                Status = DetailStatus.Failed;
            }
        }

        /// <summary>
        /// Переход на следующий этап производства
        /// </summary>
        public void MoveToNextStage()
        {
            switch (Stage)
            {
                case ProductionStage.Assembly:
                    Stage = ProductionStage.Marking;
                    break;
                case ProductionStage.Marking:
                    Stage = ProductionStage.Testing;
                    break;
                case ProductionStage.Testing:
                    Stage = ProductionStage.Packing;
                    break;
                case ProductionStage.Packing:
                    Stage = ProductionStage.Completed;
                    Status = DetailStatus.Completed;
                    break;
            }
        }
    }

    /// <summary>
    /// Статусы детали
    /// </summary>
    public enum DetailStatus
    {
        /// <summary>
        /// Деталь создана
        /// </summary>
        Created,

        /// <summary>
        /// Деталь в процессе сборки
        /// </summary>
        InAssembly,

        /// <summary>
        /// Деталь собрана
        /// </summary>
        Assembled,

        /// <summary>
        /// Деталь маркирована
        /// </summary>
        Marked,

        /// <summary>
        /// Деталь протестирована
        /// </summary>
        Tested,

        /// <summary>
        /// Деталь упакована
        /// </summary>
        Packed,

        /// <summary>
        /// Деталь завершена (готова к отправке)
        /// </summary>
        Completed,

        /// <summary>
        /// Деталь не прошла контроль качества
        /// </summary>
        Failed
    }

    /// <summary>
    /// Этапы производства
    /// </summary>
    public enum ProductionStage
    {
        /// <summary>
        /// Этап сборки
        /// </summary>
        Assembly,

        /// <summary>
        /// Этап маркировки
        /// </summary>
        Marking,

        /// <summary>
        /// Этап тестирования
        /// </summary>
        Testing,

        /// <summary>
        /// Этап упаковки
        /// </summary>
        Packing,

        /// <summary>
        /// Производство завершено
        /// </summary>
        Completed
    }

    /// <summary>
    /// Компонент детали
    /// </summary>
    public class DetailComponent
    {
        /// <summary>
        /// Идентификатор компонента
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Название компонента
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Серийный номер компонента
        /// </summary>
        public string SerialNumber { get; set; }

        /// <summary>
        /// Тип компонента
        /// </summary>
        public string Type { get; set; }

        /// <summary>
        /// Описание компонента
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Идентификатор родительской детали
        /// </summary>
        public string ParentDetailId { get; set; }
    }

    /// <summary>
    /// Результат тестирования
    /// </summary>
    public class TestResult
    {
        /// <summary>
        /// Идентификатор результата тестирования
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Название теста
        /// </summary>
        public string TestName { get; set; }

        /// <summary>
        /// Описание теста
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Дата и время выполнения теста
        /// </summary>
        public DateTime TestDate { get; set; }

        /// <summary>
        /// Признак успешного прохождения теста
        /// </summary>
        public bool IsPassed { get; set; }

        /// <summary>
        /// Сообщение об ошибке (если тест не пройден)
        /// </summary>
        public string ErrorMessage { get; set; }

        /// <summary>
        /// Идентификатор пользователя, проводившего тест
        /// </summary>
        public string UserId { get; set; }

        /// <summary>
        /// Параметры теста (ключ-значение)
        /// </summary>
        public Dictionary<string, string> Parameters { get; set; } = new Dictionary<string, string>();
    }

    /// <summary>
    /// Проблема, связанная с деталью
    /// </summary>
    public class Issue
    {
        /// <summary>
        /// Идентификатор проблемы
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Заголовок проблемы
        /// </summary>
        public string Title { get; set; }

        /// <summary>
        /// Описание проблемы
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Дата и время обнаружения проблемы
        /// </summary>
        public DateTime ReportDate { get; set; }

        /// <summary>
        /// Идентификатор пользователя, сообщившего о проблеме
        /// </summary>
        public string ReportedByUserId { get; set; }

        /// <summary>
        /// Серьезность проблемы
        /// </summary>
        public IssueSeverity Severity { get; set; }

        /// <summary>
        /// Статус проблемы
        /// </summary>
        public IssueStatus Status { get; set; }

        /// <summary>
        /// Идентификатор пользователя, которому назначена проблема
        /// </summary>
        public string AssignedToUserId { get; set; }

        /// <summary>
        /// Дата и время решения проблемы
        /// </summary>
        public DateTime? ResolvedDate { get; set; }

        /// <summary>
        /// Комментарий к решению проблемы
        /// </summary>
        public string ResolutionComment { get; set; }
    }

    /// <summary>
    /// Серьезность проблемы
    /// </summary>
    public enum IssueSeverity
    {
        /// <summary>
        /// Низкая серьезность
        /// </summary>
        Low,

        /// <summary>
        /// Средняя серьезность
        /// </summary>
        Medium,

        /// <summary>
        /// Высокая серьезность
        /// </summary>
        High,

        /// <summary>
        /// Критическая серьезность
        /// </summary>
        Critical
    }

    /// <summary>
    /// Статус проблемы
    /// </summary>
    public enum IssueStatus
    {
        /// <summary>
        /// Проблема открыта
        /// </summary>
        Open,

        /// <summary>
        /// Проблема в работе
        /// </summary>
        InProgress,

        /// <summary>
        /// Проблема решена
        /// </summary>
        Resolved,

        /// <summary>
        /// Проблема закрыта
        /// </summary>
        Closed,

        /// <summary>
        /// Проблема отклонена
        /// </summary>
        Rejected
    }
} 