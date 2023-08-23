import re

text = "这是一段话，用于示范分割功能. 另一段话则使用了另一种分割方式.\" 最后一段话使用了另外的分割符号. "
split_text = text.split(". ") #+ text.split(".) ")+ text.split(".\" ")

print(split_text)

import re

text = "ENDS OF THOUSANDS of [Ukrainian soldiers](https://www.economist.com/1843/2023/02/22/the-secret-diary-of-a-ukrainian-soldier-death-and-drones-on-the-eastern-front) are readying for action; checking their kit, writing what might be their last letters."

# 匹配 [] 中的内容并保留，删除 () 中的内容
processed_text = re.sub(r'\((.*?)\)|\[([^\]]+)\]', lambda m: m.group(2) if m.group(2) else "", text)

print(processed_text)
