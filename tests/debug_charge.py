from intent_recognition import IntentRecognizer

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

test_cases = [
    "不要去充电了",
    "不要充电了",
    "停止充电",
    "去充电",
    "取消充电",
]

for test in test_cases:
    print(f"\n{'='*60}")
    print(f"输入: {test}")
    print(f"{'='*60}")
    result = recognizer.recognize(test)
    
    print(f"意图: {result.get('intent', 'unknown')}")
    print(f"值: {result.get('value', '')}")
    print(f"参数: {result.get('params', {})}")
    print(f"置信度: {result.get('confidence', 0.0):.2f}")
    print(f"来源: {result.get('source', 'unknown')}")
    
    if "debug" in result:
        print("\n调试信息:")
        print(f"  规则结果: {result['debug'].get('rule_result')}")
        print(f"  LLM结果: {result['debug'].get('llm_result')}")
        print(f"  决策原因: {result['debug'].get('fusion_decision')}")
    
    print(f"\n{'='*60}")
