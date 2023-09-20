import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Объём данных для тестирования из общего количества.
TEST_SIZE: float = 0.1
# Имя файла модели
MODEL_FILE_NAME: str = "classifier_model.pkl"
# Список стоп-слов для классификатора
STOP_WORDS: list = ["на", "в", "из", "под"]


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
        train[y_field_name] = train[y_field_name].map(str)
        x_train, x_test, y_train, y_test = self.train_test_categories_split(train, x_field_name, y_field_name)

        model = Pipeline([('vect', CountVectorizer(stop_words=STOP_WORDS)),
                          ('tfidf', TfidfTransformer()),
                          ('scale', StandardScaler(with_mean=False)),
                          ('clf', LogisticRegression(class_weight='balanced', C=1e4))])
        model.fit(x_train, y_train)

        prediction = model.predict(x_test)
        accuracy = accuracy_score(y_test, prediction)
        print(f'Accuracy: {accuracy:.3f}')

        self.save_model(model)

    def filtered_train(self, train: pd.DataFrame, fields: list):
        """
        Фильтрация данных.
        :param train: Данные для фильтрации.
        :param fields: Список полей, к которым применяются правила фильртации.
        :return: Отфильтрованные данные.
        """
        return train.dropna(subset=fields)

    def train_test_categories_split(self, dataset: pd.DataFrame, x_field_name: str, y_field_name: str):
        y_unique: np.ndarray = dataset[y_field_name].unique()

        test_data = pd.DataFrame(columns=dataset.columns)
        train_data = pd.DataFrame(columns=dataset.columns)

        for category in y_unique:
            category_count: int = dataset[y_field_name].value_counts()[category]
            test_count: int = round(category_count * TEST_SIZE)
            category_dataset: pd.DataFrame = dataset[dataset[y_field_name] == category]
            for i in range(test_count):
                rnd_range: int = test_count - i
                drop_index = category_dataset.index[np.random.randint(rnd_range)]

                test_data = pd.concat([test_data, pd.DataFrame(category_dataset.loc[drop_index]).T], ignore_index=True)
                category_dataset = category_dataset.drop(index=drop_index)

            train_data = pd.concat([train_data, category_dataset], ignore_index=True)

        x_train = train_data[x_field_name]
        x_test = test_data[x_field_name]
        y_train = train_data[y_field_name]
        y_test = test_data[y_field_name]

        print("Dataset (train / test / percent):")
        for category in y_unique:
            train_count = len(y_train[y_train == category])
            test_count = len(y_test[y_test == category])
            print(f"{category}: {train_count} / {test_count} / {test_count / (train_count + test_count) * 100:.1f}%")

        return x_train, x_test, y_train, y_test

    def save_model(self, model):
        """
        Сохранение обученной модели классификатора в файл с именем MODEL_FILE_NAME.
        :param model: Обученная модель классификатора.
        """
        with open(MODEL_FILE_NAME, 'wb') as file:
            pickle.dump(model, file)

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
