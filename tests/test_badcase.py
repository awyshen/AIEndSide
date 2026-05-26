from intent_recognition.llm_client import QwenAPI

llm = QwenAPI()

badcase_cases = [
    # 音量控制
    {"input": "声音太大了", "expected_intent": "volume_control", "expected_params": {"volume": "down"}},
    {"input": "声音有点小", "expected_intent": "volume_control", "expected_params": {"volume": "up"}},
    
    # 音乐控制
    {"input": "播放上一首音乐", "expected_intent": "music_control", "expected_params": {"control": "previous"}},
    {"input": "播放蔡琴的歌", "expected_intent": "music_control", "expected_params": {"control": "play", "singer": "蔡琴"}},
    {"input": "播放歌曲渡口", "expected_intent": "music_control", "expected_params": {"control": "play", "song": "渡口"}},
    
    # 应用控制
    {"input": "放本地视频", "expected_intent": "app_control", "expected_params": {"control": "open", "app": "default_video_app"}},
    {"input": "播本地视频", "expected_intent": "app_control", "expected_params": {"control": "open", "app": "default_video_app"}},
    
    # 机器人控制
    {"input": "到客厅去", "expected_intent": "robot_control", "expected_params": {"place": "客厅"}},
    {"input": "不要去客厅了", "expected_intent": "robot_control", "expected_params": {"control": "cancel"}},
]

print("=" * 80)
print("Badcase修复测试")
print("=" * 80)

success_count = 0
total_count = len(badcase_cases)

for i, case in enumerate(badcase_cases, 1):
    print(f"\n[{i:2d}/{total_count}] 输入: {case['input']}")
    
    result = llm.classify_intent(case["input"])
    
    intent = result.get("intent", "unknown")
    params = result.get("params", {})
    
    print(f"  识别意图: {intent}")
    print(f"  识别参数: {params}")
    print(f"  期望意图: {case['expected_intent']}")
    print(f"  期望参数: {case['expected_params']}")
    
    intent_match = intent == case["expected_intent"]
    params_match = params == case["expected_params"]
    
    if intent_match and params_match:
        print("  ✅ 通过")
        success_count += 1
    else:
        print("  ❌ 失败")
        if not intent_match:
            print(f"    意图不匹配: {intent} != {case['expected_intent']}")
        if not params_match:
            print(f"    参数不匹配: {params} != {case['expected_params']}")

print(f"\n测试结果: {success_count}/{total_count} 通过 ({success_count/total_count*100:.1f}%)")
print("=" * 80)
