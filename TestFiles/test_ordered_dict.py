from datetime import datetime
from collections import OrderedDict

# 示例数据
data_dict = {
    '2023-08-25': 15,
    '2023-08-27': 30,
    '2023-08-26': 20,
    '2023-08-28': 10
}

# 将日期字符串转换为datetime.date对象并排序
sorted_data = OrderedDict(sorted(data_dict.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d')))

# 打印排序后的数据
for date, value in sorted_data.items():
    print(f"Date: {date}, Value: {value}")
