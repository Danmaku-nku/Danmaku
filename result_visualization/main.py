import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

danmu_list_path = "../get_live_commenting/danmu/BV1Ux411S7oh/p_1.csv"
old_sub_list_path = "../old_results/HSA-rnn/sub_list_HSA_8.csv"
danmu_sub_list_path = "../danmu_summary/sub_list.csv"

with open(old_sub_list_path, encoding='utf-8') as result:
    old_starts = []
    old_ends = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[1] = float(col[1])
        col[2] = float(col[2])

        old_starts.append(col[1])
        old_ends.append(col[2])

with open(danmu_sub_list_path, encoding='utf-8') as result:
    danmu_starts = []
    danmu_ends = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[1] = float(col[1])
        col[2] = float(col[2])

        danmu_starts.append(col[1])
        danmu_ends.append(col[2])

with open(danmu_list_path, encoding='utf-8') as result:
    time_list = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        time_list.append(float(col[0])/(47*60+53)*(49*60+57))

danmu_num_for_second = []
is_summary_old_for_second = []
is_summary_danmu_for_second = []
for i in range(int(time_list[-1])+1):
        danmu_num_for_second.append(0)
        is_summary_old_for_second.append(0)
        is_summary_danmu_for_second.append(0)

for time in time_list:
        danmu_num_for_second[int(time)] += 1
for shot_num in range(len(old_starts)):
    for  second_pointer in range(int(old_starts[shot_num]), int(old_ends[shot_num])+1):
        is_summary_old_for_second[second_pointer] += max(danmu_num_for_second)
for shot_num in range(len(danmu_starts)):
    for  second_pointer in range(int(danmu_starts[shot_num]), int(danmu_ends[shot_num])+1):
        is_summary_danmu_for_second[second_pointer] += max(danmu_num_for_second)

plt.figure(figsize=(50,1), dpi=400)

plt.plot(danmu_num_for_second, color='greenyellow', label='danmu_num', linewidth=0.5)
plt.plot(is_summary_old_for_second, color='red', label='old_summary', linewidth=1)
plt.plot(is_summary_danmu_for_second, color='green', label='danmu_summary', linewidth=1)

plt.legend() # 显示图例
plt.savefig("result.png")
plt.show()


# fig = plt.figure(figsize=(20, 2))
# ax = fig.add_subplot(111)
#
# xnew1 = np.linspace(0, len(danmu_num_for_second), 300)
# smooth1 = make_interp_spline(list(range(len(danmu_num_for_second))),danmu_num_for_second)(xnew1)
# xnew2 = np.linspace(0, len(is_summary_old_for_second), 300)
# smooth2 = make_interp_spline(list(range(len(is_summary_old_for_second))),is_summary_old_for_second)(xnew2)
#
# ax.plot(xnew1, smooth1, color='red', label='danmu_num')
# ax.plot(xnew2, smooth2, color='blue', label='old_summary')

# plt.plot(danmu_num_for_second[0:int(len(danmu_num_for_second)/5)], color='red', label='danmu_num')
# plt.plot(is_summary_old_for_second[0:int(len(danmu_num_for_second)/5)], color='blue', label='old_summary')
