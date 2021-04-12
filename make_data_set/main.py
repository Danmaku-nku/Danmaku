from operator import itemgetter

before = open("test.csv", encoding='utf-8')
after = open("out.csv", "w", encoding='utf-8')

order_in = []
header_line = before.readline()  # 读取并弹出第一行
for line in before:
    col = line.split(',')  # 每行分隔为列表，好处理列格式
    col[0] = float(col[0])
    col[5] = int(col[5])
    order_in.append(col)  # 嵌套列表table[[8,8][*,*],...]

order_idstr = sorted(order_in, key=itemgetter(5))

last = 0
order_idstr_clean = []
for line in order_idstr:
    if line[5] != last:
        order_idstr_clean.append(line)
        last = line[5]

order_progress = sorted(order_idstr_clean, key=itemgetter(0))

after.write(header_line + '\t')
for row in order_progress:  # 遍历读取排序后的嵌套列表
    temp = str(row[0])
    for x in range(1,len(row)):
        temp += ","+ str(row[x])
    after.write("\t".join(temp) + '\n')

before.close()
after.close()
