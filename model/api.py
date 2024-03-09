import os
from flask import Flask, request, jsonify
from model2 import KeywordExtractor
from model1 import SentimentAnalyzerApp

# 加载模型
keyword_extractor = KeywordExtractor('keyword_extraction_model.pt')
sentiment_app = SentimentAnalyzerApp('sentiment_model.ckpt', 'tokenizer_path')

# 设置鉴权码
AUTH_TOKEN = 'your_secret_token'

app = Flask(__name__)

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_api():
    # 检查鉴权码
    auth_token = request.headers.get('Authorization')
    if auth_token != AUTH_TOKEN:
        return jsonify({'error': 'Invalid auth token'}), 401

    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    keywords = keyword_extractor.extract_keywords(text)
    return jsonify({'keywords': keywords})

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_api():
    # 检查鉴权码
    auth_token = request.headers.get('Authorization')
    if auth_token != AUTH_TOKEN:
        return jsonify({'error': 'Invalid auth token'}), 401

    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    sentiment, score = sentiment_app.run(text)
    return jsonify({'sentiment': sentiment, 'score': score})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)