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
# Список стоп-слов для классификатора
STOP_WORDS: list = ['english', 'spanish']


class Classifier:
    """
    Класс с моделью для классификации текста по категориям.
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

