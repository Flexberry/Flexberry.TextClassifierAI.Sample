import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import os

# Функция для определения наличия прозрачности в изображении.
def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False

# Функция для замены фона изображения на белый.
def change_background_of_image_to_white(img_path):
    # Открываем изображение.
    img = Image.open(img_path)

    if not has_transparency(img):
        # Создаем новое изображение с белым фоном.
        white_bg = Image.new('RGBA', img.size, 'WHITE') 

        # Комбинируем изображения.
        white_bg.paste(img, (0,0), img)

        # Сохраняем новое изображение в исходный файл.
        white_bg.save(img_path)

# Функция для обработки изображений в директории
def process_images(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                change_background_of_image_to_white(img_path)
                image_class = classify(model, image_transform, img_path, classes)
                sort_image(img_path, image_class)

# Функция для перемещения изображения в соответствующую папку.
def sort_image(image_path, image_class):
    # Читаем изображение.
    image = Image.open(image_path)
    
    # Определяем папку, в которую нужно переместить изображение на основе некоторого условия.
    destination_folder = classes[image_class]
    
    # Создаем папку, если она не существует.
    os.makedirs(destination_folder, exist_ok=True)
    
    # Перемещаем изображение в папку назначения.
    destination_path = os.path.join(destination_folder, os.path.basename(image_path))
    image.save(destination_path)

# Функция для классификации изображения с помощью модели.
def classify(model, image_transform, image_path, classes):
    model = model.eval()
    image = Image.open(image_path)

    # Проверяем количество каналов.
    if image.mode != 'RGB':
        # Если у изображения нет 3 каналов (RGB), конвертируем его.
        image = image.convert('RGB')

    image = image_transform(image).float()

    image = image.unsqueeze(0)

    output = model(image)
    _, predicted = torch.max(output.data, 1)

    return predicted.item()

if __name__ == '__main__':
    # Список классов.
    classes = [
        "not_signature",
        "signature",
    ]

    # Загрузка модели.
    model = torch.load('model.pth')

    # Путь к директории с изображениями для обработки.
    images_dataset_path = './images'

    # Средние значения и стандартное отклонение для нормализации изображений.
    mean = [0.9738, 0.9738, 0.9738]
    std = [0.1121, 0.1121, 0.1121]

    # Преобразование изображений.
    image_transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Изменяем размер изображений до фиксированного размера.
        transforms.ToTensor(),  # Преобразуем изображения в тензоры.
        transforms.Normalize(torch.Tensor(mean), torch.Tensor(std)),  # Нормализуем изображения.
    ])

    # Обработка изображений.
    process_images(images_dataset_path)
