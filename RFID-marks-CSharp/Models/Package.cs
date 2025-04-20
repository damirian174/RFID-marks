using System;
using System.Collections.Generic;

namespace RFID_marks_CSharp.Models
{
    /// <summary>
    /// Модель упаковки с изделиями
    /// </summary>
    public class Package
    {
        /// <summary>
        /// Идентификатор упаковки
        /// </summary>
        public int Id { get; set; }

        /// <summary>
        /// Серийный номер упаковки
        /// </summary>
        public string SerialNumber { get; set; }

        /// <summary>
        /// Тип упаковки
        /// </summary>
        public string Type { get; set; }

        /// <summary>
        /// Размер упаковки
        /// </summary>
        public string Size { get; set; }

        /// <summary>
        /// Вес упаковки (кг)
        /// </summary>
        public double Weight { get; set; }

        /// <summary>
        /// Метка RFID упаковки
        /// </summary>
        public string RfidMark { get; set; }

        /// <summary>
        /// Статус упаковки (Создана, Заполняется, Закрыта, Отправлена)
        /// </summary>
        public string Status { get; set; }

        /// <summary>
        /// Идентификатор сотрудника, создавшего упаковку
        /// </summary>
        public int EmployeeId { get; set; }

        /// <summary>
        /// Время создания упаковки
        /// </summary>
        public DateTime CreationTime { get; set; }

        /// <summary>
        /// Время последнего обновления упаковки
        /// </summary>
        public DateTime LastUpdateTime { get; set; }

        /// <summary>
        /// Время отправки упаковки
        /// </summary>
        public DateTime? ShippingTime { get; set; }

        /// <summary>
        /// Адрес отправки
        /// </summary>
        public string ShippingAddress { get; set; }

        /// <summary>
        /// Номер заказа
        /// </summary>
        public string OrderNumber { get; set; }

        /// <summary>
        /// Клиент
        /// </summary>
        public string Customer { get; set; }

        /// <summary>
        /// Список идентификаторов изделий в упаковке
        /// </summary>
        public List<int> PartIds { get; set; }

        /// <summary>
        /// Примечания
        /// </summary>
        public string Notes { get; set; }

        /// <summary>
        /// Конструктор по умолчанию
        /// </summary>
        public Package()
        {
            CreationTime = DateTime.Now;
            LastUpdateTime = DateTime.Now;
            Status = "Создана";
            PartIds = new List<int>();
        }
    }
} 