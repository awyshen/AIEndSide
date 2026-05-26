from intent_recognition.llm_client import QwenAPI

llm = QwenAPI()

test_cases = [
    "调高音量播放周杰伦的晴天",
    "今天天气怎么样",
    "导航到客厅打开音乐",
    "播放喜剧人单口季",
    "关闭音乐播放器休息一下",
    "声音有点大，帮我调小一点",
    "我想听一首舒缓的歌曲",
    "让机器人去书房充电",
    "给我讲个有趣的故事",
    "打开爱奇艺播放奔跑吧",
]

print("=" * 80)
print("LLM优化测试")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n[{i:2d}] 输入: {test}")
    result = llm.classify_intent(test)
    
    print(f"  意图: {result.get('intent', 'unknown')}")
    print(f"  值: {result.get('value', '')}")
    print(f"  参数: {result.get('params', {})}")
    print(f"  置信度: {result.get('confidence', 0.0):.2f}")
    
    if "tasks" in result and result["tasks"]:
        print("  任务拆分:")
        for j, task in enumerate(result["tasks"], 1):
            print(f"    {j}. {task['intent']}(value={task['value']}, params={task['params']}, conf={task['confidence']:.2f})")
    
    if "error" in result:
        print(f"  错误: {result['error']}")
        if "raw_response" in result:
            print(f"  原始响应: {result['raw_response']}")

print("\n" + "=" * 80)
