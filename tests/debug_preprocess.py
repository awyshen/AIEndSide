from intent_recognition.preprocessor import TextPreprocessor

preprocessor = TextPreprocessor()

test_cases = [
    "不要去充电了",
    "不要充电了",
    "停止充电",
    "去充电",
]

for test in test_cases:
    result = preprocessor.process(test)
    print(f"输入: '{test}'")
    print(f"清洗后: '{result['cleaned_text']}'")
    print(f"长度: {len(result['cleaned_text'])}")
    print(f"字符列表: {[c for c in result['cleaned_text']]}")
    print()
