date_dict = {}  # 创建一个空的字典

while True:
    date = input("请输入日期 (或输入 'exit' 退出): ")

    if date.lower() == "exit":
        break

    value = input("请输入要添加到列表的值: ")

    if date in date_dict:
        date_dict[date].append(value)
    else:
        date_dict[date] = [value]

print("最终字典内容:")
print(date_dict)
