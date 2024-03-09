import torch
import torch.nn.functional as F
from transformers import BertTokenizer
from model01_train import ChineseSentimentClassifier

class SentimentAnalyzer:
    def __init__(self, model_path, tokenizer_path, max_length=512):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = ChineseSentimentClassifier.load_from_checkpoint(model_path).to(self.device)
        self.model.eval()
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.max_length = max_length

    def analyze(self, text):
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            pad_to_max_length=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids, attention_mask = encoding['input_ids'].to(self.device), encoding['attention_mask'].to(self.device)
        _, logits = self.model(input_ids, attention_mask)
        probs = F.softmax(logits, dim=1)
        label = probs.argmax().item()
        sentiment = '消极' if label == 0 else '中性' if label == 1 else '积极'
        return sentiment, probs[:, label].item()

class SentimentAnalyzerApp:
    def __init__(self, model_path, tokenizer_path):
        self.analyzer = SentimentAnalyzer(model_path, tokenizer_path)

    def run(self,text):
        sentiment, score = self.analyzer.analyze(text)
        return sentiment,score