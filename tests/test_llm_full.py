from intent_recognition.llm_client import QwenAPI

llm = QwenAPI()

single_task_cases = [
    "音量调低一些",
    "声音小一点",
    "声音太大了",
    "音量调高一些",
    "声音大点",
    "声音有点小",
    "音量调到70%",
    "声音调到70",
    "播放上一首音乐",
    "上一首歌",
    "播放下一首音乐",
    "下一首歌",
    "暂停播放歌曲",
    "暂停歌曲",
    "暂停音乐",
    "暂停放歌",
    "停止播放歌曲",
    "不要播放歌曲了",
    "不要播放音乐了",
    "不要放歌了",
    "停止放歌",
    "继续播放音乐",
    "继续播放歌曲",
    "继续放歌",
    "播放蔡琴的渡口",
    "播放蔡琴的歌",
    "播放歌曲渡口",
    "打开音乐播放器",
    "打开QQ音乐",
    "关闭音乐播放器",
    "关闭QQ音乐",
    "播放本地视频",
    "放本地视频",
    "播本地视频",
    "播放电影变形金刚",
    "播放喜剧人单口季节目",
    "停止播放视频",
    "停止播放本地视频",
    "打开爱奇艺",
    "关闭爱奇艺",
    "打开投影仪",
    "把投影打开",
    "关闭投影仪",
    "投影仪关了",
    "导航到客厅",
    "去客厅吧",
    "来客厅",
    "到客厅去",
    "回去充电",
    "去充电桩",
    "去充电",
    "取消导航",
    "不要去客厅了",
    "不要去充电了",
    "休息一下",
    "退下吧",
    "先下去吧",
    "我们聊一下吧",
]

multi_task_cases = [
    "到客厅打开投影仪",
    "回去充电关闭投影仪",
    "关闭爱奇艺休息一下",
    "导航到客厅打开音乐",
    "调高音量播放音乐",
    "打开投影仪播放电影",
    "导航到客厅播放音乐",
    "关闭爱奇艺休息一下",
]

print("=" * 80)
print("仅使用LLM模块进行意图识别和指令解析测试")
print("=" * 80)

print("\n" + "=" * 80)
print("一、单任务测试")
print("=" * 80)

single_success = 0
single_total = len(single_task_cases)

for i, test in enumerate(single_task_cases, 1):
    print(f"\n[{i:2d}/{single_total}] 输入: {test}")
    result = llm.classify_intent(test)
    
    intent = result.get('intent', 'unknown')
    value = result.get('value', '')
    params = result.get('params', {})
    confidence = result.get('confidence', 0.0)
    
    print(f"  意图: {intent}")
    print(f"  值: {value}")
    print(f"  参数: {params}")
    print(f"  置信度: {confidence:.2f}")
    
    if intent != 'unknown':
        single_success += 1
    
    if "error" in result:
        print(f"  错误: {result['error']}")

print(f"\n单任务识别成功率: {single_success}/{single_total} ({single_success/single_total*100:.1f}%)")

print("\n" + "=" * 80)
print("二、多任务测试")
print("=" * 80)

multi_success = 0
multi_total = len(multi_task_cases)

for i, test in enumerate(multi_task_cases, 1):
    print(f"\n[{i:2d}/{multi_total}] 输入: {test}")
    result = llm.classify_intent(test)
    
    intent = result.get('intent', 'unknown')
    value = result.get('value', '')
    params = result.get('params', {})
    confidence = result.get('confidence', 0.0)
    tasks = result.get('tasks', [])
    
    print(f"  意图: {intent}")
    print(f"  值: {value}")
    print(f"  参数: {params}")
    print(f"  置信度: {confidence:.2f}")
    
    if intent == 'multi_task' and tasks:
        print(f"  任务拆分:")
        for j, task in enumerate(tasks, 1):
            print(f"    {j}. {task['intent']}(value={task['value']}, params={task['params']}, conf={task['confidence']:.2f})")
        multi_success += 1
    elif intent != 'unknown':
        print(f"  ⚠️  未识别为多任务")
    
    if "error" in result:
        print(f"  错误: {result['error']}")

print(f"\n多任务识别成功率: {multi_success}/{multi_total} ({multi_success/multi_total*100:.1f}%)")

print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"单任务成功率: {single_success}/{single_total} ({single_success/single_total*100:.1f}%)")
print(f"多任务成功率: {multi_success}/{multi_total} ({multi_success/multi_total*100:.1f}%)")
print(f"总体成功率: {(single_success+multi_success)}/{(single_total+multi_total)} ({(single_success+multi_success)/(single_total+multi_total)*100:.1f}%)")
print("=" * 80)
