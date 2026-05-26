
CONFIG = {
    "llm": {
        "api_key": "EMPTY",
        "base_url": "http://10.61.85.20:32685/v1",
        "model_name": "qwen3.5-0.8b",
        # "model_name": "minicpm-1b",
        "timeout": 300
    },
    "confidence": {
        "threshold": 0.7,
        "high_confidence_threshold": 0.9,
        "rule_weight": 0.7,
        "llm_weight": 0.3
    },
    "performance": {
        "max_concurrent": 4,
        "cache_size": 1000
    }
}

INTENT_KEYWORDS = {
    "volume_control": {
        "keywords": ["音量", "声音", "静音", "大声", "小声", "响", "轻"],
        "patterns": {
            "up": ["调高", "调大", "大一点", "高一点", "大声点", "响一点", "大点", "有点小", "太小", "太轻"],
            "down": ["调低", "调小", "小一点", "低一点", "小声点", "轻一点", "小点", "太大", "太响"],
            "mute": ["静音", "关掉", "最低", "静音模式", "关闭声音"],
            "percent": ["调到", "设置为", "调整到", "设为"]
        }
    },
    "music_control": {
        "keywords": ["播放", "音乐", "歌曲", "歌", "暂停", "停止", "继续", "上一首", "下一首", "播放器", "放歌"],
        "patterns": {
            "previous": ["上一首", "上一个", "上一曲", "前一首", "上一首歌", "上首歌"],
            "next": ["下一首", "下一个", "下一曲", "下一首歌", "下首歌"],
            "pause": ["暂停", "暂停播放", "暂停歌曲", "暂停音乐", "暂停放歌"],
            "stop": ["停止", "停止播放", "不要播放", "停止放歌", "不要放歌"],
            "play": ["播放", "继续播放", "接着播放", "继续放歌", "放歌"],
            "open": ["打开", "开启"],
            "close": ["关闭", "关掉"]
        }
    },
    "app_control": {
        "keywords": ["视频", "电影", "播放", "打开", "关闭", "爱奇艺", "腾讯视频", "优酷", "节目", "本地"],
        "patterns": {
            "video": ["视频", "电影", "节目", "影视", "本地视频"],
            "play": ["播放", "放", "播"],
            "stop": ["停止", "停止播放"],
            "open": ["打开"],
            "close": ["关闭"]
        }
    },
    "projector_control": {
        "keywords": ["投影", "投影仪", "投影设备"],
        "patterns": {
            "open": ["打开", "开启", "打开投影", "把投影打开"],
            "close": ["关闭", "关掉", "关闭投影", "投影仪关了"]
        }
    },
    "robot_control": {
        "keywords": ["导航", "客厅", "充电", "充电桩", "回充", "回去", "前往", "来"],
        "patterns": {
            "nav": ["导航", "去", "到", "前往", "来"],
            "charge": ["充电", "回充", "充电桩", "去充电"],
            "cancel": ["取消", "不去", "停止", "不要"]
        }
    },
    "assistant_control": {
        "keywords": ["休息", "退下", "下去", "离开", "退出", "待机"],
        "patterns": {
            "sleep": ["休息", "退下", "下去", "离开", "退出", "待机"]
        }
    },
    "chat": {
        "keywords": ["聊", "聊天", "说话", "谈谈", "交流"],
        "patterns": {
            "chat": ["聊一下", "聊天", "说话", "谈谈", "交流"]
        }
    }
}

REGEX_PATTERNS = {
    "volume_percent": r'(音量|声音).*?(\d+)%?',
    "play_song": r'播放(.+?)的(.+)',
    "play_song_direct": r'播放(歌曲)?(.+)',
    "play_film": r'播放(电影|视频)?(.+)',
    "nav_place": r'(导航|去|到|前往|来)(.+)',
    "open_app": r'打开(.+)',
    "close_app": r'关闭(.+)'
}

MULTI_TASK_DELIMITERS = ["然后", "接着", "再", "同时", "和", ",", "并且"]

INTENT_VALUE_MAP = {
    "volume_control": "speaker",
    "music_control": "music_player",
    "app_control": "video_player",
    "projector_control": "projector",
    "robot_control": "nav",
    "assistant_control": "assistant",
    "chat": "chat"
}

MUSIC_APP_MAP = {
    "default": "default_music_app",
    "QQ音乐": "qq_music_app",
    "网易云音乐": "netease_music_app",
    "酷狗音乐": "kugou_music_app"
}

VIDEO_APP_MAP = {
    "default": "default_video_app",
    "爱奇艺": "iqiyi_video_app",
    "腾讯视频": "tencent_video_app",
    "优酷": "youku_video_app"
}

PLACE_FILTER_WORDS = ["吧", "去", "来", "了", "吧"]

INTENT_DESCRIPTIONS = {
    "volume_control": "音量控制：调整音量大小、静音等操作",
    "music_control": "音乐控制：播放、暂停、切歌、打开音乐播放器等",
    "app_control": "应用控制：播放视频、打开/关闭视频应用等",
    "projector_control": "投影仪控制：打开/关闭投影仪",
    "robot_control": "机器人控制：导航到指定地点、回充等",
    "assistant_control": "助手控制：让助手休眠、退出等",
    "chat": "聊天模式：进入对话聊天状态"
}
