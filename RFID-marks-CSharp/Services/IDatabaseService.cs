using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using RFID_marks_CSharp.Models;

namespace RFID_marks_CSharp.Services
{
    /// <summary>
    /// Интерфейс сервиса для работы с базой данных
    /// </summary>
    public interface IDatabaseService
    {
        #region Подключение

        /// <summary>
        /// Инициализирует подключение к базе данных
        /// </summary>
        /// <returns>True, если подключение успешно установлено</returns>
        Task<bool> InitializeAsync();

        /// <summary>
        /// Проверяет, доступно ли подключение к базе данных
        /// </summary>
        /// <returns>True, если подключение доступно</returns>
        Task<bool> CheckConnectionAsync();

        /// <summary>
        /// Закрывает подключение к базе данных
        /// </summary>
        Task CloseConnectionAsync();

        #endregion

        #region Сотрудники

        /// <summary>
        /// Получает сотрудника по RFID-коду карты
        /// </summary>
        /// <param name="rfidCardCode">RFID-код карты</param>
        /// <returns>Данные сотрудника или null, если сотрудник не найден</returns>
        Task<Employee> GetEmployeeByRfidCardAsync(string rfidCardCode);

        /// <summary>
        /// Получает сотрудника по ID
        /// </summary>
        /// <param name="id">Идентификатор сотрудника</param>
        /// <returns>Данные сотрудника или null, если сотрудник не найден</returns>
        Task<Employee> GetEmployeeByIdAsync(int id);

        /// <summary>
        /// Получает список всех сотрудников
        /// </summary>
        /// <returns>Список сотрудников</returns>
        Task<List<Employee>> GetAllEmployeesAsync();

        /// <summary>
        /// Добавляет нового сотрудника
        /// </summary>
        /// <param name="employee">Данные сотрудника</param>
        /// <returns>Идентификатор добавленного сотрудника</returns>
        Task<int> AddEmployeeAsync(Employee employee);

        /// <summary>
        /// Обновляет данные сотрудника
        /// </summary>
        /// <param name="employee">Обновленные данные сотрудника</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        Task<bool> UpdateEmployeeAsync(Employee employee);

        /// <summary>
        /// Удаляет сотрудника
        /// </summary>
        /// <param name="id">Идентификатор сотрудника</param>
        /// <returns>True, если удаление выполнено успешно</returns>
        Task<bool> DeleteEmployeeAsync(int id);

        #endregion

        #region Сессии

        /// <summary>
        /// Получает сессию по ID
        /// </summary>
        /// <param name="id">Идентификатор сессии</param>
        /// <returns>Данные сессии или null, если сессия не найдена</returns>
        Task<Session> GetSessionByIdAsync(int id);

        /// <summary>
        /// Получает текущую активную сессию для сотрудника
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <returns>Данные активной сессии или null, если активная сессия не найдена</returns>
        Task<Session> GetActiveSessionForEmployeeAsync(int employeeId);

        /// <summary>
        /// Получает все сессии сотрудника
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <returns>Список сессий сотрудника</returns>
        Task<List<Session>> GetSessionsByEmployeeIdAsync(int employeeId);

        /// <summary>
        /// Получает список всех сессий
        /// </summary>
        /// <returns>Список сессий</returns>
        Task<List<Session>> GetAllSessionsAsync();

        /// <summary>
        /// Создает новую сессию
        /// </summary>
        /// <param name="session">Данные сессии</param>
        /// <returns>Идентификатор созданной сессии</returns>
        Task<int> CreateSessionAsync(Session session);

        /// <summary>
        /// Обновляет данные сессии
        /// </summary>
        /// <param name="session">Обновленные данные сессии</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        Task<bool> UpdateSessionAsync(Session session);

        /// <summary>
        /// Закрывает сессию
        /// </summary>
        /// <param name="sessionId">Идентификатор сессии</param>
        /// <param name="endTime">Время завершения сессии</param>
        /// <returns>True, если закрытие выполнено успешно</returns>
        Task<bool> CloseSessionAsync(int sessionId, DateTime endTime);

        #endregion

        #region Детали

        /// <summary>
        /// Получает деталь по ID
        /// </summary>
        /// <param name="id">Идентификатор детали</param>
        /// <returns>Данные детали или null, если деталь не найдена</returns>
        Task<Part> GetPartByIdAsync(int id);

        /// <summary>
        /// Получает деталь по серийному номеру
        /// </summary>
        /// <param name="serialNumber">Серийный номер детали</param>
        /// <returns>Данные детали или null, если деталь не найдена</returns>
        Task<Part> GetPartBySerialNumberAsync(string serialNumber);

        /// <summary>
        /// Получает деталь по RFID-метке
        /// </summary>
        /// <param name="rfidTag">RFID-метка детали</param>
        /// <returns>Данные детали или null, если деталь не найдена</returns>
        Task<Part> GetPartByRfidTagAsync(string rfidTag);

