import random
import re
import time
import os

import csv
import requests

from get_danmus import *


class GetDanmuSeg:
    def __init__(self, bvid):
        self.bvid = bvid
        self.headers = {
            "cookie": "c8a19b78%2C1620925524%2C5d1eb*b1", # 爬取弹幕需要登陆，通过开发者模式获取你的登录cookie
            "origin": "https://www.bilibili.com",
            # "referer": "https://www.bilibili.com/video/BV1os41127rm",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36" # 换成自己的ua就行
        }


    def get_oid_duration(self):
        """
        通过视频编号获取用户的id->oid
        :param bvid: 视频编号
        :return: oid, duration
        """
        bvid_url = 'https://api.bilibili.com/x/player/pagelist?bvid={0}'.format(self.bvid)
        response = requests.get(bvid_url, headers=self.headers)
        oid = re.search(r'"cid":(\d+)', response.text).group(1)
        duration = re.search(r'"duration":(\d+)', response.text).group(1)
        return oid, duration


    def get_urls(self):
        """
        获取弹幕url
        :param oid: 用户id duration: 视频长度
        :return: 弹幕url_list列表
        """
        oid, duration = self.get_oid_duration()

        url_list = []
        for i in range(int(int(duration)/360)+1):
            url = 'http://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid={0}&segment_index='.format(oid) + str(i+1)
            url_list.append(url)

        return url_list


    def get_danmu_seg(self):
        """
        爬取并保存弹幕数据
        :param url
        :return:
        """
        print('正在爬取视频编号为{}的弹幕数据'.format(self.bvid))
        urls = self.get_urls()
        os.makedirs("./seg/" + self.bvid)

        for i in range(len(urls)):
            seg = requests.get(urls[i], headers=self.headers)

            with open(r"./seg/"+self.bvid+"/seg_"+str(i)+".so", "wb") as f:
                f.write(seg.content)

            print('链接{}的弹幕数据爬取成功'.format(urls[i]))

            if i % 10 == 0:
                time.sleep(random.uniform(3, 5))


if __name__ == '__main__':
    with open('videos.csv', 'r') as f:
        videos = list(csv.reader(f))[0]

    for i in range(len(videos)):
        danmu_seg = GetDanmuSeg(videos[i])
        danmu_seg.get_danmu_seg()

    get_danmu(videos)

# print(text_format.MessageToString(danmaku_seg.elems[0],as_utf8=True))