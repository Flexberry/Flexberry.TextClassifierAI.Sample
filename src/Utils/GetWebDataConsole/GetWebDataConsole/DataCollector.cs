using HtmlAgilityPack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Web;

namespace GetWebDataConsole
{
    internal class DataCollector
    {
        private const string baseUrl = "https://nauchforum.ru";
        private const string archiveUrl = "/archive/article";
        private const string baseUrlMask = "\\/archive\\/article";
        private const string articleMask = "\\/studconf\\/\\w+\\/\\d+\\/\\d+";
        private Dictionary<int, string> articles = new() {
            { 458, "Безопасность жизнедеятельности" },
            { 232, "Педагогика" },
            { 272, "Физико-математические науки" },
            { 181, "Биология" },
            { 399, "Политология" },
            { 330, "Филология" },
            { 314, "Искусствоведение" },
            { 239, "Психология" },
            { 406, "Философия" },
            { 384, "История и археология" },
            { 416, "Сельскохозяйственные науки" },
            { 214, "Химия" },
            { 322, "Культурология" },
            { 392, "Социология" },
            { 349, "Экономика" },
            { 126, "Медицина и фармацевтика" },
            { 250, "Технические науки" },
            { 368, "Юриспруденция" },
            { 421, "Науки о Земле" },
        };
        private const string folderName = "result";
        private const string endListMask = "Список литературы:";
        private const string contentStartClass = "body-content";
        private const string csvSpliter = ";";

        private static void LogMessage(string message)
        {
            Console.WriteLine(message);
        }

        private static void SaveString(string fileName, string content)
        {
            var sw = new StreamWriter(fileName, false, Encoding.UTF8);

            sw.Write(content);
            sw.Close();
        }

        public void CollectData()
        {
            LogMessage("CollectData Start!");

            var dInfo = new DirectoryInfo(folderName);

            if (!dInfo.Exists) dInfo.Create();

            foreach (var article in articles)
            {
                var artDirName = Path.Combine(dInfo.FullName, article.Value);
                var artDir = new DirectoryInfo(artDirName);

                if (!artDir.Exists) artDir.Create();

                LogMessage($"Proccess article: name = {article.Value}");

                ProccessPage(article.Key.ToString(), artDir);
            }

            LogMessage("CollectData Stop!");
        }

        public void ProccessData()
        {
            LogMessage("ProccessData Start!");

            var dInfo = new DirectoryInfo(folderName);

            foreach (DirectoryInfo folder in dInfo.GetDirectories())
            {
                foreach (DirectoryInfo articleFolder in folder.GetDirectories())
                {
                    var fileName = Path.Combine(articleFolder.FullName, "content.html");

                    if (File.Exists(fileName))
                    {
                        LogMessage($"Proccess file: {fileName}");

                        var sr = new StreamReader(fileName, Encoding.UTF8);
                        var stringContent = sr.ReadToEnd();

                        sr.Close();

                        HtmlDocument htmlSnippet = new HtmlDocument();
                        htmlSnippet.LoadHtml(stringContent);

                        var divNode = htmlSnippet.DocumentNode
                            .SelectNodes("//div")
                            .Where(p => p.HasClass(contentStartClass))
                            .FirstOrDefault();

                        if (divNode != null)
                        {
                            var htmlText = divNode.InnerText.Trim();
                            var text = HttpUtility.HtmlDecode(htmlText);
                            var endIndex = text.IndexOf(endListMask);

                            if (endIndex > 0)
                            {
                                text = text.Substring(0, endIndex);
                            }

                            SaveString(Path.Combine(articleFolder.FullName, "content.txt"), text);
                        } 
                        else
                        {
                            LogMessage($"Start substring not found in file: {fileName}");
                        }
                    }
                }
            }

            LogMessage("ProccessData Stop!");
        }

        public void MergeData()
        {
            LogMessage("MergeData Start!");

            var dInfo = new DirectoryInfo(folderName);
            var mergedFileName = Path.Combine(dInfo.FullName, "merged.csv");
            //var sw = new StreamWriter(mergedFileName, false, Encoding.UTF8);
            //var sw = new StreamWriter(mergedFileName, false, new UTF8Encoding(encoderShouldEmitUTF8Identifier: false));
            var sw = new StreamWriter(mergedFileName, false, Encoding.GetEncoding(1251));

            sw.WriteLine($"\"category\"{csvSpliter}\"text\"");

            foreach (DirectoryInfo folder in dInfo.GetDirectories())
            {
                foreach (DirectoryInfo articleFolder in folder.GetDirectories())
                {
                    var fileName = Path.Combine(articleFolder.FullName, "content.txt");

                    if (File.Exists(fileName))
                    {
                        LogMessage($"Proccess file: {fileName}");

                        var sr = new StreamReader(fileName, Encoding.UTF8);
                        var stringContent = sr.ReadToEnd();

                        sr.Close();

                        stringContent = stringContent.Replace("\n", " ").Replace("\r", " ").Replace("\t", " ").Replace("  ", " ").Trim();

                        sw.WriteLine($"\"{folder.Name}\"{csvSpliter}\"{stringContent}\"");
                    }
                }
            }

            sw.Close();

            LogMessage("MergeData Stop!");
        }

        private void ProccessPage(string key, DirectoryInfo artDir, bool first = true)
        {
            LogMessage($"ProccessPage: key = {key}.");

            var articleListHtml = GetHtmlString($"{baseUrl}{archiveUrl}/{key}");
            var regex = new Regex(articleMask);
            var regexMatches = regex.Matches(articleListHtml);

            foreach (Match match in regexMatches)
            {
                var articleUrl = match.Value;
                var folderId = articleUrl.Substring(articleUrl.LastIndexOf("/") + 1);
                var folderName = Path.Combine(artDir.FullName, folderId);
                var dInfo = new DirectoryInfo(folderName);
                var contentFileName = Path.Combine(dInfo.FullName, "content.html");

                if (File.Exists(contentFileName))
                {
                    LogMessage($"(!) Файл {contentFileName} уже существует");
                    continue;
                }

                var articleFullUrl = baseUrl + articleUrl;
                var articleHtml = GetHtmlString(articleFullUrl);

                if (!dInfo.Exists) dInfo.Create();

                SaveString(Path.Combine(dInfo.FullName, "content.url"), articleFullUrl);
                SaveString(contentFileName, articleHtml);
            }

            if (first)
            {
                var regexMask = $"{baseUrlMask}\\/{key}\\?page=\\d+";
                var pagesRegex = new Regex(regexMask);
                var pagesMatches = pagesRegex.Matches(articleListHtml);
                var pagesMax = 0;

                foreach (Match pageMatch in pagesMatches)
                {
                    var pageNumber = int.Parse(pageMatch.Value.Substring(pageMatch.Value.IndexOf("=") + 1));
                    pagesMax = Math.Max(pagesMax, pageNumber);
                }

                if (pagesMax > 0)
                {
                    for (int i = 1; i <= pagesMax; i++)
                    {
                        ProccessPage($"{key}?page={i}", artDir, false);
                    }
                }
            }
        }

        private string GetHtmlString(string url)
        {
            LogMessage($"GetHtmlString: url = {url}.");

            var httpClient = new HttpClient() { BaseAddress = new Uri(url) };
            var getTask = httpClient.GetAsync("");

            getTask.Wait();

            HttpResponseMessage response = getTask.Result;
            var readTask = response.Content.ReadAsStringAsync();

            readTask.Wait();

            LogMessage($"GetHtmlString result length = {readTask.Result.Length}");

            return readTask.Result;
        }
    }
}
