from intent_recognition.rule_engine import RuleEngine

engine = RuleEngine()

print("测试多次调用 rule_engine.recognize 是否存在状态污染")
print("=" * 60)

text = "不要去充电了"
print(f"\n输入: '{text}'")

print("\n第1次调用:")
result1 = engine.recognize(text)
print(f"  result1: params={result1.get('params')}, confidence={result1.get('confidence')}")

print("\n第2次调用:")
result2 = engine.recognize(text)
print(f"  result2: params={result2.get('params')}, confidence={result2.get('confidence')}")

print("\n第3次调用:")
result3 = engine.recognize(text)
print(f"  result3: params={result3.get('params')}, confidence={result3.get('confidence')}")

print("\n检查是否有实例变量被修改:")
print(f"  engine.song_pattern_detected: {getattr(engine, 'song_pattern_detected', 'NOT SET')}")
print(f"  engine.nav_pattern_detected: {getattr(engine, 'nav_pattern_detected', 'NOT SET')}")
