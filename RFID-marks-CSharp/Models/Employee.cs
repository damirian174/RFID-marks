using System;
using System.Collections.Generic;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель сотрудника, работающего с системой
    /// </summary>
    public class Employee
    {
        /// <summary>
        /// Уникальный идентификатор сотрудника
        /// </summary>
        public int Id { get; set; }
        
        /// <summary>
        /// Код RFID-карты сотрудника
        /// </summary>
        public string RfidCardCode { get; set; }
        
        /// <summary>
        /// Табельный номер сотрудника
        /// </summary>
        public string EmployeeNumber { get; set; }
        
        /// <summary>
        /// Фамилия сотрудника
        /// </summary>
        public string LastName { get; set; }
        
        /// <summary>
        /// Имя сотрудника
        /// </summary>
        public string FirstName { get; set; }
        
        /// <summary>
        /// Отчество сотрудника
        /// </summary>
        public string MiddleName { get; set; }
        
        /// <summary>
        /// Полное имя сотрудника
        /// </summary>
        public string FullName => $"{LastName} {FirstName} {MiddleName}".Trim();
        
        /// <summary>
        /// Должность сотрудника
        /// </summary>
        public string Position { get; set; }
        
        /// <summary>
        /// Отдел сотрудника
        /// </summary>
        public string Department { get; set; }
        
        /// <summary>
        /// Электронная почта сотрудника
        /// </summary>
        public string Email { get; set; }
        
        /// <summary>
        /// Телефон сотрудника
        /// </summary>
        public string Phone { get; set; }
        
        /// <summary>
        /// Дата приема на работу
        /// </summary>
        public DateTime HireDate { get; set; }
        
        /// <summary>
        /// Дата увольнения (если уволен)
        /// </summary>
        public DateTime? TerminationDate { get; set; }
        
        /// <summary>
        /// Статус сотрудника (Активен, Неактивен, Уволен)
        /// </summary>
        public string Status { get; set; }
        
        /// <summary>
        /// Роль сотрудника в системе (Администратор, Оператор, Технолог, Контролер)
        /// </summary>
        public string Role { get; set; }
        
        /// <summary>
        /// Логин для входа в систему (для администраторов)
        /// </summary>
        public string Username { get; set; }
        
        /// <summary>
        /// Хеш пароля для входа в систему (для администраторов)
        /// </summary>
        public string PasswordHash { get; set; }
        
        /// <summary>
        /// Дата последнего входа в систему
        /// </summary>
        public DateTime? LastLoginDate { get; set; }
        
        /// <summary>
        /// Фотография сотрудника (путь к файлу)
        /// </summary>
        public string PhotoPath { get; set; }
        
        /// <summary>
        /// Список сессий сотрудника
        /// </summary>
        public List<Session> Sessions { get; set; }
        
        /// <summary>
        /// Список операций, выполненных сотрудником
        /// </summary>
        public List<Operation> Operations { get; set; }
        
        /// <summary>
        /// Список тестов, проведенных сотрудником
        /// </summary>
        public List<TestResult> TestResults { get; set; }
        
        /// <summary>
        /// Комментарий к сотруднику
        /// </summary>
        public string Comment { get; set; }
        
        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public Employee()
        {
            Status = "Активен";
            HireDate = DateTime.Now;
            Sessions = new List<Session>();
            Operations = new List<Operation>();
            TestResults = new List<TestResult>();
        }
        
        /// <summary>
        /// Проверяет, имеет ли сотрудник административные права
        /// </summary>
        public bool IsAdmin()
        {
            return Role == "Администратор";
        }
        
        /// <summary>
        /// Проверяет, активен ли сотрудник
        /// </summary>
        public bool IsActive()
        {
            return Status == "Активен" && (TerminationDate == null || TerminationDate > DateTime.Now);
        }
        
        /// <summary>
        /// Создает новую сессию для сотрудника
        /// </summary>
        /// <returns>Созданная сессия</returns>
        public Session CreateSession()
        {
            if (!IsActive())
            {
                throw new InvalidOperationException("Невозможно создать сессию для неактивного сотрудника");
            }
            
            var session = new Session
            {
                EmployeeId = Id,
                EmployeeName = FullName,
                StartTime = DateTime.Now
            };
            
            Sessions.Add(session);
            LastLoginDate = DateTime.Now;
            
            return session;
        }
        
        /// <summary>
        /// Форматирует информацию о сотруднике для отображения в интерфейсе
        /// </summary>
        public string FormatDisplayInfo()
        {
            return $"{FullName} ({EmployeeNumber}, {Position}) - {Department}";
        }
    }
} 