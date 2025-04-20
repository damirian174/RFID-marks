using System;
using System.Collections.Generic;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель результата тестирования детали
    /// </summary>
    public class TestResult
    {
        /// <summary>
        /// Уникальный идентификатор результата теста
        /// </summary>
        public int Id { get; set; }
        
        /// <summary>
        /// Идентификатор детали
        /// </summary>
        public int PartId { get; set; }
        
        /// <summary>
        /// Идентификатор сотрудника, проводившего тест
        /// </summary>
        public int EmployeeId { get; set; }
        
        /// <summary>
        /// Идентификатор сессии, в рамках которой проводился тест
        /// </summary>
        public int SessionId { get; set; }
        
        /// <summary>
        /// Наименование теста
        /// </summary>
        public string TestName { get; set; }
        
        /// <summary>
        /// Описание теста
        /// </summary>
        public string Description { get; set; }
        
        /// <summary>
        /// Дата и время проведения теста
        /// </summary>
        public DateTime TestDate { get; set; }
        
        /// <summary>
        /// Флаг, указывающий, пройден ли тест
        /// </summary>
        public bool Passed { get; set; }
        
        /// <summary>
        /// Результаты измерений (в JSON формате)
        /// </summary>
        public string Measurements { get; set; }
        
        /// <summary>
        /// Ожидаемые параметры (в JSON формате)
        /// </summary>
        public string ExpectedParameters { get; set; }
        
        /// <summary>
        /// Фактические параметры (в JSON формате)
        /// </summary>
        public string ActualParameters { get; set; }
        
        /// <summary>
        /// Список параметров теста в виде коллекции
        /// </summary>
        public List<TestParameter> Parameters { get; set; }
        
        /// <summary>
        /// Комментарий к результату теста
        /// </summary>
        public string Comment { get; set; }
        
        /// <summary>
        /// Ошибки, возникшие при тестировании
        /// </summary>
        public string Errors { get; set; }
        
        /// <summary>
        /// Путь к файлу отчета по тесту
        /// </summary>
        public string ReportFilePath { get; set; }
        
        /// <summary>
        /// Категория теста (например, "Электрический", "Механический", "Функциональный")
        /// </summary>
        public string Category { get; set; }
        
        /// <summary>
        /// Уровень критичности теста (Критический, Важный, Информационный)
        /// </summary>
        public string Severity { get; set; }
        
        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public TestResult()
        {
            TestDate = DateTime.Now;
            Parameters = new List<TestParameter>();
        }
        
        /// <summary>
        /// Добавляет параметр к результату теста
        /// </summary>
        /// <param name="parameter">Параметр теста</param>
        public void AddParameter(TestParameter parameter)
        {
            Parameters.Add(parameter);
        }
        
        /// <summary>
        /// Оценивает общий результат теста на основе параметров
        /// </summary>
        public void EvaluateResult()
        {
            bool allPassed = true;
            
            foreach (var parameter in Parameters)
            {
                if (!parameter.WithinTolerance())
                {
                    allPassed = false;
                    break;
                }
            }
            
            Passed = allPassed;
        }
        
        /// <summary>
        /// Форматирует информацию о результате теста для отображения в интерфейсе
        /// </summary>
        public string FormatDisplayInfo()
        {
            string result = Passed ? "Пройден" : "Не пройден";
            return $"{TestName} - {result} ({TestDate:dd.MM.yyyy HH:mm:ss})";
        }
    }
    
    /// <summary>
    /// Модель параметра теста
    /// </summary>
    public class TestParameter
    {
        /// <summary>
        /// Уникальный идентификатор параметра
        /// </summary>
        public int Id { get; set; }
        
        /// <summary>
        /// Идентификатор результата теста
        /// </summary>
        public int TestResultId { get; set; }
        
        /// <summary>
        /// Наименование параметра
        /// </summary>
        public string Name { get; set; }
        
        /// <summary>
        /// Единица измерения
        /// </summary>
        public string Unit { get; set; }
        
        /// <summary>
        /// Ожидаемое значение
        /// </summary>
        public double ExpectedValue { get; set; }
        
        /// <summary>
        /// Фактическое значение
        /// </summary>
        public double ActualValue { get; set; }
        
        /// <summary>
        /// Минимально допустимое значение
        /// </summary>
        public double MinValue { get; set; }
        
        /// <summary>
        /// Максимально допустимое значение
        /// </summary>
        public double MaxValue { get; set; }
        
        /// <summary>
        /// Допустимое отклонение в процентах
        /// </summary>
        public double TolerancePercent { get; set; }
        
        /// <summary>
        /// Проверяет, находится ли фактическое значение в пределах допустимого отклонения
        /// </summary>
        public bool WithinTolerance()
        {
            return ActualValue >= MinValue && ActualValue <= MaxValue;
        }
        
        /// <summary>
        /// Вычисляет отклонение от ожидаемого значения в процентах
        /// </summary>
        public double DeviationPercent()
        {
            if (ExpectedValue == 0)
                return ActualValue == 0 ? 0 : 100;
                
            return Math.Abs((ActualValue - ExpectedValue) / ExpectedValue * 100);
        }
    }
} 