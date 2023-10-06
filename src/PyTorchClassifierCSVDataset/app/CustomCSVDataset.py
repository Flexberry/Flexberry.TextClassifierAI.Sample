import base64
from PIL import Image
import io
import pandas as pd
from torch.utils.data import Dataset, DataLoader

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