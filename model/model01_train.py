import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel
import pytorch_lightning as pl

class ChineseSentimentClassifier(pl.LightningModule):
    def __init__(self, model_name_or_path):
        super().__init__()
        self.tokenizer = BertTokenizer.from_pretrained(model_name_or_path)
        self.bert = BertModel.from_pretrained(model_name_or_path)
        self.classifier = nn.Linear(self.bert.config.hidden_size, 3)  # 3 for 3 classes
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        cls_embedding = last_hidden_state[:, 0, :]
        logits = self.classifier(cls_embedding)
        loss = None
        if labels is not None:
            loss = self.criterion(logits, labels)
        return loss, logits

    def training_step(self, batch, batch_idx):
        input_ids, attention_mask, labels = batch
        loss, logits = self(input_ids, attention_mask, labels)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        input_ids, attention_mask, labels = batch
        loss, logits = self(input_ids, attention_mask, labels)
        self.log('val_loss', loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=2e-5)

# 准备数据集
from torch.utils.data import Dataset, DataLoader

class SentimentDataset(Dataset):
    def __init__(self, data, tokenizer, max_length):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text, label = self.data[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )
        return (
            encoding['input_ids'].squeeze(),
            encoding['attention_mask'].squeeze(),
            torch.tensor(label)
        )

# 加载数据集
train_data = []
val_data = []

# 创建数据集和数据加载器
model_name_or_path = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name_or_path)
max_length = 512

train_dataset = SentimentDataset(train_data, tokenizer, max_length)
val_dataset = SentimentDataset(val_data, tokenizer, max_length)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# 初始化模型
model = ChineseSentimentClassifier(model_name_or_path)

# 训练模型
trainer = pl.Trainer(max_epochs=5, gpus=1 if torch.cuda.is_available() else 0)
trainer.fit(model, train_loader, val_loader)


# 训练完成后
trainer.save_checkpoint("sentiment_classifier.ckpt")  # 保存模型权重和参数
