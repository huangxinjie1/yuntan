import torch
from transformers import BertForTokenClassification, BertTokenizer

class KeywordExtractor:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BertForTokenClassification.from_pretrained('bert-base-uncased', num_labels=3)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.label_list = ['O', 'B-KW', 'I-KW']

        # 加载训练好的模型权重
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def extract_keywords(self, text):
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=512
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs[0]

        predictions = torch.argmax(logits, dim=2)

        pred_labels = [self.label_list[p.item()] for p in predictions[0]]
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])

        keywords = []
        current_keyword = ""
        for token, label in zip(tokens, pred_labels):
            if label == 'B-KW':
                if current_keyword:
                    keywords.append(current_keyword.strip())
                current_keyword = token
            elif label == 'I-KW':
                current_keyword += " " + token
            else:
                if current_keyword:
                    keywords.append(current_keyword.strip())
                    current_keyword = ""

        if current_keyword:
            keywords.append(current_keyword.strip())
        return keywords