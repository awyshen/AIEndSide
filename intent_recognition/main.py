import time
import hashlib
from .preprocessor import TextPreprocessor
from .rule_engine import RuleEngine
from .llm_client import QwenAPI
from .result_fusion import ResultFusion
from .config import CONFIG

class IntentRecognizer:
    def __init__(self, use_llm=True, enable_cache=True, strict_mode=True, debug=False):
        self.preprocessor = TextPreprocessor()
        self.rule_engine = RuleEngine()
        self.llm_client = QwenAPI() if use_llm else None
        self.result_fusion = ResultFusion()
        self.use_llm = use_llm
        self.enable_cache = enable_cache
        self.strict_mode = strict_mode
        self.debug = debug
        self.cache = {}
        self.cache_size = CONFIG["performance"]["cache_size"]
        self.threshold = CONFIG["confidence"]["threshold"]

    def _get_cache_key(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def _add_to_cache(self, text, result):
        if self.enable_cache:
            key = self._get_cache_key(text)
            if len(self.cache) >= self.cache_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
            self.cache[key] = {"result": result, "timestamp": time.time()}

    def _get_from_cache(self, text):
        if self.enable_cache:
            key = self._get_cache_key(text)
            if key in self.cache:
                return self.cache[key]["result"]
        return None

    def recognize(self, user_input):
        start_time = time.time()

        cache_result = self._get_from_cache(user_input)
        if cache_result:
            cache_result["from_cache"] = True
            cache_result["latency_ms"] = int((time.time() - start_time) * 1000)
            return cache_result

        preprocessed = self.preprocessor.process(user_input)
        cleaned_text = preprocessed["cleaned_text"]

        debug_info = {
            "original_input": user_input,
            "cleaned_text": cleaned_text,
            "rule_result": None,
            "llm_result": None,
            "fusion_decision": ""
        }

        if not cleaned_text or len(cleaned_text) < 2:
            result = {
                "query_type": "unknown",
                "intent": "unknown",
                "value": "",
                "params": {},
                "confidence": 0.0,
                "reason": "输入为空或过短",
                "handover": True,
                "source": "preprocessor",
                "latency_ms": int((time.time() - start_time) * 1000)
            }
            if self.debug:
                result["debug"] = debug_info
            self._add_to_cache(user_input, result)
            return result

        tasks = self.result_fusion.split_multi_task(cleaned_text)

        if len(tasks) > 1:
            task_results = []
            for task in tasks:
                task_result = self._recognize_single_task(task, debug_info)
                task_results.append(task_result)
            final_result = self.result_fusion.combine_tasks(task_results)
        else:
            final_result = self._recognize_single_task(cleaned_text, debug_info)
            if final_result.get("intent") != "unknown":
                final_result["query_type"] = "single_task"
                final_result["tasks"] = [final_result.copy()]

        final_result["latency_ms"] = int((time.time() - start_time) * 1000)

        if self.debug:
            final_result["debug"] = debug_info

        self._add_to_cache(user_input, final_result)

        return final_result

    def _recognize_single_task(self, text, debug_info=None):
        rule_result = self.rule_engine.recognize(text)

        if debug_info is not None:
            debug_info["rule_result"] = rule_result

        if not self.use_llm:
            if rule_result and rule_result.get("confidence", 0) >= self.threshold:
                rule_result["source"] = "rule_based"
                return rule_result
            else:
                return {
                    "intent": "unknown",
                    "value": "",
                    "params": {},
                    "confidence": 0.0,
                    "reason": "规则置信度不足",
                    "handover": True,
                    "source": "rule_engine"
                }

        llm_result = None
        try:
            llm_result = self.llm_client.classify_intent(text)
        except Exception as e:
            llm_result = {"intent": "unknown", "confidence": 0.0, "error": str(e)}

        if debug_info is not None:
            debug_info["llm_result"] = llm_result

        fusion_result = self.result_fusion.merge_results(rule_result, llm_result)

        if fusion_result.get("intent") != "unknown":
            if fusion_result.get("method") == "hybrid_confirmed":
                fusion_result["source"] = "hybrid_confirmed"
                if debug_info is not None:
                    debug_info["fusion_decision"] = "规则+LLM混合确认"
            elif fusion_result.get("confidence", 0) >= CONFIG["confidence"]["high_confidence_threshold"]:
                fusion_result["source"] = "rule_based_high_confidence"
                if debug_info is not None:
                    debug_info["fusion_decision"] = "规则高置信度直接返回"
            elif llm_result and llm_result.get("intent") == fusion_result.get("intent"):
                fusion_result["source"] = "llm_fallback"
                if debug_info is not None:
                    debug_info["fusion_decision"] = "LLM兜底"
            else:
                fusion_result["source"] = "rule_based"
                if debug_info is not None:
                    debug_info["fusion_decision"] = "规则匹配"
        else:
            fusion_result["source"] = "unknown"

        return fusion_result

    def batch_recognize(self, inputs):
        results = []
        for input_text in inputs:
            results.append(self.recognize(input_text))
        return results

if __name__ == "__main__":
    print("=" * 70)
    print("意图识别系统验证测试")
    print("策略: 规则优先(高准确率) + LLM保守兜底(宁错过不错判)")
    print("=" * 70)

    test_cases = [
        "声音调到70",
        "到客厅打开投影仪",
        "播放蔡琴的渡口",
        "我们聊一下吧",
        "调高音量",
        "静音",
        "播放上一首",
        "暂停播放音乐",
        "打开爱奇艺",
        "导航到客厅",
        "回去充电",
        "休息一下",
        "今天天气怎么样",
        "帮我搜索一下",
        "随便说说"
    ]

    print("\n--- 测试: 规则+LLM混合模式 ---")
    recognizer = IntentRecognizer(use_llm=True, strict_mode=True, debug=False, enable_cache=False)
    for test in test_cases:
        result = recognizer.recognize(test)
        status = "✓" if result["intent"] != "unknown" else "✗"
        source = result.get("source", "unknown")
        print(f"{status} [{source}] {test:<15} → {result['intent']} {result.get('value', None)} params: {result.get('params', {})} (置信度: {result.get('confidence', 0):.2f})")
