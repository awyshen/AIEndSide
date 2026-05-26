
import re
from .config import INTENT_KEYWORDS, REGEX_PATTERNS, INTENT_VALUE_MAP, CONFIG, MUSIC_APP_MAP, VIDEO_APP_MAP, PLACE_FILTER_WORDS

class RuleEngine:
    def __init__(self):
        self.intent_keywords = INTENT_KEYWORDS
        self.regex_patterns = REGEX_PATTERNS
        self.intent_value_map = INTENT_VALUE_MAP
        self.high_conf_threshold = CONFIG["confidence"]["high_confidence_threshold"]

        self.variety_shows = [
            "脱口秀大会", "奔跑吧兄弟", "国家宝藏", "乘风破浪的姐姐", 
            "一年一度喜剧大赛", "喜剧人单口季", "中国好声音", "快乐大本营",
            "极限挑战", "向往的生活", "创造营", "偶像练习生", "奔跑吧"
        ]

    def match_keywords(self, text):
        matched_intents = []

        for intent, config in self.intent_keywords.items():
            score = 0
            total_keywords = len(config["keywords"])
            matched_keywords = 0

            for keyword in config["keywords"]:
                if keyword.lower() in text.lower():
                    matched_keywords += 1
                    score += 3

            for pattern_type, patterns in config["patterns"].items():
                for pattern in patterns:
                    if pattern.lower() in text.lower():
                        score += 5
                        matched_keywords += 1

            if matched_keywords > 0:
                base_confidence = min(1.0, matched_keywords / total_keywords * 0.8)
                bonus = min(0.4, score / 15)
                confidence = min(1.0, base_confidence + bonus)
                matched_intents.append({
                    "intent": intent,
                    "confidence": confidence,
                    "matched_keywords": matched_keywords,
                    "score": score
                })

        matched_intents.sort(key=lambda x: (-x["score"], -x["confidence"]))
        return matched_intents

    def filter_place(self, place):
        for word in PLACE_FILTER_WORDS:
            place = place.replace(word, "")
        place = place.replace("到", "")
        place = place.replace("去", "")
        place = place.replace("来", "")
        return place.strip()

    def match_patterns(self, intent, text):
        params = {}
        value = self.intent_value_map.get(intent, "")
        pattern_matched = False

        if intent == "volume_control":
            if "调到最大" in text or "调最大" in text:
                params["volume"] = "100"
                pattern_matched = True
            elif "调到最小" in text or "调最小" in text:
                params["volume"] = "0"
                pattern_matched = True
            elif "取消静音" in text or "取消静音模式" in text:
                params["volume"] = "up"
                pattern_matched = True
            else:
                percent_match = re.search(self.regex_patterns["volume_percent"], text)
                if percent_match:
                    params["volume"] = percent_match.group(2)
                    pattern_matched = True
                else:
                    for pattern_type, patterns in self.intent_keywords[intent]["patterns"].items():
                        for pattern in patterns:
                            if pattern.lower() in text.lower():
                                pattern_matched = True
                                if pattern_type == "up":
                                    params["volume"] = "up"
                                elif pattern_type == "down":
                                    params["volume"] = "down"
                                elif pattern_type == "mute":
                                    params["volume"] = "mute"

        elif intent == "music_control":
            if "打开音乐播放器" in text or "关闭音乐播放器" in text or "启动音乐播放器" in text or "停止音乐播放器" in text:
                if "打开" in text or "启动" in text:
                    params["control"] = "open"
                else:
                    params["control"] = "close"
                params["app"] = MUSIC_APP_MAP["default"]
                pattern_matched = True
            else:
                matched_music_app = None
                for music_app in MUSIC_APP_MAP.keys():
                    if music_app.lower() in text.lower():
                        matched_music_app = music_app
                        break
                
                if matched_music_app:
                    if "打开" in text:
                        params["control"] = "open"
                    elif "关闭" in text:
                        params["control"] = "close"
                    else:
                        params["control"] = "play"
                    params["app"] = MUSIC_APP_MAP[matched_music_app]
                    pattern_matched = True

            if not pattern_matched:
                if "我想听" in text and "的歌" in text:
                    singer = text.replace("我想听", "").replace("的歌", "").strip()
                    if singer:
                        params["control"] = "play"
                        params["singer"] = singer
                        pattern_matched = True

            if not pattern_matched:
                if "放一首" in text and "的歌" in text:
                    singer = text.replace("放一首", "").replace("的歌", "").strip()
                    if singer:
                        params["control"] = "play"
                        params["singer"] = singer
                        pattern_matched = True

            if not pattern_matched:
                if "找一首" in text:
                    content = text.replace("找一首", "").strip()
                    if content:
                        params["control"] = "play"
                        if "的" in content:
                            parts = content.split("的", 1)
                            if len(parts) == 2:
                                params["singer"] = parts[0].strip()
                                params["song"] = parts[1].strip()
                            else:
                                params["song"] = content
                        else:
                            params["song"] = content
                        pattern_matched = True

            if not pattern_matched:
                for pattern in self.intent_keywords[intent]["patterns"].get("pause", []):
                    if pattern.lower() in text.lower():
                        params["control"] = "pause"
                        pattern_matched = True
                        break

            if not pattern_matched:
                for pattern in self.intent_keywords[intent]["patterns"].get("stop", []):
                    if pattern.lower() in text.lower():
                        params["control"] = "stop"
                        pattern_matched = True
                        break

            if not pattern_matched:
                if "不要播放" in text:
                    params["control"] = "stop"
                    pattern_matched = True

            if not pattern_matched:
                for pattern in self.intent_keywords[intent]["patterns"].get("previous", []):
                    if pattern.lower() in text.lower():
                        params["control"] = "previous"
                        pattern_matched = True
                        break

            if not pattern_matched:
                for pattern in self.intent_keywords[intent]["patterns"].get("next", []):
                    if pattern.lower() in text.lower():
                        params["control"] = "next"
                        pattern_matched = True
                        break

            if not pattern_matched:
                song_match = re.search(self.regex_patterns["play_song"], text)
                if song_match:
                    singer = song_match.group(1).strip()
                    song_name = song_match.group(2).strip()
                    if song_name and song_name != "歌" and song_name != "音乐":
                        if "上一首" not in song_name and "下一首" not in song_name:
                            params["control"] = "play"
                            params["singer"] = singer
                            params["song"] = song_name
                            pattern_matched = True
                    elif singer and "上一首" not in singer and "下一首" not in singer:
                        params["control"] = "play"
                        params["singer"] = singer
                        pattern_matched = True

            if not pattern_matched:
                song_direct_match = re.search(self.regex_patterns["play_song_direct"], text)
                if song_direct_match:
                    song_name = song_direct_match.group(2).strip()
                    if song_name and "播放" not in song_name and song_name != "歌曲" and song_name != "音乐" and song_name != "播放器":
                        if "上一首" not in song_name and "下一首" not in song_name:
                            params["control"] = "play"
                            params["song"] = song_name
                            pattern_matched = True

            if not pattern_matched:
                if "播放音乐" in text or "播放歌曲" in text or "播放歌" in text or "继续播放" in text:
                    params["control"] = "play"
                    pattern_matched = True

            if not pattern_matched:
                for pattern in self.intent_keywords[intent]["patterns"].get("play", []):
                    if pattern.lower() in text.lower():
                        params["control"] = "play"
                        pattern_matched = True
                        break

            if not pattern_matched:
                if "打开音乐" in text and not "音量" in text and not "声音" in text:
                    params["control"] = "open"
                    params["app"] = "default_music_app"
                    pattern_matched = True

        elif intent == "app_control":
            if "qq音乐" in text.lower() or "音乐播放器" in text or ("打开音乐" in text and not "音量" in text):
                pattern_matched = False
            else:
                open_match = re.search(self.regex_patterns["open_app"], text)
                close_match = re.search(self.regex_patterns["close_app"], text)

                start_match = re.search(r'启动(.+)', text)
                if start_match:
                    app_name = start_match.group(1).strip()
                    if app_name.lower() in [k.lower() for k in VIDEO_APP_MAP.keys()]:
                        for k in VIDEO_APP_MAP.keys():
                            if k.lower() == app_name.lower():
                                params["control"] = "open"
                                params["app"] = VIDEO_APP_MAP[k]
                                pattern_matched = True
                                break
                    elif app_name.lower() in [k.lower() for k in MUSIC_APP_MAP.keys()]:
                        for k in MUSIC_APP_MAP.keys():
                            if k.lower() == app_name.lower():
                                params["control"] = "open"
                                params["app"] = MUSIC_APP_MAP[k]
                                pattern_matched = True
                                break
                    else:
                        for k in VIDEO_APP_MAP.keys():
                            if k.lower() in app_name.lower():
                                params["control"] = "open"
                                params["app"] = VIDEO_APP_MAP[k]
                                pattern_matched = True
                                break
                        if not pattern_matched:
                            params["control"] = "open"
                            params["app"] = VIDEO_APP_MAP["default"]
                            pattern_matched = True
                elif open_match:
                    app_name = open_match.group(1).strip()
                    if app_name.lower() in [k.lower() for k in VIDEO_APP_MAP.keys()]:
                        for k in VIDEO_APP_MAP.keys():
                            if k.lower() == app_name.lower():
                                params["control"] = "open"
                                params["app"] = VIDEO_APP_MAP[k]
                                pattern_matched = True
                                break
                    elif app_name.lower() in [k.lower() for k in MUSIC_APP_MAP.keys()]:
                        for k in MUSIC_APP_MAP.keys():
                            if k.lower() == app_name.lower():
                                params["control"] = "open"
                                params["app"] = MUSIC_APP_MAP[k]
                                pattern_matched = True
                                break
                    elif app_name.lower() == "音乐播放器":
                        params["control"] = "open"
                        params["app"] = MUSIC_APP_MAP["default"]
                        pattern_matched = True
                    else:
                        for k in VIDEO_APP_MAP.keys():
                            if k.lower() in app_name.lower():
                                params["control"] = "open"
                                params["app"] = VIDEO_APP_MAP[k]
                                pattern_matched = True
                                break
                        if not pattern_matched:
                            params["control"] = "open"
                            params["app"] = VIDEO_APP_MAP["default"]
                            pattern_matched = True
                elif close_match:
                    app_name = close_match.group(1).strip()
                    if app_name.lower() in [k.lower() for k in VIDEO_APP_MAP.keys()]:
                        for k in VIDEO_APP_MAP.keys():
                            if k.lower() == app_name.lower():
                                params["control"] = "close"
                                params["app"] = VIDEO_APP_MAP[k]
                                pattern_matched = True
                                break
                    elif app_name.lower() in [k.lower() for k in MUSIC_APP_MAP.keys()]:
                        for k in MUSIC_APP_MAP.keys():
                            if k.lower() == app_name.lower():
                                params["control"] = "close"
                                params["app"] = MUSIC_APP_MAP[k]
                                pattern_matched = True
                                break
                    elif app_name.lower() == "音乐播放器":
                        params["control"] = "close"
                        params["app"] = MUSIC_APP_MAP["default"]
                        pattern_matched = True
                    else:
                        params["control"] = "close"
                        params["app"] = VIDEO_APP_MAP["default"]
                        pattern_matched = True
                else:
                    is_variety_show = False
                    program_name = ""
                    for show in self.variety_shows:
                        if show in text:
                            is_variety_show = True
                            start_idx = text.find(show)
                            program_name = text[start_idx:].strip()
                            break

                    if is_variety_show:
                        params["control"] = "play"
                        params["program"] = program_name
                        pattern_matched = True
                    elif "停止播放" in text:
                        params["control"] = "stop"
                        pattern_matched = True
                    elif "放本地" in text or "播本地" in text:
                        params["control"] = "open"
                        params["app"] = VIDEO_APP_MAP["default"]
                        pattern_matched = True
                    elif "电影" in text or "视频" in text or "节目" in text:
                        film_match = re.search(self.regex_patterns["play_film"], text)
                        if film_match:
                            params["control"] = "play"
                            content = film_match.group(2).strip()
                            if "电影" in text:
                                params["film"] = content
                            elif "视频" in text:
                                params["program"] = content
                            else:
                                params["program"] = content
                            pattern_matched = True
                    elif "我想看" in text:
                        program_name = text.replace("我想看", "").strip()
                        if program_name:
                            params["control"] = "play"
                            params["program"] = program_name
                            pattern_matched = True
                    else:
                        is_music_pattern = False
                        for pattern in ["上一首", "下一首", "上一曲", "下一曲"]:
                            if pattern in text:
                                is_music_pattern = True
                                break
                        
                        if not is_music_pattern:
                            film_match = re.search(self.regex_patterns["play_film"], text)
                            if film_match:
                                params["control"] = "play"
                                content = film_match.group(2).strip()
                                params["program"] = content
                                pattern_matched = True

        elif intent == "projector_control":
            for pattern_type, patterns in self.intent_keywords[intent]["patterns"].items():
                for pattern in patterns:
                    if pattern.lower() in text.lower():
                        pattern_matched = True
                        params["control"] = "open" if pattern_type == "open" else "close"

        elif intent == "robot_control":
            if "停止充电" in text:
                value = "charge"
                params["control"] = "stop"
                pattern_matched = True
            elif "不要去充电" in text:
                value = "charge"
                params["control"] = "stop"
                pattern_matched = True
            elif "不要去充电桩" in text:
                value = "charge"
                params["control"] = "stop"
                pattern_matched = True
            elif "不要去充电了" in text:
                value = "charge"
                params["control"] = "stop"
                pattern_matched = True
            elif "不要充电" in text:
                value = "charge"
                params["control"] = "stop"
                pattern_matched = True
            else:
                nav_match = re.search(self.regex_patterns["nav_place"], text)
                if nav_match:
                    place = nav_match.group(2).strip()
                    place = self.filter_place(place)
                    if "充电" in text or "充电桩" in text:
                        if "不要" in text or "取消" in text:
                            value = "charge"
                            params["control"] = "stop"
                        elif "停止" in text:
                            value = "charge"
                            params["control"] = "stop"
                        else:
                            value = "charge"
                            params["control"] = "start"
                    else:
                        if "不要" in text or "取消" in text:
                            params["control"] = "cancel"
                        else:
                            value = "nav"
                            params["place"] = place
                    pattern_matched = True
                elif "去" == text[0] and len(text) <= 5:
                    place = text.replace("去", "").strip()
                    if place and place not in ["充电", "充电桩"]:
                        value = "nav"
                        params["place"] = place
                        pattern_matched = True
                elif "导航到" in text:
                    place = text.replace("导航到", "").strip()
                    place = self.filter_place(place)
                    if place:
                        value = "nav"
                        params["place"] = place
                        pattern_matched = True
                else:
                    for pattern_type, patterns in self.intent_keywords[intent]["patterns"].items():
                        for pattern in patterns:
                            if pattern.lower() in text.lower():
                                pattern_matched = True
                                if pattern_type == "charge":
                                    if "不要" in text or "取消" in text:
                                        value = "charge"
                                        params["control"] = "stop"
                                    elif "停止" in text:
                                        value = "charge"
                                        params["control"] = "stop"
                                    else:
                                        value = "charge"
                                        params["control"] = "start"
                                elif pattern_type == "cancel":
                                    params["control"] = "cancel"

        elif intent == "assistant_control":
            for pattern_type, patterns in self.intent_keywords[intent]["patterns"].items():
                for pattern in patterns:
                    if pattern.lower() in text.lower():
                        pattern_matched = True
                        params["control"] = "sleep"

        elif intent == "chat":
            chat_keywords = ["你好", "您好", "嗨", "哈喽", "聊天", "聊一下", "说话", "谈谈", "交流", "天气", "笑话", "讲个", "什么", "能帮我", "做什么", "可以做什么", "能干什么", "帮助", "帮忙", "故事"]
            for keyword in chat_keywords:
                if keyword.lower() in text.lower():
                    pattern_matched = True
                    break
            if not pattern_matched:
                for pattern_type, patterns in self.intent_keywords[intent]["patterns"].items():
                    for pattern in patterns:
                        if pattern.lower() in text.lower():
                            pattern_matched = True

        return {"value": value, "params": params, "pattern_matched": pattern_matched}

    def recognize(self, text):
        matched_intents = self.match_keywords(text)

        intent = None
        confidence = 0.0
        score = 0

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
            ("不要去充电了", "robot_control", 0.9),
            ("不要去充电桩了", "robot_control", 0.9),
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

        special_case_matched = False
        for pattern, target_intent, default_confidence in special_cases:
            if ".*" in pattern:
                if re.search(pattern, text, re.IGNORECASE):
                    if pattern.startswith("播放.*?"):
                        is_variety_show = any(show.lower() in text.lower() for show in self.variety_shows)
                        if is_variety_show:
                            continue
                    intent = target_intent
                    confidence = default_confidence
                    score = 10
                    special_case_matched = True
                    break
            elif pattern.lower() in text.lower():
                intent = target_intent
                confidence = default_confidence
                score = 10
                special_case_matched = True
                break

        if not intent and matched_intents:
            top_intent = matched_intents[0]
            intent = top_intent["intent"]
            confidence = top_intent["confidence"]
            score = top_intent["score"]

        if not intent:
            for show in self.variety_shows:
                if show in text:
                    intent = "app_control"
                    confidence = 0.85
                    score = 10
                    break

        if not intent and "我想看" in text:
            intent = "app_control"
            confidence = 0.8

        if not intent:
            return None

        self.song_pattern_detected = False
        self.nav_pattern_detected = False
        result = self.match_patterns(intent, text)

        if not result["pattern_matched"]:
            return None

        final_confidence = confidence
        if result["pattern_matched"]:
            bonus = 0.1
            if self.song_pattern_detected:
                bonus = 0.25
            elif self.nav_pattern_detected:
                bonus = 0.15
            final_confidence = min(1.0, confidence + bonus)

        return {
            "intent": intent,
            "value": result["value"],
            "params": result["params"],
            "confidence": final_confidence,
            "method": "rule_based",
            "pattern_matched": result["pattern_matched"]
        }
