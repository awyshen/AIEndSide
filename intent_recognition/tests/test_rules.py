
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from intent_recognition.rule_engine import RuleEngine

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()
    
    def test_volume_control_down(self):
        result = self.engine.recognize("音量调低一些")
        self.assertEqual(result["intent"], "volume_control")
        self.assertEqual(result["value"], "speaker")
        self.assertEqual(result["params"]["volume"], "down")
        self.assertGreater(result["confidence"], 0.5)
    
    def test_volume_control_up(self):
        result = self.engine.recognize("音量调高一些")
        self.assertEqual(result["intent"], "volume_control")
        self.assertEqual(result["value"], "speaker")
        self.assertEqual(result["params"]["volume"], "up")
    
    def test_volume_control_mute(self):
        result = self.engine.recognize("静音")
        self.assertEqual(result["intent"], "volume_control")
        self.assertEqual(result["value"], "speaker")
        self.assertEqual(result["params"]["volume"], "mute")
    
    def test_volume_control_percent(self):
        result = self.engine.recognize("音量调到70%")
        self.assertEqual(result["intent"], "volume_control")
        self.assertEqual(result["value"], "speaker")
        self.assertEqual(result["params"]["volume"], "70")
    
    def test_music_control_play_song(self):
        result = self.engine.recognize("播放蔡琴的渡口")
        self.assertEqual(result["intent"], "music_control")
        self.assertEqual(result["params"]["control"], "play")
        self.assertEqual(result["params"]["singer"], "蔡琴")
        self.assertEqual(result["params"]["song"], "渡口")
    
    def test_music_control_pause(self):
        result = self.engine.recognize("暂停播放音乐")
        self.assertEqual(result["intent"], "music_control")
        self.assertEqual(result["params"]["control"], "pause")
    
    def test_music_control_stop(self):
        result = self.engine.recognize("停止播放歌曲")
        self.assertEqual(result["intent"], "music_control")
        self.assertEqual(result["params"]["control"], "stop")
    
    def test_robot_control_nav(self):
        result = self.engine.recognize("导航到客厅")
        self.assertEqual(result["intent"], "robot_control")
        self.assertEqual(result["value"], "nav")
        self.assertEqual(result["params"]["place"], "客厅")
    
    def test_robot_control_charge(self):
        result = self.engine.recognize("回去充电")
        self.assertEqual(result["intent"], "robot_control")
        self.assertEqual(result["value"], "charge")
        self.assertEqual(result["params"]["control"], "start")
    
    def test_projector_control_open(self):
        result = self.engine.recognize("打开投影仪")
        self.assertEqual(result["intent"], "projector_control")
        self.assertEqual(result["value"], "projector")
        self.assertEqual(result["params"]["control"], "open")
    
    def test_projector_control_close(self):
        result = self.engine.recognize("关闭投影仪")
        self.assertEqual(result["intent"], "projector_control")
        self.assertEqual(result["params"]["control"], "close")
    
    def test_assistant_control_sleep(self):
        result = self.engine.recognize("休息一下")
        self.assertEqual(result["intent"], "assistant_control")
        self.assertEqual(result["params"]["control"], "sleep")
    
    def test_chat(self):
        result = self.engine.recognize("我们聊一下吧")
        self.assertEqual(result["intent"], "chat")
        self.assertEqual(result["value"], "chat")
    
    def test_app_control_open_iqiyi(self):
        result = self.engine.recognize("打开爱奇艺")
        self.assertEqual(result["intent"], "app_control")
        self.assertEqual(result["params"]["control"], "open")
        self.assertEqual(result["params"]["app"], "爱奇艺")
    
    def test_app_control_close_iqiyi(self):
        result = self.engine.recognize("关闭爱奇艺")
        self.assertEqual(result["intent"], "app_control")
        self.assertEqual(result["params"]["control"], "close")
        self.assertEqual(result["params"]["app"], "爱奇艺")

if __name__ == "__main__":
    unittest.main()
