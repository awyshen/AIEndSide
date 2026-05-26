from intent_recognition import IntentRecognizer

recognizer = IntentRecognizer(use_llm=False, strict_mode=True, debug=True, enable_cache=False)

result = recognizer.recognize("不要去充电了")

print("完整识别结果:")
print(f"意图: {result.get('intent')}")
print(f"值: {result.get('value')}")
print(f"参数: {result.get('params')}")
print(f"置信度: {result.get('confidence')}")
print(f"来源: {result.get('source')}")

if "debug" in result:
    print("\n调试信息:")
    print(f"原始输入: {result['debug'].get('original_input')}")
    print(f"清洗后文本: {result['debug'].get('cleaned_text')}")
    print(f"规则结果: {result['debug'].get('rule_result')}")
