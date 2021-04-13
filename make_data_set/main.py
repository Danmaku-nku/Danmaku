
with open("p_0.csv", encoding='utf-8') as result:
    time_list = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[0] = float(col[0])
        time_list.append(col[0])