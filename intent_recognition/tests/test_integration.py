
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from intent_recognition.main import IntentRecognizer

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.recognizer = IntentRecognizer(use_llm=False)
    
    def test_single_task_volume(self):
        result = self.recognizer.recognize("声音调到70")
        self.assertEqual(result["query_type"], "single_task")
        self.assertEqual(result["intent"], "volume_control")
        self.assertEqual(result["value"], "speaker")
        self.assertEqual(result["params"]["volume"], "70")
    
    def test_single_task_music(self):
        result = self.recognizer.recognize("播放上一首音乐")
        self.assertEqual(result["query_type"], "single_task")
        self.assertEqual(result["intent"], "music_control")
        self.assertEqual(result["params"]["control"], "previous")
    
    def test_multi_task(self):
        result = self.recognizer.recognize("到客厅打开投影仪")
        self.assertEqual(result["query_type"], "multi_task")
        self.assertEqual(len(result["tasks"]), 2)
        
        intents = [task["intent"] for task in result["tasks"]]
        self.assertIn("robot_control", intents)
        self.assertIn("projector_control", intents)
    
    def test_chat_intent(self):
        result = self.recognizer.recognize("我们聊一下吧")
        self.assertEqual(result["intent"], "chat")
    
    def test_unknown_intent(self):
        result = self.recognizer.recognize("今天天气怎么样")
        self.assertEqual(result["intent"], "unknown")
        self.assertTrue(result.get("handover", False))
    
    def test_cache_enabled(self):
        result1 = self.recognizer.recognize("音量调高")
        result2 = self.recognizer.recognize("音量调高")
        self.assertTrue(result2.get("from_cache", False))
    
    def test_latency(self):
        result = self.recognizer.recognize("静音")
        self.assertLess(result["latency_ms"], 300)

if __name__ == "__main__":
    unittest.main()
