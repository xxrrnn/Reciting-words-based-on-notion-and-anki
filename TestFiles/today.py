from datetime import datetime

# 获取当前日期
current_date = datetime.now().date()

# 将日期格式化为 "YYYY-MM-DD" 形式
formatted_date = current_date.strftime('%Y-%m-%d')

print(formatted_date)