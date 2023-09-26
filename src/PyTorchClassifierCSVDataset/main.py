!pip install torchtext spacy

import torch
from torch.autograd import Variable
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataset import random_split
from torchtext.data.functional import to_map_style_dataset
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
import pandas as pd
import base64
from PIL import Image
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import traceback

# Hyperparameters
EPOCHS = 15  # epoch
LR = 0.002  # learning rate
BATCH_SIZE = 16  # Размер пакета для обучения.
IMAGE_SIZE = 196 # Размер нормализованного изображения в пикселях.
csv_file = "test.csv" # Имя CSV файла с данными

# Устройство для вычислений.
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")

print("The model will be running on", device, "device")

class CustomCSVDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        # Загрузка данных из CSV.
        self.data = pd.read_csv(csv_file, on_bad_lines='skip', delimiter=';')
        # Подгонка изображений под одни размеры.
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        category = row['category']
        coded_string = row['image']
        # Преобразование base64 строки к двоичным данным.
        try:
          imgBytes = base64.b64decode(coded_string)

          # Преобразование двоичных данных в изображение.
          image = Image.open(io.BytesIO(imgBytes))
        except Exception as e:
          print(traceback.format_exc())
          print(idx)
          print(coded_string)

        if self.transform:
            # Преобразование изображений.
            image = self.transform(image)

        return image, int(category)

# Преобразование изображений к одному размеру.
data_transform  = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
])

# Основной набор данных.
custom_dataset = CustomCSVDataset(csv_file, data_transform)
traint_iter, test_iter = train_test_split(custom_dataset, test_size=0.1, random_state=20)
# Тренировочный и тестовый наборы данных.
train_dataset = to_map_style_dataset(traint_iter)
test_dataset = to_map_style_dataset(test_iter)
num_train = int(len(train_dataset) * 0.9)

# Случайное разделение набора данных на обучение и контроль.
split_train_, split_valid_ = random_split(
    train_dataset, [num_train, len(train_dataset) - num_train]
)

train_dataloader = DataLoader(
    split_train_, batch_size=BATCH_SIZE, num_workers=0, shuffle=True
)
valid_dataloader = DataLoader(
    split_valid_, batch_size=BATCH_SIZE, num_workers=0, shuffle=True
)
test_dataloader = DataLoader(
    test_dataset, batch_size=BATCH_SIZE, num_workers=0, shuffle=True
)

# Отрисовка набора данных для контроля.
train_features, train_labels = next(iter(train_dataloader))
print(f"Feature batch shape: {train_features.size()}")
print(f"Labels batch shape: {train_labels.size()}")
indx = 0
# Рисуем таблицу 4 на 4 с 16 изображениями.
f, axarr = plt.subplots(4, 4, figsize=(12, 8))
for r in range(0, 4):
  for c in range(0, 4):
    img = train_features[indx].squeeze()
    label = train_labels[indx]
    axarr[r, c].imshow(transforms.ToPILImage()(img))
    axarr[r, c].set_title(str(label.item()))
    indx+=1

# Определяем нейронную сеть.
class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(12)
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(12)
        self.pool = nn.MaxPool2d(2,2)
        self.conv4 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(24)
        self.conv5 = nn.Conv2d(in_channels=24, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(24)
        self.fc1 = nn.Linear(24*10*10, 10)

    def forward(self, input):
        output = F.relu(self.bn1(self.conv1(input)))      
        output = F.relu(self.bn2(self.conv2(output)))     
        output = self.pool(output)                        
        output = F.relu(self.bn4(self.conv4(output)))     
        output = F.relu(self.bn5(self.conv5(output)))     
        output = output.view(-1, 24*10*10)
        output = self.fc1(output)

        return output

# Модель нейронной сети.
model = Network()

# Define the loss function with Classification Cross-Entropy loss and an optimizer with Adam optimizer
loss_fn = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

# Сохранение модели.
def saveModel():
    path = "learningModel.pth"
    torch.save(model.state_dict(), path)

# Тестирование точности нейронной сети.
def testAccuracy():
    
    model.eval()
    accuracy = 0.0
    total = 0.0
    
    with torch.no_grad():
        for data in test_dataloader:
            images, labels = data
            # Запуск модели нейронной сети для определения категории изображения.
            outputs = model(images)
            # Берем наиболее подходящую категорию, с наибольшим весом.
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            accuracy += (predicted == labels).sum().item()
    
    # Расчитываем точность для всех изображений.
    accuracy = (100 * accuracy / total)
    return(accuracy)

# Функция тренировки нейронной сети.
def train(num_epochs):
    
    best_accuracy = 0.0

    print("The model will be running on", device, "device")
    # Загрузка параметров в процессор.
    model.to(device)

    for epoch in range(num_epochs):  # Цикл по набору данных.
        running_loss = 0.0
        running_acc = 0.0

        for i, (images, labels) in enumerate(train_dataloader, 0):
            
            # Входные параметры.
            images = Variable(images.to(device))
            labels = Variable(labels.to(device))

            # Обнуление градиента параметров.
            optimizer.zero_grad()
            # Прогнозировать классы, используя изображения из обучающего набора.
            outputs = model(images)
            # Вычислить потери на основе результатов модели и реальных меток.
            loss = loss_fn(outputs, labels)
            # Обратное распространение потерь.
            loss.backward()
            # Оптимизировать параметры на основе рассчитанных градиентов.
            optimizer.step()

            # Выведем статистику для каждых 16 изображений.
            running_loss += loss.item()     # Значение потерь.
            if i % 16 == 15:    
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 16))
                # обнулим потери.
                running_loss = 0.0

        # Рассчитаем и выведем среднюю точность этой эпохи при тестировании на всех тестовых изображениях.
        accuracy = testAccuracy()
        print('For epoch', epoch+1,'the test accuracy over the whole test set is %d %%' % (accuracy))
        
        # Сохранить модель, если точность наилучшая.
        if accuracy > best_accuracy:
            saveModel()
            best_accuracy = accuracy

# Функция для тестирования модели.
def testBatch():
    # Пакет изображений из тестового DataLoader.
    images, labels = next(iter(test_dataloader))

    # Вывод изображений.
    imageshow(torchvision.utils.make_grid(images))
   
    # Вывод категорий которы должны быть.
    print('Real labels: ', ' '.join('%5s' % classes[labels[j]] 
                               for j in range(batch_size)))
  
    # Посмотрим как модель идентифицирует метки из этого примера.
    outputs = model(images)
    
    # Мы получили вероятность для всех категорий. Самая высокая (максимальная) вероятность должна быть правильной категории.
    _, predicted = torch.max(outputs, 1)
    
    # Вывод результатов.
    print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] 
                              for j in range(batch_size)))
    

# Построение модели.
train(EPOCHS)
print('Finished Training')

testModelAccuracy()
testBatch()