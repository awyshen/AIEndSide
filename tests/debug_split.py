from intent_recognition.result_fusion import ResultFusion

fusion = ResultFusion()

test_cases = [
    "关闭音乐播放器休息一下",
    "关闭音乐播放器",
    "休息一下",
]

for test in test_cases:
    print(f"\n输入: {test}")
    split_result = fusion.split_multi_task(test)
    print(f"分割结果: {split_result}")
