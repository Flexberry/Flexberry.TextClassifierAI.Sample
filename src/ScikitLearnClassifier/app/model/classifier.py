import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Объём данных для тестирования из общего количества.
TEST_SIZE: float = 0.2
# Значение для генератора случайных чисел при разделении общего количества данных
# на случайные множества для обучения и тестирования.
RANDOM_STATE: int = 2
# Имя файла модели
MODEL_FILE_NAME: str = "classifier_model.pkl"
# Список стоп-слов для классификатора
STOP_WORDS: list = ['english', 'spanish']


class Classifier:
    """
    Класс с моделью для классифиуации текста по категориям.
    """

    def new_model(self, train: pd.DataFrame, x_field_name: str, y_field_name: str):
        """
        Обучение новой модели классификатора.
        :param train: Данные для обучения и получения оценки точности обучения.
        :param x_field_name: Имя поля в train с влияющим параметром на целевое значение.
        :param y_field_name: Имя поля в train с целевыми значениями.
        """
        train = self.filtered_train(train, [x_field_name, y_field_name])
        y = train[y_field_name]
        x = train[x_field_name]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE)

        model = Pipeline([('vect', CountVectorizer(stop_words=STOP_WORDS)),
                          ('tfidf', TfidfTransformer()),
                          ('scale', StandardScaler(with_mean=False))])

    def filtered_train(self, train: pd.DataFrame, fields: list):
        """
        Фильтрация данных.
        :param train: Данные для фильтрации.
        :param fields: Список полей, к которым применяются правила фильртации.
        :return: Отфильтрованные данные.
        """
        return train.dropna(subset=fields)

    def load_model(self):
        """
        Загрузка ранее обученной модели классификатора из файла с именем MODEL_FILE_NAME.
        :return: Обученная модель классификатора.
        """
        with open(MODEL_FILE_NAME, 'rb') as file:
            model = pickle.load(file)

        return model

    def classified_text(self, text: str):
        """
        Классификация строки текста согласно обученной ранее модели классификатора.
        :param text: Классифицируемый текст
        :return: Категория, к которой относится текст
        """
        try:
            model = self.load_model()
        except FileNotFoundError as ex:
            raise FileNotFoundError("Classifier model wasn't found!")

        return model.predict([text])[0]
