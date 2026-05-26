from intent_recognition import IntentRecognizer
from intent_recognition.rule_engine import RuleEngine

print("=== 调试QQ音乐问题 ===")
rule_engine = RuleEngine()

test_cases = [
    "打开QQ音乐",
    "关闭QQ音乐",
]

print("\n--- 规则引擎输出 ---")
for test in test_cases:
    result = rule_engine.recognize(test)
    print(f"输入: {test}")
    print(f"规则引擎输出: {result}")
    print()

print("\n--- 预处理后的文本 ---")
from intent_recognition.preprocessor import TextPreprocessor
preprocessor = TextPreprocessor()
for test in test_cases:
    result = preprocessor.process(test)
    print(f"输入: {test}")
    print(f"预处理后: {result}")
    print()
