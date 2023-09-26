import logging
import os
import joblib

import numpy as np

from skimage.transform import resize
from PIL import Image, ImageOps

# Составляющая имени файла набора данных для обучения.
DATASET_FILE_NAME: str = 'signatures'
# Подкаталоги с изображениями подписей и не подписей для обучения, расположены внутри DATASET_DEFAULT_SRC_DIR.
DATASET_DEFAULT_DIR: list = ['signature', 'not_signature']
# Каталог с набором изображений для обучения.
DATASET_DEFAULT_SRC_DIR: str = 'signature_dataset'

# Имя файла модели.
MODEL_FILE_NAME: str = 'signature_classifier_model.pkl'
# Имя распознаваемого файла.
TEMPORARY_FILE_NAME: str = 'temporary_signature.png'


def get_train_dataset(source_dir: str = DATASET_DEFAULT_SRC_DIR,
                      include: str = None,
                      width: int = 100,
                      height: int = None) -> dict:
    if include is None:
        include = DATASET_DEFAULT_DIR

    height = height if height is not None else width

    data = dict()
    data['description'] = 'resized ({0}x{1}) signature in grayscale'.format(int(width), int(height))
    data['label'] = []
    data['filename'] = []
    data['data'] = []

    pkl_file_name = f"{DATASET_FILE_NAME}_{width}x{height}px.pkl"

    for subdir in os.listdir(source_dir):
        if subdir in include:
            current_path = os.path.join(source_dir, subdir)
            logging.info(f"Getting dataset from directory: '{current_path}'")

            for file in os.listdir(current_path):
                if file[-3:] in {'jpg', 'png'}:
                    data['label'].append(subdir)
                    data['filename'].append(file)
                    data['data'].append(get_file_data(os.path.join(current_path, file), width, height))

    joblib.dump(data, pkl_file_name)

    return data


def save_model(model, model_file: str = MODEL_FILE_NAME):
    """
    Сохранение обученной модели классификатора в файл с именем MODEL_FILE_NAME.
    :param model: Обученная модель классификатора.
    :param model_file: Имя файла с сохраненной моделью обучения.
    """
    joblib.dump(model, model_file)


def load_model(model_file: str = MODEL_FILE_NAME):
    return joblib.load(model_file)


def save_signature_file(file_bytes: bytes):
    with open(TEMPORARY_FILE_NAME, 'wb') as f:
        f.write(file_bytes)
    return TEMPORARY_FILE_NAME


def get_file_data(file_name: str, width: int, height: int) -> np.array:
    bit_image = None

    image = Image.open(file_name)

    if image.mode == "LA":
        bit_image = image.convert("RGBA")
        background = Image.new('RGBA', bit_image.size, (255, 255, 255))
        bit_image = ImageOps.invert(Image.alpha_composite(background, bit_image).convert("1"))

    if image.mode == "RGB":
        bit_image = ImageOps.invert(Image.open(file_name).convert("1"))

    if bit_image is None:
        raise BaseException("Signature format error! Only supported RGB and grayscale with transparency formats.")

    return resize(np.array(bit_image, dtype=int), (width, height))
