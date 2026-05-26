from intent_recognition.result_fusion import ResultFusion

fusion = ResultFusion()
text = "不要去充电了"

print(f"输入: '{text}'")
print(f"长度: {len(text)}")

result = fusion.split_multi_task(text)
print(f"\nsplit_multi_task 结果: {result}")
print(f"任务数量: {len(result)}")

if len(result) > 1:
    print("\n多任务分割:")
    for i, task in enumerate(result):
        print(f"  任务{i+1}: '{task}'")
