from intent_recognition import IntentRecognizer

print("测试1: 使用缓存")
recognizer_with_cache = IntentRecognizer(use_llm=False, strict_mode=True, debug=False, enable_cache=True)
result1 = recognizer_with_cache.recognize("不要去充电了")
print(f"结果: params={result1.get('params')}, confidence={result1.get('confidence')}")

print("\n测试2: 不使用缓存")
recognizer_no_cache = IntentRecognizer(use_llm=False, strict_mode=True, debug=False, enable_cache=False)
result2 = recognizer_no_cache.recognize("不要去充电了")
print(f"结果: params={result2.get('params')}, confidence={result2.get('confidence')}")
