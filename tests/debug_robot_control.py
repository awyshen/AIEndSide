from intent_recognition.rule_engine import RuleEngine

engine = RuleEngine()
text = "不要去充电了"

print(f"输入: {text}")
print("\n1. 调用 match_keywords:")
matched_intents = engine.match_keywords(text)
print(f"   匹配结果: {matched_intents}")

print("\n2. 检查special_cases匹配:")
special_cases = [
    ("打开音乐播放器", "music_control", 0.9),
    ("关闭音乐播放器", "music_control", 0.9),
    ("启动音乐播放器", "music_control", 0.9),
    ("停止音乐播放器", "music_control", 0.9),
    ("打开QQ音乐", "music_control", 0.9),
    ("关闭QQ音乐", "music_control", 0.9),
    ("打开网易云音乐", "music_control", 0.9),
    ("关闭网易云音乐", "music_control", 0.9),
    ("打开酷狗音乐", "music_control", 0.9),
    ("关闭酷狗音乐", "music_control", 0.9),
    ("导航到", "robot_control", 0.85),
    ("去客厅", "robot_control", 0.85),
    ("去卧室", "robot_control", 0.85),
    ("去书房", "robot_control", 0.85),
    ("去阳台", "robot_control", 0.85),
    ("让机器人去", "robot_control", 0.85),
    ("取消当前导航", "robot_control", 0.85),
    ("不要去充电", "robot_control", 0.9),
    ("不要去充电桩", "robot_control", 0.9),
]

import re
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

print(f"\n3. special_cases匹配结果:")
print(f"   intent: {intent}")
print(f"   confidence: {confidence}")
print(f"   score: {score}")

print("\n4. 调用 match_patterns:")
result = engine.match_patterns(intent if intent else "robot_control", text)
print(f"   value: {result['value']}")
print(f"   params: {result['params']}")
print(f"   pattern_matched: {result['pattern_matched']}")
