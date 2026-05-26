from intent_recognition.llm_client import QwenAPI

llm = QwenAPI()

test_cases = [
    "不要去充电了",
    "不要充电了",
    "停止充电",
    "去充电",
    "取消充电",
]

print("=" * 80)
print("仅使用LLM模块测试")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n[{i:2d}] 输入: {test}")
    result = llm.classify_intent(test)
    
    print(f"  意图: {result.get('intent', 'unknown')}")
    print(f"  值: {result.get('value', '')}")
    print(f"  参数: {result.get('params', {})}")
    print(f"  置信度: {result.get('confidence', 0.0):.2f}")
    
    if "error" in result:
        print(f"  错误: {result['error']}")
        if "raw_response" in result:
            print(f"  原始响应: {result['raw_response']}")

print("\n" + "=" * 80)
