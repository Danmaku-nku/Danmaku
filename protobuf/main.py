import codecs
from danmu_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToJson,Parse
import json

DM = DmSegMobileReply()
with open("./seg.so","rb") as f:
    DM.ParseFromString(f.read())

with codecs.open("./seg.json","w","utf-8") as f:
    f.write(json.dumps(json.loads(MessageToJson(DM)),ensure_ascii=False))