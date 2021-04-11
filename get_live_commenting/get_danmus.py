import os
import csv

from danmu_pb2 import DmSegMobileReply
import google.protobuf.text_format as text_format
from google.protobuf.json_format import MessageToJson, Parse


def get_danmu(videos):
    for video in videos:
        print("writing danmu for " + video)
        with open("./danmu/" + video + ".csv", "w", newline='', encoding='utf-8') as f_write:
            writer = csv.writer(f_write)

            for root, dirs, files in os.walk("./seg/" + video):
                for seg_file in files:
                    DM = DmSegMobileReply()
                    with open("./seg/" + video + "/" + seg_file, "rb") as f:
                        DM.ParseFromString(f.read())

                        for i in range(len(DM.elems)):
                            writer.writerow([DM.elems[i].progress / 1000, DM.elems[i].content])

# print(text_format.MessageToString(DM.elems[0],as_utf8=True))
