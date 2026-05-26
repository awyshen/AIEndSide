from intent_recognition.rule_engine import RuleEngine

engine = RuleEngine()
text = "不要去充电了"

print(f"输入: '{text}'")

result = engine.recognize(text)

print(f"\nrecognize 方法返回结果:")
print(f"  intent: {result.get('intent')}")
print(f"  value: {result.get('value')}")
print(f"  params: {result.get('params')}")
print(f"  confidence: {result.get('confidence')}")
