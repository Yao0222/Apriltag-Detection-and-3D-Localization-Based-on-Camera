import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

# 初始化X, Y, Z坐标的列表
x_data = []
y_data = []
z_data = []

# 读取CSV文件
with open('detection_results.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)  # 跳过标题行
    for row in plots:
        # 移除方括号，并分割字符串以获取坐标
        tag_position = row[2].strip('[]').split()
        # 将字符串转换为浮点数并添加到列表中
        x_data.append(float(tag_position[0]))
        y_data.append(float(tag_position[1]))
        z_data.append(float(tag_position[2]))

# 绘制3D轨迹
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_data, y_data, z_data, label='Tag 3D Trajectory', marker='o')

# 设置轴标签
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.legend()

# 显示图形
# plt.show()
plt.savefig('3d.png')