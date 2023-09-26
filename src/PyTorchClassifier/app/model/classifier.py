import torch
import string
from app.model.model import TextClassificationModel
from app.model.dataset import create_dataset
from torch.utils.data.dataset import random_split
from torchtext.data.functional import to_map_style_dataset
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

# Размерность векторов в матрице внедрения.
EM_SIZE = 300
# Количество эпох обучения.
EPOCHS = 20
# Скорость обучения.
LR = 0.004
# Размер батча.
BATCH_SIZE = 64
# Идентификатор устройства расчета.
DEVICE = "cpu"
# Имя файла сохранения обученнйо модели.
MODEL_FILE_NAME: str = "model_checkpoint.pt"
DATASET_FILE_NAME: str = "dataset_checkpoint.pt"

tokenizer = get_tokenizer('spacy', language='ru_core_news_lg')


def yield_tokens(data_iter):
    for _, text in data_iter:
        yield tokenizer(text)


def remove_punctuation(input_string):
    # Make a translation table that maps all punctuation characters to None
    translator = str.maketrans("", "", string.punctuation)

    # Apply the translation table to the input string
    result = input_string.translate(translator)

    return result

class Classifier:
    """
    Класс для классификации текста по категориям.
    """

    def train_model(self, csv, text_column, label_column_name, delimiter):
        """
        Обучение новой модели классификатора.
        :param csv: Csv файл.
        :param text_column: Имя столбца с тектом.
        :param label_column_name: Имя столбца с категорией.
        :param delimiter: Разделитель.
        """
        dataset = create_dataset(csv, text_column, label_column_name, delimiter)

        vocab = build_vocab_from_iterator(yield_tokens(dataset), specials=["<unk>"])
        vocab.set_default_index(vocab["<unk>"])

        text_pipeline = lambda x: vocab(tokenizer(remove_punctuation(x)))
        label_pipeline = lambda x: int(x) - 1

        def collate_batch(batch):
            label_list, text_list, offsets = [], [], [0]
            for label, text in batch:
                label_list.append(label_pipeline(label))
                processed_text = torch.tensor(text_pipeline(text), dtype=torch.int64)
                text_list.append(processed_text)
                offsets.append(processed_text.size(0))

            label_list = torch.tensor(label_list, dtype=torch.int64)
            offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
            text_list = torch.cat(text_list)

            return label_list.to(DEVICE), text_list.to(DEVICE), offsets.to(DEVICE)

        num_class = len(set([label for (label, text) in dataset]))

        dataset_vocab = build_vocab_from_iterator(yield_tokens(dataset), specials=["<unk>"])
        dataset_vocab.set_default_index(dataset_vocab["<unk>"])

        vocab_size = len(dataset_vocab)
        model = TextClassificationModel(vocab_size, EM_SIZE, num_class).to(DEVICE)

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.1)
        total_accu = None

        traint_iter, test_iter = train_test_split(dataset, test_size=0.1, random_state=20)
        train_dataset = to_map_style_dataset(traint_iter)
        test_dataset = to_map_style_dataset(test_iter)
        num_train = int(len(train_dataset) * 0.8)

        split_train_, split_valid_ = random_split(
            train_dataset, [num_train, len(train_dataset) - num_train]
        )
        train_dataloader = DataLoader(
            split_train_, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch
        )
        valid_dataloader = DataLoader(
            split_valid_, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch
        )
        test_dataloader = DataLoader(
            test_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch
        )

        def train(dataloader):
            model.train()

            for idx, (label, text, offsets) in enumerate(dataloader):
                optimizer.zero_grad()
                predicted_label = model(text, offsets)
                loss = criterion(predicted_label, label)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
                optimizer.step()

        def evaluate(dataloader):
            model.eval()
            total_acc, total_count = 0, 0

            with torch.no_grad():
                for idx, (label, text, offsets) in enumerate(dataloader):
                    predicted_label = model(text, offsets)
                    loss = criterion(predicted_label, label)
                    total_acc += (predicted_label.argmax(1) == label).sum().item()
                    total_count += label.size(0)

            return total_acc / total_count

        for epoch in range(1, EPOCHS + 1):
            train(train_dataloader)
            accu_val = evaluate(valid_dataloader)
            if total_accu is not None and total_accu > accu_val:
                scheduler.step()
            else:
                total_accu = accu_val
            print("-" * 59)
            print(
                "| end of epoch {:3d} | valid accuracy {:8.3f} ".format(epoch, accu_val)
            )
            print("-" * 59)

        print("Checking the results of test dataset.")
        accu_test = evaluate(test_dataloader)
        print("test accuracy {:8.3f}".format(accu_test))

        model_scripted = torch.jit.script(model)
        model_scripted.save(MODEL_FILE_NAME)

        torch.save(dataset, DATASET_FILE_NAME)

    def classify_text(self, text):
        """
        Классифицировать текст.
        :param text: текст.
        """
        try:
            with open(MODEL_FILE_NAME, 'rb') as file:
                model = torch.jit.load(file)

            model.eval()

            dataset = torch.load(DATASET_FILE_NAME)

            vocab = build_vocab_from_iterator(yield_tokens(dataset), specials=["<unk>"])
            vocab.set_default_index(vocab["<unk>"])

            text_pipeline = lambda x: vocab(tokenizer(x))

            def predict(text_value):
                with torch.no_grad():
                    text_value = torch.tensor(text_pipeline(text_value))
                    output = model(text_value, torch.tensor([0]))

                    return output.argmax(1).item() + 1

            result = predict(text)

            return result
        except FileNotFoundError as ex:
            raise FileNotFoundError("Classifier model wasn't found!")
