from intent_recognition import IntentRecognizer

def load_test_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def evaluate_single_task():
    test_data = load_test_data('/Users/terminus/Desktop/workspace/application/terminus/AIEndSide/evaluation_data.txt')

    print("=" * 90)
    print("单任务测试评估")
    print("策略: 规则优先(高准确率) + LLM保守兜底(宁错过不错判)")
    print("=" * 90)
    print(f"测试样本数: {len(test_data)}")
    print()

    recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=False, enable_cache=False)

    results = []
    for input_text in test_data:
        result = recognizer.recognize(input_text)
        results.append(result)

    correct = sum(1 for r in results if r.get("intent") != "unknown")
    accuracy = correct / len(results) * 100

    print(f"识别准确率: {accuracy:.2f}% ({correct}/{len(results)})")
    print()

    source_counts = {}
    for result in results:
        source = result.get("source", "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1

    print("识别来源分布:")
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count}")

    print()
    print("识别结果详情:")
    print("-" * 90)
    print(f"{'状态':<4} {'来源':<25} {'输入':<20} {'意图':<20} {'value':<15} {'params':<30} {'置信度':<8}")
    print("-" * 90)

    for input_text, result in zip(test_data, results):
        status = "✓" if result.get("intent") != "unknown" else "✗"
        intent = result.get("intent", "unknown")
        confidence = result.get("confidence", 0)
        source = result.get("source", "unknown")
        value = result.get("value", "")
        params = result.get("params", {})
        
        print(f"{status:<4} {source:<25} {input_text:<20} {intent:<20} {value:<15} {str(params):<30} {confidence:<8.2f}")

    return accuracy

def evaluate_multi_task():
    multi_task_cases = [
        ("到客厅打开投影仪", ["robot_control", "projector_control"]),
        ("回去充电关闭投影仪", ["robot_control", "projector_control"]),
        ("关闭爱奇艺休息一下", ["app_control", "assistant_control"]),
        ("导航到客厅打开音乐", ["robot_control", "music_control"]),
        ("调高音量播放音乐", ["volume_control", "music_control"]),
        ("打开投影仪播放电影", ["projector_control", "app_control"]),
        ("导航到客厅播放音乐", ["robot_control", "music_control"]),
        ("关闭爱奇艺休息一下", ["app_control", "assistant_control"]),
    ]

    print("\n" + "=" * 90)
    print("多任务测试评估")
    print("=" * 90)
    print(f"测试样本数: {len(multi_task_cases)}")
    print()

    recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=False, enable_cache=False)

    correct = 0
    print(f"{'状态':<4} {'输入':<20} {'任务列表':<60}")
    print("-" * 90)

    for input_text, expected_intents in multi_task_cases:
        result = recognizer.recognize(input_text)
        query_type = result.get("query_type", "single_task")

        if query_type == "multi_task":
            tasks = result.get("tasks", [])
            intents = [t["intent"] for t in tasks]
            all_match = all(ei in intents for ei in expected_intents) and len(intents) == len(expected_intents)
            status = "✓" if all_match else "✗"
            
            task_details = []
            for task in tasks:
                intent = task.get("intent", "unknown")
                value = task.get("value", "")
                params = task.get("params", {})
                confidence = task.get("confidence", 0)
                task_details.append(f"{intent}(value={value}, params={params}, conf={confidence:.2f})")
            
            print(f"{status:<4} {input_text:<20} {' + '.join(task_details):<60}")
            if all_match:
                correct += 1
        else:
            intent = result.get("intent", "unknown")
            value = result.get("value", "")
            params = result.get("params", {})
            confidence = result.get("confidence", 0)
            print(f"✗ {input_text:<20} {intent}(value={value}, params={params}, conf={confidence:.2f}) (期望: {expected_intents})")

    accuracy = correct / len(multi_task_cases) * 100
    print(f"\n多任务准确率: {accuracy:.2f}% ({correct}/{len(multi_task_cases)})")
    return accuracy

if __name__ == "__main__":
    single_accuracy = evaluate_single_task()
    multi_accuracy = evaluate_multi_task()

    print("\n" + "=" * 90)
    print("评估总结")
    print("=" * 90)
    print(f"单任务准确率: {single_accuracy:.2f}%")
    print(f"多任务准确率: {multi_accuracy:.2f}%")
    print("策略说明:")
    print("  - 规则模板优先：高置信度直接返回")
    print("  - LLM保守兜底：置信度<0.8不返回，宁错过不错判")
    print("  - 无把握的请求移交下游处理")
    print("=" * 90)
