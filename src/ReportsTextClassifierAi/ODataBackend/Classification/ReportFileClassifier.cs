namespace IIS.ReportsTextClassifierAi.Classification
{
    using System;
    using System.Configuration;
    using System.Linq;
    using System.Net.Http;
    using System.Text.RegularExpressions;
    using ICSSoft.STORMNET;
    using ICSSoft.STORMNET.Business;
    using ICSSoft.STORMNET.Business.LINQProvider;
    using IIS.ReportsTextClassifierAi.Interfaces;
    using IIS.ReportsTextClassifierAi.OCR;
    using Microsoft.Extensions.Configuration;

    /// <summary>
    /// Отвечает за классификацию загруженных pdf файлов отчетов.
    /// </summary>
    public class ReportFileClassifier : IDataObjectUpdateHandler
    {
        private readonly IConfiguration config;

        /// <summary>
        /// Конструктор класса.
        /// </summary>
        /// <param name="config">Настройки.</param>
        public ReportFileClassifier(IConfiguration config)
        {
            this.config = config;
        }

        /// <summary>
        /// Обработчик события обновления или создания объекта.
        /// Запускает распознавание загруженного pdf и отправку текста в классификатор.
        /// </summary>
        /// <param name="dataObject">Измененный объект.</param>
        public void CallbackAfterUpdate(DataObject dataObject)
        {
            if (dataObject == null)
            {
                throw new ArgumentNullException(nameof(dataObject));
            }

            if (dataObject.GetType() == typeof(Report))
            {
                Report report = (Report)dataObject;

                string url = report.reportFile.Url;

                Regex regex = new Regex("fileUploadKey=(.*?)&", RegexOptions.None, TimeSpan.FromMilliseconds(1000));
                GroupCollection regexMatch = regex.Match(url).Groups;

                if (regexMatch != null && regexMatch.Count > 1)
                {
                    string uploadKey = regex.Match(url).Groups[1].ToString();
                    string uploadDirectory = config["UploadUrl"];

                    if (string.IsNullOrEmpty(uploadDirectory))
                    {
                        throw new ConfigurationErrorsException("UploadUrl is not specified in Configuration or enviromnent variables.");
                    }

                    string fileName = report.reportFile.Name;

                    string reсognizedText = RecognizeFile(uploadDirectory, uploadKey, fileName);

                    string category = GetTextCategory(fileName, reсognizedText);
                    Console.WriteLine($"Text: {reсognizedText}");
                    Console.WriteLine($"Category: {category}");

                    InitReportType(report, category);
                }
            }
        }

        private static void InitReportType(Report report, string category)
        {
            if (report.ReportType == null)
            {
                var dataService = DataServiceProvider.DataService;
                var reportType = dataService.Query<ReportType>()
                    .Where(rt => rt.TypeId == category)
                    .FirstOrDefault();

                reportType ??= dataService.Query<ReportType>()
                    .Where(rt => rt.Name == category)
                    .FirstOrDefault();

                if (reportType != null)
                {
                    report.ReportType = reportType;

                    dataService.UpdateObject(report);
                }
                else
                {
                    Console.WriteLine($"Error: no ReportType for Report({report.__PrimaryKey})");
                }
            }
        }

        /// <summary>
        /// Распознает текст с помощью класса работы с Tesseract.
        /// </summary>
        /// <param name="uploadDirectory">Директория хранения загруженных файлов.</param>
        /// <param name="uploadKey">Идентификатор загрузки.</param>
        /// <param name="fileName">Имя файла.</param>
        /// <returns>Распознанный текст.</returns>
        private static string RecognizeFile(string uploadDirectory, string uploadKey, string fileName)
        {
            string resultText = string.Empty;
            TesseractOcrRecognizer recognizer = new TesseractOcrRecognizer();

            try
            {
                resultText = recognizer.RecognizeUploadedPdf(uploadDirectory, uploadKey, fileName);
            }
            catch (Exception ex)
            {
                string errorMessage = "Recognition fail " + ex.Message;
                LogService.LogError(errorMessage);
            }

            return resultText;
        }

        /// <summary>
        /// Получение категории, к которой относится классифицируемый текст.
        /// </summary>
        /// <param name="fileName">Имя файла.</param>
        /// <param name="text">Текст из файла для классификации.</param>
        /// <returns>Категория классифицируемого текста.</returns>
        /// <exception cref="ConfigurationErrorsException">Ошибка, если не задан адрес сервиса классификации (ClassifiercUrl).</exception>
        /// <exception cref="HttpRequestException">Ошибка в случае неудачного запроса к сервису классификации.</exception>
        private string GetTextCategory(string fileName, string text)
        {
            string classifierUrl = config["ClassifierUrl"];
            if (string.IsNullOrEmpty(classifierUrl))
            {
                throw new ConfigurationErrorsException("ClassifierUrl is not specified in Configuration or enviromnent variables.");
            }

            try
            {
                return ClassifierHttpService.GetTextCategoryFromClassifier(classifierUrl, fileName, text);
            }
            catch (Exception ex)
            {
                throw new HttpRequestException("Text category getting error!\n" + ex.Message);
            }
        }
    }
}