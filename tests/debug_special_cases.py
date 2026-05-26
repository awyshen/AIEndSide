import re

text = "不要去充电了"

special_cases = [
    ("打开音乐播放器", "music_control", 0.9),
    ("关闭音乐播放器", "music_control", 0.9),
    ("启动音乐播放器", "music_control", 0.9),
    ("停止音乐播放器", "music_control", 0.9),
    ("打开QQ音乐", "music_control", 0.9),
    ("关闭QQ音乐", "music_control", 0.9),
    ("打开网易云音乐", "music_control", 0.9),
    ("关闭网易云音乐", "music_control", 0.9),
    ("打开酷狗音乐", "music_control", 0.9),
    ("关闭酷狗音乐", "music_control", 0.9),
    ("导航到", "robot_control", 0.85),
    ("去客厅", "robot_control", 0.85),
    ("去卧室", "robot_control", 0.85),
    ("去书房", "robot_control", 0.85),
    ("去阳台", "robot_control", 0.85),
    ("让机器人去", "robot_control", 0.85),
    ("取消当前导航", "robot_control", 0.85),
    ("不要去充电", "robot_control", 0.9),
    ("不要去充电桩", "robot_control", 0.9),
    ("我想听.*?的歌", "music_control", 0.85),
    ("放一首.*?的歌", "music_control", 0.85),
    ("我想听.*?", "music_control", 0.85),
    ("播放一首.*?", "music_control", 0.85),
    ("找一首.*?", "music_control", 0.9),
    ("播放音乐", "music_control", 0.8),
    ("播放歌曲", "music_control", 0.8),
    ("播放歌", "music_control", 0.8),
    ("继续播放", "music_control", 0.8),
    ("打开音乐", "music_control", 0.9),
    ("播放.*?的.*?", "music_control", 0.8),
    ("启动.*视频", "app_control", 0.9),
    ("帮我打开", "app_control", 0.9),
    ("你好", "chat", 0.9),
    ("您好", "chat", 0.9),
    ("今天天气怎么样", "chat", 0.95),
    ("讲个笑话", "chat", 0.95),
    ("讲个.*故事", "chat", 0.95),
    ("能帮我做什么", "chat", 0.95),
    ("你能做什么", "chat", 0.95),
]

print(f"输入: {text}")
print("\n匹配过程:")

for i, (pattern, target_intent, default_confidence) in enumerate(special_cases):
    if ".*" in pattern:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"[{i}] 正则匹配: {pattern} -> {target_intent}")
            print(f"    匹配成功！")
            break
    elif pattern.lower() in text.lower():
        print(f"[{i}] 字符串匹配: {pattern} -> {target_intent}")
        print(f"    匹配成功！")
        break
    else:
        print(f"[{i}] 不匹配: {pattern}")
