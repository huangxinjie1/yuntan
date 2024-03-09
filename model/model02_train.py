import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler
from transformers import BertForTokenClassification, BertTokenizer
from sklearn.metrics import f1_score

# 加载预训练BERT模型和tokenizer
model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 定义标签列表
label_list = []

# 数据预处理函数
def encode_data(text, labels):
    encoded = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        return_tensors='pt',
        padding='max_length',
        truncation=True,
        max_length=512
    )

    input_ids = encoded['input_ids']
    attention_mask = encoded['attention_mask']

    encoded_labels = []
    for label in labels:
        encoded_labels.append(label_list.index(label) if label != 'X' else -100)
    encoded_labels = torch.tensor(encoded_labels)

    return input_ids, attention_mask, encoded_labels

# 准备训练数据
train_texts = []
train_labels = []

train_encodings = [encode_data(text, labels) for text, labels in zip(train_texts, train_labels)]
train_dataset = TensorDataset([
    torch.cat([encoding[0] for encoding in train_encodings]),
    torch.cat([encoding[1] for encoding in train_encodings]),
    torch.cat([encoding[2] for encoding in train_encodings])
])

# 准备测试数据
test_texts = []
test_labels = []

test_encodings = [encode_data(text, labels) for text, labels in zip(test_texts, test_labels)]
test_dataset = TensorDataset([
    torch.cat([encoding[0] for encoding in test_encodings]),
    torch.cat([encoding[1] for encoding in test_encodings]),
    torch.cat([encoding[2] for encoding in test_encodings])
])

# 设置超参数
batch_size = 2
num_epochs = 3
learning_rate = 2e-5

# 创建数据加载器
train_dataloader = DataLoader(
    train_dataset,
    sampler=RandomSampler(train_dataset),
    batch_size=batch_size
)

test_dataloader = DataLoader(
    test_dataset,
    batch_size=batch_size
)

# 训练模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    model.train()
    for batch in train_dataloader:
        input_ids, attention_mask, labels = (t.to(device) for t in batch)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs[0]

        loss.backward()
        optimizer.step()
        model.zero_grad()

    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

# 评估模型
model.eval()
y_pred = []
y_true = []

for batch in test_dataloader:
    input_ids, attention_mask, labels = (t.to(device) for t in batch)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs[0]

    predictions = torch.argmax(logits, dim=2)

    for pred, true in zip(predictions, labels):
        pred_labels = [label_list[p.item()] for p in pred]
        true_labels = [label_list[t.item()] for t in true if t != -100]

        y_pred.extend(pred_labels)
        y_true.extend(true_labels)


model_path = "keyword_extraction_model.pt"
torch.save(model.state_dict(), model_path)