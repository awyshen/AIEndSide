text = "不要去充电了"

print(f"输入文本: '{text}'")
print(f"长度: {len(text)}")
print(f"字符列表: {[c for c in text]}")
print()

test_patterns = [
    "停止充电",
    "不要去充电", 
    "不要去充电桩",
    "不要充电"
]

print("匹配测试:")
for pattern in test_patterns:
    if pattern in text:
        print(f"  '{pattern}' 在 '{text}' 中: 是")
    else:
        print(f"  '{pattern}' 在 '{text}' 中: 否")
        
print()
print("lower匹配测试:")
for pattern in test_patterns:
    if pattern.lower() in text.lower():
        print(f"  '{pattern.lower()}' 在 '{text.lower()}' 中: 是")
    else:
        print(f"  '{pattern.lower()}' 在 '{text.lower()}' 中: 否")
