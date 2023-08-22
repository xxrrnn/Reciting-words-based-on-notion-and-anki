with open("passage.txt", "rb") as file:
    lines = file.readlines()

decoded_lines = []

for line in lines:
    try:
        decoded_line = line.decode('utf-8')  # 尝试用utf-8解码
        decoded_lines.append(decoded_line)
    except UnicodeDecodeError:
        # 如果utf-8解码失败，则使用latin-1解码
        decoded_line = line.decode('latin-1', errors='replace')  # 替换无法解码的字符
        decoded_lines.append(decoded_line)
print(decoded_lines)
for decoded_line in decoded_lines:
    decoded_line = decoded_line.replace('\n','')
    decoded_line = decoded_line.replace('\r','')
    decoded_line = decoded_line.strip('*')
    decoded_line = decoded_line.strip()
    decoded_line = decoded_line.strip('#')
    decoded_line = decoded_line.strip()
    decoded_line = decoded_line.strip('*')
    decoded_line = decoded_line.strip()
    print(decoded_line)
