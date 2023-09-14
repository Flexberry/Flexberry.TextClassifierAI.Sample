namespace IIS.ReportsTextClassifierAi.Classification
{
    using System;
    using System.Net.Http;
    using System.Text;
    using Newtonsoft.Json.Linq;

    /// <summary>
    /// Инструменты для взаимодействия с сервисом классификации.
    /// </summary>
    public static class ClassificatorTools
    {
        /// <summary>
        /// Отправка запроса к сервису классификации.
        /// </summary>
        /// <param name="classificatorUrl">Адрес сервиса классификации.</param>
        /// <param name="fileName">Имя файла.</param>
        /// <param name="text">Текст из файла для классификации.</param>
        /// <returns>Категория, к которой относится классифиируемый текст.</returns>
        /// <exception cref="HttpRequestException">Ошибка выполнения запроса к сервису классификации.</exception>
        public static string GetTextCategoryRequest(string classificatorUrl, string fileName, string text)
        {
            string requestUrl = "classify";
            string resultField = "text_category";

            JObject jsonBody = new JObject(
                new JProperty("name", fileName),
                new JProperty("text", text));
            string jsonData = jsonBody.ToString();

            using (HttpClient client = new HttpClient())
            {
                Uri baseAddress = new Uri(classificatorUrl);
                HttpContent httpContent = new StringContent(jsonData, Encoding.UTF8, "application/json");

                try
                {
                    using (HttpResponseMessage response = client.PostAsync(new Uri(baseAddress, requestUrl), httpContent).Result)
                    {
                        response.EnsureSuccessStatusCode();
                        string responseBody = response.Content.ReadAsStringAsync().Result;
                        return JObject.Parse(responseBody)[resultField].ToString();
                    }
                }
                catch (Exception ex)
                {
                    throw new HttpRequestException("Post request sended error!\n" + ex.Message);
                }
            }
        }
    }
}