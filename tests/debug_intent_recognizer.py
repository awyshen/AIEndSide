from intent_recognition import IntentRecognizer

print("测试 IntentRecognizer 实例是否存在状态问题")
print("=" * 60)

recognizer = IntentRecognizer(use_llm=False, strict_mode=True, debug=True, enable_cache=False)

test_texts = [
    "不要去充电了",
    "去充电",
    "停止充电",
    "不要去充电了",
]

print("\n测试1: 连续调用相同文本")
for i, text in enumerate(test_texts, 1):
    print(f"\n第{i}次调用 '{text}':")
    result = recognizer.recognize(text)
    print(f"  params: {result.get('params')}, confidence: {result.get('confidence')}")

print("\n" + "=" * 60)
print("\n测试2: 使用新的IntentRecognizer实例")
recognizer2 = IntentRecognizer(use_llm=False, strict_mode=True, debug=True, enable_cache=False)
result = recognizer2.recognize("不要去充电了")
print(f"  params: {result.get('params')}, confidence: {result.get('confidence')}")
