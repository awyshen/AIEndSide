from intent_recognition import IntentRecognizer

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=True, enable_cache=False)

complex_test_cases = [
    ("把音量调到60%然后打开音乐", "multi_task"),
    ("先导航到卧室再打开投影仪", "multi_task"),
    ("关闭音乐播放器休息一下", "multi_task"),
    ("调高音量播放周杰伦的晴天", "multi_task"),
    ("打开爱奇艺播放最新的奔跑吧", "multi_task"),
    
    ("声音有点大，帮我调小一点", "volume_control"),
    ("麻烦把音量降低一些", "volume_control"),
    ("请将声音调整到适中", "volume_control"),
    
    ("我想听一首舒缓的歌曲", "music_control"),
    ("播放一首最近很火的歌", "music_control"),
    ("找一首孙燕姿的经典歌曲", "music_control"),
    
    ("帮我打开腾讯视频", "app_control"),
    ("启动优酷视频", "app_control"),
    ("播放一个搞笑视频", "app_control"),
    
    ("让机器人去书房充电", "robot_control"),
    ("导航到阳台然后回来", "robot_control"),
    ("取消当前导航任务", "robot_control"),
    
    ("关闭投影设备", "projector_control"),
    ("开启投影仪", "projector_control"),
    
    ("今天天气怎么样", "chat"),
    ("给我讲个有趣的故事", "chat"),
    ("你能帮我做什么", "chat"),
    
    ("请退下休息", "assistant_control"),
    ("暂时离开一下", "assistant_control"),
]

print("=" * 80)
print("LLM泛化性测试 - 复杂场景")
print("策略说明:")
print("  - 规则模板优先：高置信度直接返回")
print("  - LLM保守兜底：置信度<0.8不返回，宁错过不错判")
print("  - 无把握的请求移交下游处理")
print("=" * 80)

total = len(complex_test_cases)
recognized = 0
llm_count = 0
rule_count = 0
unknown_count = 0

for i, (query, expected_intent) in enumerate(complex_test_cases, 1):
    result = recognizer.recognize(query)
    
    intent = result.get("intent", "unknown")
    source = result.get("source", "unknown")
    confidence = result.get("confidence", 0.0)
    is_multi_task = result.get("query_type") == "multi_task"
    
    if intent != "unknown":
        recognized += 1
        if source == "llm_fallback":
            llm_count += 1
        elif "rule" in source.lower():
            rule_count += 1
    else:
        unknown_count += 1
    
    status = "✓" if intent != "unknown" else "✗"
    
    print(f"{status} [{i:2d}/{total}]")
    print(f"  输入: {query}")
    print(f"  期望意图: {expected_intent}")
    print(f"  实际意图: {intent}")
    print(f"  置信度: {confidence:.2f}")
    print(f"  来源: {source}")
    print(f"  查询类型: {result.get('query_type', 'single_task')}")
    
    if is_multi_task and "tasks" in result:
        print("  任务拆分:")
        for j, task in enumerate(result["tasks"], 1):
            print(f"    {j}. {task['intent']}(value={task['value']}, params={task['params']}, conf={task['confidence']:.2f})")
    
    print()

print("=" * 80)
print(f"识别成功率: {recognized}/{total} ({recognized/total*100:.2f}%)")
print(f"规则匹配: {rule_count}")
print(f"LLM兜底: {llm_count}")
print(f"未识别: {unknown_count}")
print("=" * 80)
