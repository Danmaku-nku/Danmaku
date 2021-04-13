import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

with open("p_0.csv", encoding='utf-8') as result:
    time_list = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[0] = float(col[0])
        time_list.append(col[0])

num_for_second = []
for i in range(int(time_list[-1])+1):
        num_for_second.append(0)
for time in time_list:
        num_for_second[int(time)] += 1

fig = plt.figure(figsize=(20, 2))
ax = fig.add_subplot(111)


xnew = np.linspace(0, len(num_for_second), 300)
smooth = make_interp_spline(list(range(len(num_for_second))),num_for_second)(xnew)
ax.plot(xnew, smooth)
plt.savefig("result.png")
plt.show()
