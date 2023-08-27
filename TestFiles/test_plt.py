import matplotlib.pyplot as plt

# 示例数据
categories_left = ['Category A', 'Category B']
values_left_row1 = [30, 50]
values_left_row2 = [40, 20]

categories_right = ['Category X', 'Category Y']
values_right = [70, 30]

# 创建画布和子图
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# 左上角子图：第一行的柱状图
axs[0, 0].bar(categories_left, values_left_row1)
axs[0, 0].set_title('Upper Left Bar Chart')
axs[0, 0].set_xlabel('Categories')
axs[0, 0].set_ylabel('Values')
axs[0, 0].grid(True)
axs[0, 0].set_xticks(range(len(categories_left)))
axs[0, 0].text(0.5, 35, 'Custom Text', fontsize=12, color='blue')

# 右上角子图：第二行的柱状图
axs[0, 1].bar(categories_left, values_left_row2)
axs[0, 1].set_title('Upper Right Bar Chart')
axs[0, 1].set_xlabel('Categories')
axs[0, 1].set_ylabel('Values')
axs[0, 1].grid(True)
axs[0, 1].set_xticks(range(len(categories_left)))
axs[0, 1].text(0.5, 30, 'Another Text', fontsize=12, color='red')

# 左下角子图：饼状图
axs[1, 0].pie(values_right, labels=categories_right, autopct='%1.1f%%', startangle=90)
axs[1, 0].set_title('Lower Left Pie Chart')
axs[1, 0].text(0.5, 0.5, 'Pie Chart Text', fontsize=12, color='green', transform=axs[1, 0].transAxes)

# 右下角子图：空白，不画图
axs[1, 1].axis('off')

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()
