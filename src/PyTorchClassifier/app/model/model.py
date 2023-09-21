from torch import nn


class TextClassificationModel(nn.Module):
  def __init__(self, vocab_size, embed_dim, num_class):
    super(TextClassificationModel, self).__init__()
    self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=False)
    self.fc = nn.Linear(embed_dim, num_class)
    self.act = nn.ReLU
    self.sig = nn.Sigmoid()
    
  def forward(self, text, offsets):
    embedded = self.embedding(text, offsets)
    
    return self.fc(embedded)