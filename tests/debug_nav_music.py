from intent_recognition import IntentRecognizer

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

test_cases = [
    "导航到客厅打开音乐",
    "打开音乐",
    "打开音乐播放器",
]

for test in test_cases:
    print(f"\n{'='*60}")
    print(f"输入: {test}")
    print(f"{'='*60}")
    result = recognizer.recognize(test)
    
    print(f"意图: {result.get('intent', 'unknown')}")
    print(f"置信度: {result.get('confidence', 0.0):.2f}")
    print(f"来源: {result.get('source', 'unknown')}")
    print(f"查询类型: {result.get('query_type', 'single_task')}")
    
    if result.get("query_type") == "multi_task" and "tasks" in result:
        print("\n任务拆分:")
        for i, task in enumerate(result["tasks"], 1):
            print(f"\n任务 {i}:")
            print(f"  意图: {task['intent']}")
            print(f"  值: {task['value']}")
            print(f"  参数: {task['params']}")
            print(f"  置信度: {task['confidence']:.2f}")
            print(f"  来源: {task.get('source', 'unknown')}")
    
    if "debug" in result:
        print("\n调试信息:")
        print(f"  规则结果: {result['debug'].get('rule_result')}")
        print(f"  LLM结果: {result['debug'].get('llm_result')}")
        print(f"  决策原因: {result['debug'].get('fusion_decision')}")
    
    print(f"\n{'='*60}")
