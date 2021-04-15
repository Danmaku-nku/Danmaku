import os
import csv

from danmu_pb2 import DmSegMobileReply
from operator import itemgetter


def get_danmu(video, page_num):
    # os.makedirs("./danmu/" + video)
    for page in range(page_num):
        print("writing danmu for " + str(video) + " p" + str(page))

        with  open("./danmu/" + video + "/p_" + str(page) + ".csv", "w+", newline='', encoding='utf-8') as f_write:
            writer = csv.writer(f_write)
            writer.writerow(["progress", "content", "ctime", "midHash", "weight", "idStr"])
            order_in = []

            for root, dirs, files in os.walk("./seg/" + video + "/page_" + str(page)):
                for seg_file_num in range(len(files)):
                    # print(seg_file_num)
                    DM = DmSegMobileReply()
                    with open("./seg/" + video + "/page_" + str(page) + "/" + "seg_" + str(seg_file_num) + ".so",
                              "rb") as f:
                        DM.ParseFromString(f.read())

                        for i in range(len(DM.elems)):
                            order_in.append([DM.elems[i].progress / 1000, DM.elems[i].content, DM.elems[i].ctime,
                                             DM.elems[i].midHash, DM.elems[i].weight, str(DM.elems[i].idStr)])

            order_idstr = sorted(order_in, key=itemgetter(5))

            last = 0
            order_idstr_clean = []
            for line in order_idstr:
                if line[5] != last:
                    order_idstr_clean.append(line)
                    last = line[5]

            order_progress = sorted(order_idstr_clean, key=itemgetter(0))

            for row in order_progress:  
                writer.writerow(row)
