from intent_recognition import IntentRecognizer
from intent_recognition.rule_engine import RuleEngine

print("=== 调试规则引擎 ===")
rule_engine = RuleEngine()

test_cases = [
    "打开音乐播放器",
    "关闭QQ音乐",
    "打开QQ音乐",
    "关闭音乐播放器"
]

for test in test_cases:
    result = rule_engine.recognize(test)
    print(f"输入: {test}")
    print(f"规则引擎输出: {result}")
    print()

print("\n=== 调试融合逻辑 ===")
recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

for test in test_cases:
    result = recognizer.recognize(test)
    print(f"输入: {test}")
    print(f"最终结果: {result}")
    print()
