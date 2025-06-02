import re

text1 = "[5월16일] 중동의 문을 연 미국의 무기는 AI...중국까지 단절 시키나"
cleaned1 = re.sub(r"\[.*?]\s*", "", text1.strip())
print(f"==={cleaned1}===")

text2 = "[5월14일] AI가 던져준 새로운 '실존적' 문제...인간은 무엇을 해야 하나"
cleaned2 = re.sub(r"\[.*?]\s*", "", text2.strip())
print(f"==={cleaned2}===")

text3 = "[5월13일] 알트먼이 오픈AI 경영에서 손을 떼려는 이유는...우주 확장이 목표"
cleaned3 = re.sub(r"\[.*?]\s*", "", text3.strip())
print(f"==={cleaned3}===")

text4 = "[5월15일] MS가 해고한 인원 40%는 '코더'...인간은 코딩 AI 이상 능력 필요"
cleaned4 = re.sub(r"\[.*?]\s*", "", text4.strip())
print(f"==={cleaned4}===")
