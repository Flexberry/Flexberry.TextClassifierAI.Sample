import logging
import os

import numpy as np

from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from collections import Counter

from app.model.transformers import HogTransformer
from app.utils.file_utils import get_train_dataset, save_model, get_file_data, load_model

# Ширина изображений, используемых в обучении.
IMAGE_WIDTH = 100
# Объём данных для тестирования из общего количества.
TEST_SIZE: float = 0.2


class SignatureClassifier:

    def new_model(self, train_dataset_dir: str = os.path.join(os.curdir, 'signature_dataset')):
        data: dict = get_train_dataset(width=IMAGE_WIDTH, source_dir=train_dataset_dir)

        self.print_train_data_statistic(data)

        x = np.array(data['data'])
        y = np.array(data['label'])

        x_train, x_test, y_train, y_test = train_test_split(
            x, y,
            test_size=TEST_SIZE,
            shuffle=True,
            random_state=5,
        )

        self.print_splitted_data_statistic(y_train, 'train')
        self.print_splitted_data_statistic(y_test, 'test')

        model = Pipeline([
            ('hogify', HogTransformer(
                pixels_per_cell=(12, 12),
                cells_per_block=(2, 2),
                orientations=9,
                block_norm='L2-Hys')
             ),
            ('scalify', StandardScaler()),
            ('classify', SGDClassifier(random_state=42, max_iter=1000, tol=1e-3))
        ])

        model.fit(x_train, y_train)

        self.print_training_results(model, x_test, y_test)

        save_model(model)

    def is_signature(self, signature_file: str, signature_category: str = 'signature'):
        file_data = get_file_data(signature_file, width=IMAGE_WIDTH, height=IMAGE_WIDTH)
        model = load_model()
        prediction = model.predict([file_data])
        return prediction[0] == signature_category

    def print_train_data_statistic(self, data):
        logging.info(f"number of samples: {len(data['data'])}")
        logging.info(f"keys: {list(data.keys())}")
        logging.info(f"description: {data['description']}")
        logging.info(f"image shape: {data['data'][0].shape}")
        logging.info(f"labels: {str(np.unique(data['label']))}")
        logging.info(f"{Counter(data['label'])}")

    def print_splitted_data_statistic(self, y, label):
        unique, counts = np.unique(y, return_counts=True)
        sorted_index = np.argsort(unique)
        unique = unique[sorted_index]
        percent_counts = 100 * counts[sorted_index] / len(y)
        stat = "[  "
        for i in range(len(unique)):
            stat += f"'{unique[i]}': {counts[i]} ({percent_counts[i]:.2f}%)  "
        stat += "]"
        logging.info(f"{label} ({len(y)} images): {stat}")

    def print_training_results(self, model, x_test, y_test):
        prediction = model.predict(x_test)
        accuracy = accuracy_score(y_test, prediction)
        logging.info(f'Accuracy: {accuracy:.3f}')
