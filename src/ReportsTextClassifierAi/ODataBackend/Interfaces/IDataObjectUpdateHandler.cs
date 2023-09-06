namespace IIS.ReportsTextClassifierAi.Interfaces
{
    using ICSSoft.STORMNET;

    /// <summary>
    /// Интерфейс для обработки событий изменения DataObject.
    /// </summary>
    public interface IDataObjectUpdateHandler
    {
        /// <summary>
        /// Обработчик события обновления или создания объекта.
        /// </summary>
        /// <param name="dataObject">Измененный объект.</param>
        public void CallbackAfterUpdate(DataObject dataObject);
    }
}
