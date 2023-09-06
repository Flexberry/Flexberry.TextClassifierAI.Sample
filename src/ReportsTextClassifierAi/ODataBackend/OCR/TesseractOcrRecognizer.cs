namespace IIS.ReportsTextClassifierAi.OCR
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using System.Linq;

    /// <summary>
    /// Класс для конвертации pdf в png и распознавания с помощью Tesseract.
    /// </summary>
    public class TesseractOcrRecognizer
    {
        /// <summary>
        /// Распознает текст в Tesseract.
        /// </summary>
        /// <param name="uploadDirectory">Директория хранения загруженных файлов.</param>
        /// <param name="uploadKey">Идентификатор загрузки.</param>
        /// <param name="fileName">Имя файла.</param>
        /// <returns>Распознанный текст.</returns>
        public string RecognizeUploadedPdf(string uploadDirectory, string uploadKey, string fileName)
        {
            if (!File.Exists(Path.Combine(uploadDirectory, uploadKey, fileName)))
            {
                new DirectoryNotFoundException("Recognition error: File not found");
            }

            string resultText = string.Empty;

            string fileDirectory = Path.Combine(uploadDirectory, uploadKey);
            string fileNameWithoutExt = Path.GetFileNameWithoutExtension(fileName);
            string pngFolder = "png";
            string recognitionFolder = "recognition";

            string pngDirectory = Path.Combine(fileDirectory, pngFolder);
            string recognitionDirectory = Path.Combine(fileDirectory, recognitionFolder);

            try
            {
                CreatePngFilesFromPdf(fileDirectory, pngDirectory, fileNameWithoutExt);
                RecognizePng(pngDirectory, recognitionDirectory);

                resultText = MergeTxt(recognitionDirectory);

                Directory.Delete(Path.GetFullPath(pngDirectory), true);
                Directory.Delete(Path.GetFullPath(recognitionDirectory), true);
            }
            catch (Exception ex)
            {
                throw new Exception("Recognition PDF failure " + ex.Message);
            }

            return resultText;
        }

        /// <summary>
        /// Конвертирует указанный pdf в набор png файлов.
        /// </summary>
        /// <param name="mainDirectory">Директория, где находится изначальный файл.</param>
        /// <param name="pngDirectory">Директория в которую будут складываться png файлы.</param>
        /// <param name="originFileNameWithoutExt">Имя изначального pdf файла, без расширения.</param>
        private void CreatePngFilesFromPdf(string mainDirectory, string pngDirectory, string originFileNameWithoutExt)
        {
            string pdfFile = Path.Combine(mainDirectory, originFileNameWithoutExt + ".pdf");
            string pngFile = Path.Combine(pngDirectory, originFileNameWithoutExt + ".png");

            var convertPdfToPngProcess = new Process()
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/bin/bash",
                    Arguments = $"-c \"mkdir -p {pngDirectory} && convert -density 300 -trim {pdfFile} -quality 100 {pngFile}\"",
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                },
            };

            convertPdfToPngProcess.Start();

            string errors = convertPdfToPngProcess.StandardError.ReadToEnd();

            convertPdfToPngProcess.WaitForExit();

            if (convertPdfToPngProcess.ExitCode != 0)
            {
                throw new Exception(errors);
            }
        }

        /// <summary>
        /// Распознает png файлы и сохраняет результат в txt.
        /// </summary>
        /// <param name="pngDirectory">Директория с png файлами.</param>
        /// <param name="recognitionDirectory">Директория для сохранения распознанных файлов.</param>
        private void RecognizePng(string pngDirectory, string recognitionDirectory)
        {
            // Получаем список конвертированных png файлов.
            List<string> pngFiles = Directory.GetFiles(pngDirectory).ToList();

            foreach (string pngFile in pngFiles)
            {
                string pngFileName = Path.GetFileNameWithoutExtension(pngFile);
                string resultFile = Path.Combine(recognitionDirectory, pngFileName);

                var convertPdfToPngProcess = new Process()
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = "/bin/bash",
                        Arguments = $"-c \"mkdir -p {recognitionDirectory} && tesseract {pngFile} {resultFile} -l rus+eng --psm 1 --oem 3 txt\"",
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        UseShellExecute = false,
                        CreateNoWindow = true,
                    },
                };

                convertPdfToPngProcess.Start();

                string errors = convertPdfToPngProcess.StandardError.ReadToEnd();

                convertPdfToPngProcess.WaitForExit();

                if (convertPdfToPngProcess.ExitCode != 0)
                {
                    throw new Exception(errors);
                }
            }
        }

        /// <summary>
        /// Объединяет текст из распознанных txt файлов, относящихся к одному pdf, в одну строку.
        /// </summary>
        /// <param name="recognitionDirectory">Директория для сохранения распознанных файлов.</param>
        /// <returns>Объединенный распознанный текст.</returns>
        private string MergeTxt(string recognitionDirectory)
        {
            string resultText = string.Empty;

            // Получаем список распознанных файлов.
            List<string> txtFiles = Directory.GetFiles(recognitionDirectory, "*.txt").ToList();
            txtFiles.Sort();

            if (txtFiles.Count == 0)
            {
                throw new Exception("Merge txt error. Recognized files not found");
            }

            foreach (string existingFile in txtFiles)
            {
                resultText += File.ReadAllText(existingFile);
            }

            return resultText;
        }
    }
}