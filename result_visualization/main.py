import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

danmu_list_path = "../get_live_commenting/danmu/BV1Ux411S7oh/p_1.csv"
sub_list_path = "../old_results/HSA-rnn/sub_list_HSA_8.csv"

with open(sub_list_path, encoding='utf-8') as result:
    starts = []
    ends = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[1] = float(col[1])
        col[2] = float(col[2])

        starts.append(col[1])
        ends.append(col[2])

with open(danmu_list_path, encoding='utf-8') as result:
    time_list = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[0] = float(col[0])
        time_list.append(col[0])

danmu_num_for_second = []
is_summary_old_for_second = []
for i in range(int(time_list[-1])+1):
        danmu_num_for_second.append(0)
        is_summary_old_for_second.append(0)

for time in time_list:
        danmu_num_for_second[int(time)] += 1
for shot_num in range(len(starts)):
    for  second_pointer in range(int(starts[shot_num]), int(ends[shot_num])+1):
        is_summary_old_for_second[second_pointer] += max(danmu_num_for_second)



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

plt.figure(figsize=(50,1), dpi=500)

plt.plot(danmu_num_for_second, color='red', label='danmu_num', linewidth=0.5)
plt.plot(is_summary_old_for_second, color='blue', label='old_summary', linewidth=1)

plt.legend() # 显示图例
plt.savefig("result.png")
plt.show()
