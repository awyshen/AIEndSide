from intent_recognition import IntentRecognizer

recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=False, enable_cache=False)

test_cases = [
    ("播放脱口秀大会最新一期", "app_control", {"control": "play", "program": "脱口秀大会最新一期"}),
    ("播放奔跑吧", "app_control", {"control": "play", "program": "奔跑吧"}),
    ("我想看国家宝藏", "app_control", {"control": "play", "program": "国家宝藏"}),
    ("乘风破浪的姐姐第三季", "app_control", {"control": "play", "program": "乘风破浪的姐姐第三季"}),
    ("一年一度喜剧大赛第二季", "app_control", {"control": "play", "program": "一年一度喜剧大赛第二季"}),
    ("喜剧人单口季", "app_control", {"control": "play", "program": "喜剧人单口季"}),
    
    ("音量调到最大", "volume_control", {"volume": "up"}),
    ("音量调到最小", "volume_control", {"volume": "down"}),
    ("把声音调到50%", "volume_control", {"volume": "50"}),
    ("静音", "volume_control", {"volume": "mute"}),
    ("取消静音", "volume_control", {"volume": "up"}),
    
    ("我想听周杰伦的七里香", "music_control", {"control": "play", "singer": "周杰伦", "song": "七里香"}),
    ("放一首陈奕迅的歌", "music_control", {"control": "play", "singer": "陈奕迅"}),
    ("播放歌曲后来", "music_control", {"control": "play", "song": "后来"}),
    ("打开网易云音乐", "music_control", {"control": "open", "app": "netease_music_app"}),
    ("关闭酷狗音乐", "music_control", {"control": "close", "app": "kugou_music_app"}),
    
    ("导航到卧室", "robot_control", {"place": "卧室"}),
    ("去书房", "robot_control", {"place": "书房"}),
    ("来阳台", "robot_control", {"place": "阳台"}),
    ("不要去卧室了", "robot_control", {"control": "cancel"}),
    ("停止充电", "robot_control", {"control": "stop"}),
    
    ("打开投影", "projector_control", {"control": "open"}),
    ("把投影仪关掉", "projector_control", {"control": "close"}),
    
    ("打开优酷", "app_control", {"control": "open", "app": "youku_video_app"}),
    ("关闭腾讯视频", "app_control", {"control": "close", "app": "tencent_video_app"}),
    ("播放电影阿凡达", "app_control", {"control": "play", "film": "阿凡达"}),
    
    ("你好", "chat", {}),
    ("今天天气怎么样", "chat", {}),
    ("讲个笑话", "chat", {}),
    
    ("退下", "assistant_control", {"control": "sleep"}),
    ("休息", "assistant_control", {"control": "sleep"}),
]

print("=" * 80)
print("泛化性测试")
print("策略说明:")
print("  - 规则模板优先：高置信度直接返回")
print("  - LLM保守兜底：置信度<0.8不返回，宁错过不错判")
print("  - 无把握的请求移交下游处理")
print("=" * 80)

correct = 0
total = len(test_cases)

for i, (query, expected_intent, expected_params) in enumerate(test_cases, 1):
    result = recognizer.recognize(query)
    
    intent_ok = result.get("intent") == expected_intent
    params_ok = True
    
    for key, expected_value in expected_params.items():
        if result.get("params", {}).get(key) != expected_value:
            params_ok = False
            break
    
    status = "✓" if intent_ok and params_ok else "✗"
    
    print(f"{status} [{i:2d}/{total}]")
    print(f"  输入: {query}")
    print(f"  期望意图: {expected_intent}")
    print(f"  期望参数: {expected_params}")
    print(f"  实际意图: {result.get('intent', 'unknown')}")
    print(f"  实际参数: {result.get('params', {})}")
    print(f"  置信度: {result.get('confidence', 0.0):.2f}")
    print(f"  来源: {result.get('source', 'unknown')}")
    
    if intent_ok and params_ok:
        correct += 1
    
    print()

print("=" * 80)
print(f"泛化性测试准确率: {correct}/{total} ({correct/total*100:.2f}%)")
print("=" * 80)
