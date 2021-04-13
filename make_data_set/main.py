import os
import h5py

video = "BV1oJ41137oE"
dataset_name = "dataset_googlenet_mine_our_planet"

time_list = []
for root, dirs, files in os.walk("../get_live_commenting/danmu/" + video):
    for page in range(len(files)):
        with open("../get_live_commenting/danmu/p_"+str(page)+".csv", encoding='utf-8') as result:
            header_line = result.readline()  # 读取并弹出第一行
            for line in result:
                col = line.split(',')  # 每行分隔为列表，好处理列格式
                col[0] = float(col[0])
                time_list.append(col[0])


before = h5py.File("../dataset/"+dataset_name+".h5", 'r')
f = h5py.File("../dataset/"+dataset_name+"_ready.h5", 'w')

