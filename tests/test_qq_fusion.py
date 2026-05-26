from intent_recognition import IntentRecognizer

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

test_cases = [
    "打开QQ音乐",
    "关闭QQ音乐",
]

for test in test_cases:
    print(f"\n输入: {test}")
    result = recognizer.recognize(test)
    print(f"结果: {result}")
    if "debug" in result:
        print(f"调试信息:")
        print(f"  规则结果: {result['debug'].get('rule_result')}")
        print(f"  LLM结果: {result['debug'].get('llm_result')}")
        print(f"  决策原因: {result['debug'].get('fusion_decision')}")
