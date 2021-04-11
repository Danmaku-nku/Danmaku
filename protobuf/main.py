
from danmu_pb2 import DmSegMobileReply
import google.protobuf.text_format as text_format
from google.protobuf.json_format import MessageToJson,Parse
import xml

DM = DmSegMobileReply()
with open("seg/seg.so","rb") as f:
    DM.ParseFromString(f.read())

for i in range(len(DM.elems)):
    print(DM.elems[i].progress/60000)
    print(DM.elems[i].content)
    print()

# print(text_format.MessageToString(DM.elems[0],as_utf8=True))