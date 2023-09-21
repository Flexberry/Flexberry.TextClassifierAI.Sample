import pandas as pd
from torch.utils.data import Dataset

class CustomTextDataset(Dataset):
  def __init__(self, csv_file, text_column_name, label_column_name, delimiter):
    self.data = pd.read_csv(csv_file, on_bad_lines='skip', delimiter=delimiter)
    self.text_column_name = text_column_name
    self.label_column_name = label_column_name
    
  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):
    row = self.data.iloc[idx]
    text = row[self.text_column_name].lower()
    label = row[self.label_column_name]
    
    return label, text
      
def create_dataset(csv_file, text_column, label_column_name, delimiter):
  return CustomTextDataset(csv_file, text_column, label_column_name, delimiter)
