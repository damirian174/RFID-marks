using System;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель компонента, используемого в сборке изделий
    /// </summary>
    public class Component
    {
        /// <summary>
        /// Уникальный идентификатор компонента
        /// </summary>
        public int Id { get; set; }
        
        /// <summary>
        /// Артикул компонента
        /// </summary>
        public string ArticleNumber { get; set; }
        
        /// <summary>
        /// Наименование компонента
        /// </summary>
        public string Name { get; set; }
        
        /// <summary>
        /// Серийный номер компонента
        /// </summary>
        public string SerialNumber { get; set; }
        
        /// <summary>
        /// Номер партии
        /// </summary>
        public string BatchNumber { get; set; }
        
        /// <summary>
        /// Дата создания записи о компоненте
        /// </summary>
        public DateTime CreatedAt { get; set; }
        
        /// <summary>
        /// Категория компонента
        /// </summary>
        public string Category { get; set; }
        
        /// <summary>
        /// Описание компонента
        /// </summary>
        public string Description { get; set; }
        
        /// <summary>
        /// RFID-метка, связанная с компонентом (если есть)
        /// </summary>
        public string RfidTag { get; set; }
        
        /// <summary>
        /// Статус компонента (Доступен, Использован, Брак)
        /// </summary>
        public string Status { get; set; }
        
        /// <summary>
        /// Идентификатор склада/местоположения
        /// </summary>
        public int? LocationId { get; set; }
        
        /// <summary>
        /// Идентификатор поставщика
        /// </summary>
        public int? SupplierId { get; set; }
        
        /// <summary>
        /// Наименование поставщика
        /// </summary>
        public string SupplierName { get; set; }
        
        /// <summary>
        /// Дата поставки
        /// </summary>
        public DateTime? DeliveryDate { get; set; }
        
        /// <summary>
        /// Срок годности (если применимо)
        /// </summary>
        public DateTime? ExpiryDate { get; set; }
        
        /// <summary>
        /// Идентификатор детали, в которую установлен компонент
        /// </summary>
        public int? InstalledInPartId { get; set; }
        
        /// <summary>
        /// Флаг, указывающий, прошел ли компонент проверку качества
        /// </summary>
        public bool QualityChecked { get; set; }
        
        /// <summary>
        /// Комментарий к компоненту
        /// </summary>
        public string Comment { get; set; }
        
        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public Component()
        {
            CreatedAt = DateTime.Now;
            Status = "Доступен";
            QualityChecked = false;
        }
        
        /// <summary>
        /// Устанавливает компонент в деталь
        /// </summary>
        /// <param name="partId">Идентификатор детали</param>
        public void InstallInPart(int partId)
        {
            if (Status == "Использован")
            {
                throw new InvalidOperationException("Компонент уже используется в другой детали");
            }
            
            InstalledInPartId = partId;
            Status = "Использован";
        }
        
        /// <summary>
        /// Помечает компонент как брак
        /// </summary>
        /// <param name="comment">Причина брака</param>
        public void MarkAsDefective(string comment)
        {
            Status = "Брак";
            Comment = comment;
        }
        
        /// <summary>
        /// Проверяет, доступен ли компонент для использования
        /// </summary>
        public bool IsAvailable()
        {
            return Status == "Доступен" && (ExpiryDate == null || ExpiryDate > DateTime.Now);
        }
        
        /// <summary>
        /// Форматирует информацию о компоненте для отображения в интерфейсе
        /// </summary>
        public string FormatDisplayInfo()
        {
            return $"{Name} (SN: {SerialNumber}, Артикул: {ArticleNumber}) - {Status}";
        }
    }
} 