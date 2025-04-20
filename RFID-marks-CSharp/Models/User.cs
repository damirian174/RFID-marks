using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace RFID_marks.Models
{
    /// <summary>
    /// Представляет информацию о пользователе
    /// </summary>
    public class User
    {
        /// <summary>
        /// Уникальный идентификатор пользователя
        /// </summary>
        public string Id { get; set; }

        /// <summary>
        /// Имя пользователя
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Фамилия пользователя
        /// </summary>
        public string Surname { get; set; }

        /// <summary>
        /// Отчество пользователя (если имеется)
        /// </summary>
        public string MiddleName { get; set; }

        /// <summary>
        /// Должность пользователя
        /// </summary>
        public string Position { get; set; }

        /// <summary>
        /// Отдел, в котором работает пользователь
        /// </summary>
        public string Department { get; set; }

        /// <summary>
        /// Уровень доступа пользователя
        /// </summary>
        public AccessLevel AccessLevel { get; set; }

        /// <summary>
        /// Дата и время последнего входа пользователя
        /// </summary>
        public DateTime LastLogin { get; set; }

        /// <summary>
        /// Активные сессии пользователя
        /// </summary>
        public List<Session> ActiveSessions { get; set; } = new List<Session>();

        /// <summary>
        /// Фото пользователя (путь к файлу)
        /// </summary>
        public string PhotoPath { get; set; }

        /// <summary>
        /// Флаг активности пользователя
        /// </summary>
        public bool IsActive { get; set; } = true;

        /// <summary>
        /// Полное имя пользователя (Фамилия И.О.)
        /// </summary>
        public string FullName
        {
            get
            {
                if (string.IsNullOrEmpty(MiddleName))
                {
                    return $"{Surname} {(string.IsNullOrEmpty(Name) ? "" : Name.Substring(0, 1) + ".")}";
                }
                else
                {
                    return $"{Surname} {(string.IsNullOrEmpty(Name) ? "" : Name.Substring(0, 1) + ".")}{(string.IsNullOrEmpty(MiddleName) ? "" : MiddleName.Substring(0, 1) + ".")}";
                }
            }
        }

        /// <summary>
        /// Создает новую сессию для пользователя
        /// </summary>
        /// <returns>Объект сессии</returns>
        public Session CreateSession()
        {
            var session = new Session
            {
                UserId = Id,
                UserName = FullName,
                StartTime = DateTime.Now
            };

            ActiveSessions.Add(session);
            return session;
        }

        /// <summary>
        /// Закрывает активную сессию пользователя
        /// </summary>
        /// <param name="session">Объект сессии</param>
        public void CloseSession(Session session)
        {
            if (session != null && ActiveSessions.Contains(session))
            {
                session.EndTime = DateTime.Now;
                ActiveSessions.Remove(session);
            }
        }

        /// <summary>
        /// Определяет, имеет ли пользователь необходимый уровень доступа
        /// </summary>
        /// <param name="requiredLevel">Требуемый уровень доступа</param>
        /// <returns>true, если пользователь имеет достаточный уровень доступа</returns>
        public bool HasAccess(AccessLevel requiredLevel)
        {
            return AccessLevel >= requiredLevel;
        }
    }

    /// <summary>
    /// Уровни доступа пользователей
    /// </summary>
    public enum AccessLevel
    {
        /// <summary>
        /// Оператор - базовый уровень доступа
        /// </summary>
        Operator = 0,

        /// <summary>
        /// Инженер - средний уровень доступа
        /// </summary>
        Engineer = 1,

        /// <summary>
        /// Администратор - высший уровень доступа
        /// </summary>
        Administrator = 2
    }
} 