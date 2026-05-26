from intent_recognition import IntentRecognizer

print("=" * 60)
print("测试 use_llm=True 的情况")
print("=" * 60)

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

text = "不要去充电了"
print(f"\n输入文本: '{text}'")

result = recognizer.recognize(text)

print(f"\n最终结果:")
print(f"   intent: {result.get('intent')}")
print(f"   value: {result.get('value')}")
print(f"   params: {result.get('params')}")
print(f"   confidence: {result.get('confidence')}")
print(f"   source: {result.get('source')}")

if "debug" in result:
    print(f"\n调试信息:")
    print(f"   rule_result: {result['debug'].get('rule_result')}")
    print(f"   llm_result: {result['debug'].get('llm_result')}")
    print(f"   fusion_decision: {result['debug'].get('fusion_decision')}")
