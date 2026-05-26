from intent_recognition.rule_engine import RuleEngine

engine = RuleEngine()

test_cases = [
    "找一首孙燕姿的经典歌曲",
    "启动优酷视频",
]

for test in test_cases:
    print(f"\n输入: {test}")
    result = engine.recognize(test)
    print(f"结果: {result}")
