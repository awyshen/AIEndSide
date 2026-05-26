
from .config import CONFIG, MULTI_TASK_DELIMITERS

class ResultFusion:
    def __init__(self):
        self.threshold = CONFIG["confidence"]["threshold"]
        self.high_threshold = CONFIG["confidence"]["high_confidence_threshold"]
        self.rule_weight = CONFIG["confidence"]["rule_weight"]
        self.llm_weight = CONFIG["confidence"]["llm_weight"]

    def merge_results(self, rule_result, llm_result):
        if not rule_result and not llm_result:
            return self._create_unknown_result("无法识别意图")

        if rule_result and not llm_result:
            rule_confidence = rule_result.get("confidence", 0)
            if rule_confidence >= self.threshold:
                return rule_result
            return self._create_unknown_result("规则置信度不足")

        if llm_result and not rule_result:
            llm_confidence = llm_result.get("confidence", 0)
            if llm_confidence >= 0.8:
                return llm_result
            return self._create_unknown_result("LLM置信度不足")

        rule_confidence = rule_result.get("confidence", 0)

        if rule_confidence >= self.high_threshold:
            return rule_result

        if rule_confidence >= self.threshold:
            llm_confidence = llm_result.get("confidence", 0)
            if llm_confidence >= 0.85 and llm_result.get("intent") == rule_result.get("intent"):
                combined_confidence = (rule_confidence * self.rule_weight + llm_confidence * self.llm_weight)
                result = rule_result.copy()
                result["confidence"] = combined_confidence
                result["method"] = "hybrid_confirmed"
                return result
            return rule_result

        llm_confidence = llm_result.get("confidence", 0)
        if llm_confidence >= 0.8:
            return llm_result

        return self._create_unknown_result("规则和LLM置信度均不足")

    def _create_unknown_result(self, reason):
        return {
            "query_type": "unknown",
            "intent": "unknown",
            "value": "",
            "params": {},
            "confidence": 0.0,
            "reason": reason,
            "handover": True
        }

    def split_multi_task(self, text):
        exclusion_patterns = [
            "打开音乐播放器",
            "关闭音乐播放器",
            "启动音乐播放器",
            "停止音乐播放器",
            "打开QQ音乐",
            "关闭QQ音乐",
            "不要去充电",
            "不要去充电桩",
            "不要充电",
            "停止充电",
            "回去充电",
        ]

        for pattern in exclusion_patterns:
            if pattern in text:
                prefix = text[:text.find(pattern)]
                suffix = text[text.find(pattern) + len(pattern):]

                tasks = []
                if prefix.strip() and len(prefix.strip()) >= 2:
                    tasks.append(prefix.strip())

                tasks.append(pattern)

                if suffix.strip() and len(suffix.strip()) >= 2:
                    tasks.append(suffix.strip())

                return tasks if len(tasks) > 1 else [text]

        action_patterns = [
            ("导航到", 3),
            ("导航", 2),
            ("打开", 2),
            ("关闭", 2),
            ("播放", 2),
            ("暂停", 2),
            ("停止", 2),
            ("调高", 2),
            ("调低", 2),
            ("充电", 2),
            ("回充", 2),
            ("到", 1),
            ("去", 1),
        ]

        action_positions = []
        for pattern, length in action_patterns:
            start = 0
            while True:
                idx = text.find(pattern, start)
                if idx == -1:
                    break
                if idx == 0 or text[idx-1] not in "打开关闭播放暂停停止调":
                    action_positions.append((idx, pattern, length))
                start = idx + length

        action_positions.sort(key=lambda x: x[0])

        unique_positions = []
        last_end = -1
        for idx, pattern, length in action_positions:
            if idx >= last_end:
                unique_positions.append((idx, pattern, length))
                last_end = idx + length

        if len(unique_positions) >= 2:
            tasks = []
            prev_idx = 0
            for idx, pattern, length in unique_positions:
                if idx > prev_idx:
                    task_part = text[prev_idx:idx].strip()
                    if len(task_part) >= 2:
                        tasks.append(task_part)
                prev_idx = idx

            final_task = text[prev_idx:].strip()
            if len(final_task) >= 2:
                tasks.append(final_task)

            if len(tasks) >= 2:
                return tasks

        tasks = []
        current_task = text

        for delimiter in MULTI_TASK_DELIMITERS:
            if delimiter in current_task:
                parts = current_task.split(delimiter)
                valid_parts = []
                for part in parts:
                    part = part.strip()
                    if part and len(part) >= 2:
                        valid_parts.append(part)
                if len(valid_parts) >= 2:
                    tasks = valid_parts
                    break

        if not tasks or len(tasks) == 1:
            split_patterns = [
                (["到", "去", "导航"], ["打开", "关闭", "播放", "暂停", "停止"]),
                (["调高", "调低", "音量"], ["打开", "关闭", "播放", "暂停", "停止"]),
                (["充电", "回充"], ["打开", "关闭", "播放", "暂停", "停止"]),
                (["关闭"], ["休息", "退下", "充电"]),
                (["打开"], ["播放", "暂停", "停止", "关闭"])
            ]

            for first_group, second_group in split_patterns:
                for first_pattern in first_group:
                    idx = text.find(first_pattern)
                    if idx == -1:
                        continue
                    for second_pattern in second_group:
                        idx2 = text.find(second_pattern)
                        if idx2 != -1 and idx < idx2 and idx2 - idx >= 2:
                            part1 = text[:idx2].strip()
                            part2 = text[idx2:].strip()
                            if len(part1) >= 2 and len(part2) >= 2:
                                return [part1, part2]

        if not tasks:
            tasks = [text]

        return tasks

    def combine_tasks(self, task_results):
        if len(task_results) == 1:
            result = task_results[0]
            if result.get("intent") == "unknown":
                return result
            result["query_type"] = "single_task"
            result["tasks"] = [result.copy()]
            return result

        valid_tasks = [t for t in task_results if t.get("intent") != "unknown" and t.get("confidence", 0) >= self.threshold]

        if len(valid_tasks) == 0:
            return self._create_unknown_result("所有任务均无法识别")

        if len(valid_tasks) == 1:
            result = valid_tasks[0]
            result["query_type"] = "single_task"
            result["tasks"] = [result.copy()]
            return result

        return {
            "query_type": "multi_task",
            "intent": "multi_task",
            "value": "multi",
            "params": {},
            "tasks": valid_tasks,
            "confidence": min(t.get("confidence", 0) for t in valid_tasks),
            "source": "rule_based_high_confidence"
        }
