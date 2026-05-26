from intent_recognition import IntentRecognizer
from intent_recognition.rule_engine import RuleEngine

print("=== 调试失败案例 ===")
rule_engine = RuleEngine()

test_cases = [
    "打开音乐播放器",
    "关闭QQ音乐",
]

print("\n--- 规则引擎输出 ---")
for test in test_cases:
    result = rule_engine.recognize(test)
    print(f"输入: {test}")
    print(f"规则引擎输出: {result}")
    print()

print("\n--- 融合后输出 ---")
recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

for test in test_cases:
    result = recognizer.recognize(test)
    print(f"输入: {test}")
    print(f"最终结果: {result}")
    if "debug" in result:
        print(f"调试信息: {result['debug']}")
    print()
