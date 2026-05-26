import sys
from intent_recognition.rule_engine import RuleEngine

text = "不要去充电了"
print(f"输入: '{text}'")

engine = RuleEngine()

print("\n1. 调用 recognize 方法")
print(f"   text = '{text}'")

matched_intents = engine.match_keywords(text)
print(f"\n2. match_keywords 结果: {matched_intents}")

intent = None
confidence = 0.0
score = 0

special_cases = [
    ("打开音乐播放器", "music_control", 0.9),
    ("不要去充电了", "robot_control", 0.9),
    ("不要去充电桩了", "robot_control", 0.9),
    ("不要去充电", "robot_control", 0.9),
    ("不要去充电桩", "robot_control", 0.9),
]

import re
for i, (pattern, target_intent, default_confidence) in enumerate(special_cases):
    if ".*" in pattern:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"\n3. special_cases 匹配 [{i}]: '{pattern}' -> {target_intent}, confidence={default_confidence}")
            intent = target_intent
            confidence = default_confidence
            score = 10
            break
    elif pattern.lower() in text.lower():
        print(f"\n3. special_cases 匹配 [{i}]: '{pattern}' -> {target_intent}, confidence={default_confidence}")
        intent = target_intent
        confidence = default_confidence
        score = 10
        break

if not intent:
    print("\n3. special_cases 没有匹配")
    if matched_intents:
        top_intent = matched_intents[0]
        intent = top_intent["intent"]
        confidence = top_intent["confidence"]
        score = top_intent["score"]
        print(f"   使用 match_keywords 结果: intent={intent}, confidence={confidence}")

print(f"\n4. 最终 intent={intent}, confidence={confidence}, score={score}")

print("\n5. 调用 match_patterns")
result = engine.match_patterns(intent, text)
print(f"   result: {result}")

final_confidence = confidence
if result["pattern_matched"]:
    bonus = 0.1
    if engine.song_pattern_detected:
        bonus = 0.25
    elif engine.nav_pattern_detected:
        bonus = 0.15
    final_confidence = min(1.0, confidence + bonus)

print(f"\n6. 最终置信度计算:")
print(f"   base confidence: {confidence}")
print(f"   bonus: {bonus}")
print(f"   final_confidence: {final_confidence}")

print(f"\n7. 最终结果:")
print(f"   intent: {intent}")
print(f"   value: {result['value']}")
print(f"   params: {result['params']}")
print(f"   confidence: {final_confidence}")