        /// <summary>
        /// Получает список всех деталей
        /// </summary>
        /// <returns>Список деталей</returns>
        Task<List<Part>> GetAllPartsAsync();

        /// <summary>
        /// Получает список деталей по статусу
        /// </summary>
        /// <param name="status">Статус деталей</param>
        /// <returns>Список деталей с указанным статусом</returns>
        Task<List<Part>> GetPartsByStatusAsync(string status);

        /// <summary>
        /// Добавляет новую деталь
        /// </summary>
        /// <param name="part">Данные детали</param>
        /// <returns>Идентификатор добавленной детали</returns>
        Task<int> AddPartAsync(Part part);

        /// <summary>
        /// Обновляет данные детали
        /// </summary>
        /// <param name="part">Обновленные данные детали</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        Task<bool> UpdatePartAsync(Part part);

        /// <summary>
        /// Удаляет деталь
        /// </summary>
        /// <param name="id">Идентификатор детали</param>
        /// <returns>True, если удаление выполнено успешно</returns>
        Task<bool> DeletePartAsync(int id);

        #endregion

        #region Операции

        /// <summary>
        /// Получает операцию по ID
        /// </summary>
        /// <param name="id">Идентификатор операции</param>
        /// <returns>Данные операции или null, если операция не найдена</returns>
        Task<Operation> GetOperationByIdAsync(int id);

        /// <summary>
        /// Получает список операций для детали
        /// </summary>
        /// <param name="partId">Идентификатор детали</param>
        /// <returns>Список операций для детали</returns>
        Task<List<Operation>> GetOperationsByPartIdAsync(int partId);

        /// <summary>
        /// Получает список операций для сессии
        /// </summary>
        /// <param name="sessionId">Идентификатор сессии</param>
        /// <returns>Список операций для сессии</returns>
        Task<List<Operation>> GetOperationsBySessionIdAsync(int sessionId);

        /// <summary>
        /// Получает список операций для сотрудника
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <returns>Список операций сотрудника</returns>
        Task<List<Operation>> GetOperationsByEmployeeIdAsync(int employeeId);

        /// <summary>
        /// Добавляет новую операцию
        /// </summary>
        /// <param name="operation">Данные операции</param>
        /// <returns>Идентификатор добавленной операции</returns>
        Task<int> AddOperationAsync(Operation operation);

        /// <summary>
        /// Обновляет данные операции
        /// </summary>
        /// <param name="operation">Обновленные данные операции</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        Task<bool> UpdateOperationAsync(Operation operation);

        /// <summary>
        /// Завершает операцию
        /// </summary>
        /// <param name="operationId">Идентификатор операции</param>
        /// <param name="endTime">Время завершения операции</param>
        /// <param name="result">Результат операции</param>
        /// <param name="comment">Комментарий к операции</param>
        /// <returns>True, если завершение выполнено успешно</returns>
        Task<bool> CompleteOperationAsync(int operationId, DateTime endTime, string result = "Успешно", string comment = "");

        /// <summary>
        /// Отменяет операцию
        /// </summary>
        /// <param name="operationId">Идентификатор операции</param>
        /// <param name="comment">Комментарий к отмене</param>
        /// <returns>True, если отмена выполнена успешно</returns>
        Task<bool> CancelOperationAsync(int operationId, string comment = "");

        #endregion

        #region Компоненты

        /// <summary>
        /// Получает компонент по ID
        /// </summary>
        /// <param name="id">Идентификатор компонента</param>
        /// <returns>Данные компонента или null, если компонент не найден</returns>
        Task<Component> GetComponentByIdAsync(int id);

        /// <summary>
        /// Получает компонент по серийному номеру
        /// </summary>
        /// <param name="serialNumber">Серийный номер компонента</param>
        /// <returns>Данные компонента или null, если компонент не найден</returns>
        Task<Component> GetComponentBySerialNumberAsync(string serialNumber);

        /// <summary>
        /// Получает список компонентов для детали
        /// </summary>
        /// <param name="partId">Идентификатор детали</param>
        /// <returns>Список компонентов для детали</returns>
        Task<List<Component>> GetComponentsByPartIdAsync(int partId);

        /// <summary>
        /// Получает список всех компонентов
        /// </summary>
        /// <returns>Список компонентов</returns>
        Task<List<Component>> GetAllComponentsAsync();

        /// <summary>
        /// Получает список доступных компонентов определенной категории
        /// </summary>
        /// <param name="category">Категория компонентов</param>
        /// <returns>Список доступных компонентов указанной категории</returns>
        Task<List<Component>> GetAvailableComponentsByCategoryAsync(string category);

        /// <summary>
        /// Добавляет новый компонент
        /// </summary>
        /// <param name="component">Данные компонента</param>
        /// <returns>Идентификатор добавленного компонента</returns>
        Task<int> AddComponentAsync(Component component);

