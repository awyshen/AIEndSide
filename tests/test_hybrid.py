import sys
sys.path.insert(0, '/Users/terminus/Desktop/workspace/application/terminus/AIEndSide')

import json
from intent_recognition.main import IntentRecognizer

def run_test():
    with open('/Users/terminus/Desktop/workspace/application/terminus/AIEndSide/tests/test_cases.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=False, enable_cache=False)

    success = 0
    failed = []

    for case in test_data['test_cases']:
        try:
            result = recognizer.recognize(case['input'])
            expected = case['expected']
            
            intent_ok = result['intent'] == expected['intent']
            value_ok = result.get('value', '') == expected['value']
            params_ok = result.get('params', {}) == expected.get('params', {})
            
            if intent_ok and value_ok and params_ok:
                success += 1
            else:
                failed.append({
                    'input': case['input'],
                    'expected': expected,
                    'actual': {
                        'intent': result['intent'],
                        'value': result.get('value', ''),
                        'params': result.get('params', {}),
                        'source': result.get('source', 'unknown')
                    }
                })
        except Exception as e:
            failed.append({
                'input': case['input'],
                'expected': case['expected'],
                'actual': {'error': str(e)}
            })

    print(f'Total: {len(test_data["test_cases"])}')
    print(f'Success: {success}')
    print(f'Failed: {len(failed)}')
    print(f'Rate: {success/len(test_data["test_cases"])*100:.1f}%')

    if failed:
        print('\nFailed cases:')
        for f in failed:
            print(f"\nInput: {f['input']}")
            print(f"Expected: {f['expected']}")
            print(f"Actual: {f['actual']}")

if __name__ == '__main__':
    run_test()
