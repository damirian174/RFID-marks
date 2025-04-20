using System;
using System.Collections.Generic;

namespace RFID_marks.Models
{
    /// <summary>
    /// Модель записи о тестировании детали
    /// </summary>
    public class TestRecord
    {
        /// <summary>
        /// Идентификатор записи тестирования
        /// </summary>
        public int Id { get; set; }
        
        /// <summary>
        /// Идентификатор детали, которая тестировалась
        /// </summary>
        public int DetailId { get; set; }
        
        /// <summary>
        /// Деталь, которая тестировалась
        /// </summary>
        public Detail Detail { get; set; }
        
        /// <summary>
        /// Идентификатор пользователя, проводившего тестирование
        /// </summary>
        public int? UserId { get; set; }
        
        /// <summary>
        /// Пользователь, проводивший тестирование
        /// </summary>
        public User User { get; set; }
        
        /// <summary>
        /// Тип проведенного теста
        /// </summary>
        public string TestType { get; set; }
        
        /// <summary>
        /// Дата и время проведения теста
        /// </summary>
        public DateTime TestDate { get; set; }
        
        /// <summary>
        /// Длительность теста в секундах
        /// </summary>
        public int DurationSeconds { get; set; }
        
        /// <summary>
        /// Параметры теста в формате JSON
        /// </summary>
        public string Parameters { get; set; }
        
        /// <summary>
        /// Требования для успешного прохождения теста в формате JSON
        /// </summary>
        public string Requirements { get; set; }
        
        /// <summary>
        /// Результаты теста в формате JSON
        /// </summary>
        public string Results { get; set; }
        
        /// <summary>
        /// Признак успешного прохождения теста
        /// </summary>
        public bool Passed { get; set; }
        
        /// <summary>
        /// Комментарий к результатам тестирования
        /// </summary>
        public string Comments { get; set; }
        
        /// <summary>
        /// Конструктор
        /// </summary>
        public TestRecord()
        {
            TestDate = DateTime.Now;
            Passed = false;
        }
    }
    
    /// <summary>
    /// Тип тестирования RFID-метки
    /// </summary>
    public enum TestType
    {
        /// <summary>
        /// Проверка на читаемость метки
        /// </summary>
        ReadabilityTest,
        
        /// <summary>
        /// Тест на запись данных
        /// </summary>
        WriteTest,
        
        /// <summary>
        /// Тест на чтение данных
        /// </summary>
        ReadTest,
        
        /// <summary>
        /// Тест на множественные операции чтения/записи
        /// </summary>
        MultipleOperationsTest,
        
        /// <summary>
        /// Стресс-тест (тестирование в экстремальных условиях)
        /// </summary>
        StressTest,
        
        /// <summary>
        /// Тест на расстояние считывания
        /// </summary>
        RangeTest,
        
        /// <summary>
        /// Другой тип теста
        /// </summary>
        Other
    }
} 