        /// <summary>
        /// Обновляет данные компонента
        /// </summary>
        /// <param name="component">Обновленные данные компонента</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        Task<bool> UpdateComponentAsync(Component component);

        /// <summary>
        /// Устанавливает компонент в деталь
        /// </summary>
        /// <param name="componentId">Идентификатор компонента</param>
        /// <param name="partId">Идентификатор детали</param>
        /// <returns>True, если установка выполнена успешно</returns>
        Task<bool> InstallComponentInPartAsync(int componentId, int partId);

        /// <summary>
        /// Помечает компонент как брак
        /// </summary>
        /// <param name="componentId">Идентификатор компонента</param>
        /// <param name="comment">Причина брака</param>
        /// <returns>True, если операция выполнена успешно</returns>
        Task<bool> MarkComponentAsDefectiveAsync(int componentId, string comment);

        #endregion

        #region Результаты тестирования

        /// <summary>
        /// Получает результат теста по ID
        /// </summary>
        /// <param name="id">Идентификатор результата теста</param>
        /// <returns>Данные результата теста или null, если результат не найден</returns>
        Task<TestResult> GetTestResultByIdAsync(int id);

        /// <summary>
        /// Получает список результатов тестов для детали
        /// </summary>
        /// <param name="partId">Идентификатор детали</param>
        /// <returns>Список результатов тестов для детали</returns>
        Task<List<TestResult>> GetTestResultsByPartIdAsync(int partId);

        /// <summary>
        /// Получает список результатов тестов для сессии
        /// </summary>
        /// <param name="sessionId">Идентификатор сессии</param>
        /// <returns>Список результатов тестов для сессии</returns>
        Task<List<TestResult>> GetTestResultsBySessionIdAsync(int sessionId);

        /// <summary>
        /// Получает список результатов тестов для сотрудника
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <returns>Список результатов тестов сотрудника</returns>
        Task<List<TestResult>> GetTestResultsByEmployeeIdAsync(int employeeId);

        /// <summary>
        /// Добавляет новый результат теста
        /// </summary>
        /// <param name="testResult">Данные результата теста</param>
        /// <returns>Идентификатор добавленного результата теста</returns>
        Task<int> AddTestResultAsync(TestResult testResult);

        /// <summary>
        /// Обновляет данные результата теста
        /// </summary>
        /// <param name="testResult">Обновленные данные результата теста</param>
        /// <returns>True, если обновление выполнено успешно</returns>
        Task<bool> UpdateTestResultAsync(TestResult testResult);

        /// <summary>
        /// Добавляет параметр к результату теста
        /// </summary>
        /// <param name="testParameter">Данные параметра теста</param>
        /// <returns>Идентификатор добавленного параметра</returns>
        Task<int> AddTestParameterAsync(TestParameter testParameter);

        #endregion

        #region История деталей

        /// <summary>
        /// Получает запись истории по ID
        /// </summary>
        /// <param name="id">Идентификатор записи истории</param>
        /// <returns>Данные записи истории или null, если запись не найдена</returns>
        Task<PartHistory> GetHistoryRecordByIdAsync(int id);

        /// <summary>
        /// Получает историю для детали
        /// </summary>
        /// <param name="partId">Идентификатор детали</param>
        /// <returns>Список записей истории для детали</returns>
        Task<List<PartHistory>> GetHistoryByPartIdAsync(int partId);

        /// <summary>
        /// Добавляет новую запись в историю
        /// </summary>
        /// <param name="historyRecord">Данные записи истории</param>
        /// <returns>Идентификатор добавленной записи</returns>
        Task<int> AddHistoryRecordAsync(PartHistory historyRecord);

        #endregion

        #region Отчеты

        /// <summary>
        /// Получает статистику по деталям за период
        /// </summary>
        /// <param name="startDate">Начало периода</param>
        /// <param name="endDate">Конец периода</param>
        /// <returns>Данные статистики</returns>
        Task<Dictionary<string, int>> GetPartsStatisticsByPeriodAsync(DateTime startDate, DateTime endDate);

        /// <summary>
        /// Получает статистику по операциям сотрудника за период
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <param name="startDate">Начало периода</param>
        /// <param name="endDate">Конец периода</param>
        /// <returns>Данные статистики</returns>
        Task<Dictionary<string, int>> GetEmployeeStatisticsByPeriodAsync(int employeeId, DateTime startDate, DateTime endDate);

        /// <summary>
        /// Получает общую продолжительность работы сотрудника за период
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <param name="startDate">Начало периода</param>
        /// <param name="endDate">Конец периода</param>
        /// <returns>Продолжительность работы в минутах</returns>
        Task<double> GetEmployeeWorkDurationAsync(int employeeId, DateTime startDate, DateTime endDate);

        #endregion
    }
} 