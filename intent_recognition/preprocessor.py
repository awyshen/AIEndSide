
import re

class TextPreprocessor:
    def __init__(self):
        self.stopwords = ["的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"]
    
    def clean_text(self, text):
        text = text.strip()
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'[^\w\s\u4e00-\u9fa5]', '', text)
        return text
    
    def tokenize(self, text):
        chars = []
        i = 0
        while i < len(text):
            if text[i] == ' ':
                i += 1
                continue
            found = False
            for j in range(min(4, len(text) - i), 0, -1):
                word = text[i:i+j]
                if word in self.stopwords or len(word) > 0:
                    chars.append(word)
                    i += j
                    found = True
                    break
            if not found:
                chars.append(text[i])
                i += 1
        return chars
    
    def extract_keywords(self, text):
        tokens = self.tokenize(text)
        return [t for t in tokens if t not in self.stopwords]
    
    def normalize(self, text):
        text = text.lower()
        text = re.sub(r'[。，！？；：、]', '', text)
        return text
    
    def process(self, text):
        text = self.clean_text(text)
        text = self.normalize(text)
        keywords = self.extract_keywords(text)
        return {
            "cleaned_text": text,
            "keywords": keywords,
            "tokens": self.tokenize(text)
        }
