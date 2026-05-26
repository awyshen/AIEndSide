from intent_recognition import IntentRecognizer

print("=" * 60)
print("逐步调试 IntentRecognizer")
print("=" * 60)

recognizer = IntentRecognizer(use_llm=False, strict_mode=True, debug=True, enable_cache=False)

text = "不要去充电了"
print(f"\n输入文本: '{text}'")

print("\n1. 调用 preprocessor.process")
preprocessed = recognizer.preprocessor.process(text)
print(f"   cleaned_text: '{preprocessed['cleaned_text']}'")

print("\n2. 调用 split_multi_task")
tasks = recognizer.result_fusion.split_multi_task(preprocessed['cleaned_text'])
print(f"   tasks: {tasks}")

print("\n3. 调用 _recognize_single_task")
debug_info = {"original_input": text, "cleaned_text": preprocessed['cleaned_text'], "rule_result": None, "llm_result": None, "fusion_decision": ""}

task_text = tasks[0] if len(tasks) == 1 else preprocessed['cleaned_text']
print(f"   实际处理的文本: '{task_text}'")

rule_result = recognizer.rule_engine.recognize(task_text)
print(f"   rule_result: {rule_result}")

print("\n4. 调用 merge_results (with use_llm=False)")
fusion_result = recognizer.result_fusion.merge_results(rule_result, None)
print(f"   fusion_result: {fusion_result}")

print("\n5. 最终结果")
print(f"   intent: {fusion_result.get('intent')}")
print(f"   value: {fusion_result.get('value')}")
print(f"   params: {fusion_result.get('params')}")
print(f"   confidence: {fusion_result.get('confidence')}")
