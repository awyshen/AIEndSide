import json
import sys
sys.path.insert(0, '/Users/terminus/Desktop/workspace/application/terminus/AIEndSide')
from intent_recognition.llm_client import QwenAPI

model_config = {
    "api_key": "sk-no-key-required",
    "base_url": "http://10.61.85.20:33790/v1",
    # "model_name": "qwen"
    "model_name": "minicpm5-1b"
}

llm = QwenAPI(model_config=model_config)

with open('/Users/terminus/Desktop/workspace/application/terminus/AIEndSide/tests/test_cases.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

print("=" * 80)
print("意图识别测试套件")
print(f"版本: {test_data['version']}")
print(f"测试用例数: {len(test_data['test_cases'])}")
print("=" * 80)

success_count = 0
failed_cases = []

for case in test_data['test_cases']:
    case_id = case['id']
    user_input = case['input']
    expected = case['expected']
    
    print(f"\n[{case_id}] 输入: {user_input}")
    
    result = llm.classify_intent(user_input)
    
    intent = result.get('intent', 'unknown')
    value = result.get('value', '')
    params = result.get('params', {})
    confidence = result.get('confidence', 0.0)
    
    expected_intent = expected['intent']
    expected_value = expected['value']
    expected_params = expected.get('params', {})
    
    print(f"  识别结果:")
    print(f"    意图: {intent}")
    print(f"    值: {value}")
    print(f"    参数: {params}")
    print(f"    置信度: {confidence:.2f}")
    print(f"  期望结果:")
    print(f"    意图: {expected_intent}")
    print(f"    值: {expected_value}")
    print(f"    参数: {expected_params}")
    
    intent_match = intent == expected_intent
    value_match = value == expected_value
    params_match = params == expected_params
    
    if intent_match and value_match and params_match:
        print("  ✅ 通过")
        success_count += 1
    else:
        print("  ❌ 失败")
        failed_cases.append({
            'id': case_id,
            'input': user_input,
            'expected': expected,
            'actual': {
                'intent': intent,
                'value': value,
                'params': params,
                'confidence': confidence
            }
        })
        
        if not intent_match:
            print(f"    意图不匹配: {intent} != {expected_intent}")
        if not value_match:
            print(f"    值不匹配: {value} != {expected_value}")
        if not params_match:
            print(f"    参数不匹配: {params} != {expected_params}")

print(f"\n" + "=" * 80)
print(f"测试结果: {success_count}/{len(test_data['test_cases'])} 通过 ({success_count/len(test_data['test_cases'])*100:.1f}%)")

if failed_cases:
    print("\n失败用例详情:")
    for case in failed_cases:
        print(f"\n  [{case['id']}] {case['input']}")
        print(f"    期望: {case['expected']}")
        print(f"    实际: {case['actual']}")

print("=" * 80)
