from intent_recognition.rule_engine import RuleEngine
import re

engine = RuleEngine()
text = "不要去充电了"

print(f"输入: {text}")
print("\n=== Step 1: match_keywords ===")
matched_intents = engine.match_keywords(text)
print(f"匹配结果: {matched_intents}")

print("\n=== Step 2: special_cases ===")
special_cases = [
    ("不要去充电了", "robot_control", 0.9),
    ("不要去充电桩了", "robot_control", 0.9),
    ("不要去充电", "robot_control", 0.9),
    ("不要去充电桩", "robot_control", 0.9),
    ("去充电", "robot_control", 0.9),
]

intent = None
confidence = 0.0
score = 0

for i, (pattern, target_intent, default_confidence) in enumerate(special_cases):
    if ".*" in pattern:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"   [{i}] 正则匹配成功: {pattern} -> {target_intent}")
            intent = target_intent
            confidence = default_confidence
            score = 10
            break
    elif pattern.lower() in text.lower():
        print(f"   [{i}] 字符串匹配成功: {pattern} -> {target_intent}")
        intent = target_intent
        confidence = default_confidence
        score = 10
        break
    else:
        print(f"   [{i}] 不匹配: {pattern}")

print(f"\n=== Step 3: special_cases结果 ===")
print(f"intent: {intent}")
print(f"confidence: {confidence}")
print(f"score: {score}")

print("\n=== Step 4: match_patterns ===")
print(f"调用 match_patterns('{intent}', '{text}')")
result = engine.match_patterns(intent, text)
print(f"返回结果: {result}")

print("\n=== Step 5: 计算最终置信度 ===")
final_confidence = confidence
if result["pattern_matched"]:
    bonus = 0.1
    if engine.song_pattern_detected:
        bonus = 0.25
    elif engine.nav_pattern_detected:
        bonus = 0.15
    final_confidence = min(1.0, confidence + bonus)

print(f"最终置信度: {final_confidence}")

print("\n=== 最终结果 ===")
print({
    "intent": intent,
    "value": result["value"],
    "params": result["params"],
    "confidence": final_confidence,
    "method": "rule_based",
    "pattern_matched": result["pattern_matched"]
})
