using System;
using System.Drawing;
using System.Threading.Tasks;

namespace RFID_marks_CSharp.Services
{
    /// <summary>
    /// Интерфейс сервиса для генерации и чтения QR-кодов
    /// </summary>
    public interface IQrCodeService
    {
        /// <summary>
        /// Генерирует QR-код с указанным содержимым
        /// </summary>
        /// <param name="content">Содержимое QR-кода</param>
        /// <param name="size">Размер изображения в пикселях</param>
        /// <param name="errorCorrectionLevel">Уровень коррекции ошибок (L, M, Q, H)</param>
        /// <returns>Изображение с QR-кодом</returns>
        Bitmap GenerateQrCode(string content, int size = 300, string errorCorrectionLevel = "M");

        /// <summary>
        /// Сохраняет QR-код в файл
        /// </summary>
        /// <param name="content">Содержимое QR-кода</param>
        /// <param name="filePath">Путь к файлу для сохранения</param>
        /// <param name="size">Размер изображения в пикселях</param>
        /// <param name="errorCorrectionLevel">Уровень коррекции ошибок (L, M, Q, H)</param>
        /// <returns>True, если операция выполнена успешно</returns>
        Task<bool> SaveQrCodeToFileAsync(string content, string filePath, int size = 300, string errorCorrectionLevel = "M");

        /// <summary>
        /// Считывает QR-код с изображения
        /// </summary>
        /// <param name="qrCodeImage">Изображение с QR-кодом</param>
        /// <returns>Содержимое QR-кода или null, если QR-код не распознан</returns>
        string DecodeQrCode(Bitmap qrCodeImage);

        /// <summary>
        /// Считывает QR-код из файла
        /// </summary>
        /// <param name="filePath">Путь к файлу с изображением</param>
        /// <returns>Содержимое QR-кода или null, если QR-код не распознан</returns>
        Task<string> DecodeQrCodeFromFileAsync(string filePath);

        /// <summary>
        /// Генерирует QR-код для детали
        /// </summary>
        /// <param name="articleNumber">Артикул детали</param>
        /// <param name="serialNumber">Серийный номер детали</param>
        /// <param name="batchNumber">Номер партии</param>
        /// <param name="additionalInfo">Дополнительная информация</param>
        /// <param name="size">Размер изображения в пикселях</param>
        /// <returns>Изображение с QR-кодом</returns>
        Bitmap GeneratePartQrCode(string articleNumber, string serialNumber, string batchNumber, 
            string additionalInfo = "", int size = 300);

        /// <summary>
        /// Генерирует QR-код для сотрудника
        /// </summary>
        /// <param name="employeeId">Идентификатор сотрудника</param>
        /// <param name="employeeNumber">Табельный номер сотрудника</param>
        /// <param name="fullName">Полное имя сотрудника</param>
        /// <param name="position">Должность сотрудника</param>
        /// <param name="size">Размер изображения в пикселях</param>
        /// <returns>Изображение с QR-кодом</returns>
        Bitmap GenerateEmployeeQrCode(int employeeId, string employeeNumber, string fullName, 
            string position, int size = 300);

        /// <summary>
        /// Добавляет логотип в центр QR-кода
        /// </summary>
        /// <param name="qrCode">Изображение QR-кода</param>
        /// <param name="logoPath">Путь к изображению логотипа</param>
        /// <param name="logoSizePercent">Размер логотипа в процентах от размера QR-кода</param>
        /// <returns>QR-код с логотипом</returns>
        Bitmap AddLogoToQrCode(Bitmap qrCode, string logoPath, int logoSizePercent = 20);

        /// <summary>
        /// Проверяет валидность содержимого QR-кода
        /// </summary>
        /// <param name="content">Содержимое QR-кода</param>
        /// <param name="expectedFormat">Ожидаемый формат (например, "Part", "Employee")</param>
        /// <returns>True, если содержимое соответствует ожидаемому формату</returns>
        bool ValidateQrContent(string content, string expectedFormat);

        /// <summary>
        /// Извлекает информацию из QR-кода детали
        /// </summary>
        /// <param name="qrContent">Содержимое QR-кода</param>
        /// <param name="articleNumber">Артикул детали</param>
        /// <param name="serialNumber">Серийный номер детали</param>
        /// <param name="batchNumber">Номер партии</param>
        /// <param name="additionalInfo">Дополнительная информация</param>
        /// <returns>True, если информация успешно извлечена</returns>
        bool ParsePartQrCode(string qrContent, out string articleNumber, out string serialNumber, 
            out string batchNumber, out string additionalInfo);
    }
} 