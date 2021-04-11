import random
import re
import time, datetime
import os

import csv
import requests

from get_danmus import *


class GetDanmuSeg:
    def __init__(self, bvid):
        self.bvid = bvid
        self.headers = {
            "cookie": "SESSDATA=c8a19b78%2C1620925524%2C5d1eb*b1",  # 爬取弹幕需要登陆，通过开发者模式获取你的登录cookie
            "origin": "https://www.bilibili.com",
            # "referer": "https://www.bilibili.com/video/BV1os41127rm",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
            # 换成自己的ua就行
        }

    def get_oid_pubdate(self):
        """
        通过视频编号获取用户的id->oid
        :param bvid: 视频编号
        :return: oid, duration, pubdate
        """
        bvid_url = 'https://api.bilibili.com/x/player/pagelist?bvid={0}'.format(self.bvid)
        response = requests.get(bvid_url, headers=self.headers)
        oid = re.search(r'"cid":(\d+)', response.text).group(1)

        bvid_url = 'https://api.bilibili.com/x/web-interface/view?bvid={0}'.format(self.bvid)
        response = requests.get(bvid_url, headers=self.headers)
        pubdate = re.search(r'"pubdate":(\d+)', response.text).group(1)

        return oid, pubdate

    def get_dates(self):
        """
        获取日期list
        :param oid: 用户id pudate: 视频长度
        :return: date_list列表
        """
        oid, pubdate = self.get_oid_pubdate()
        date_stamp = int(pubdate)
        now = time.time()

        date_list = []
        for i in range(3):  # for 3 month
            date_month = datetime.datetime.fromtimestamp(date_stamp).strftime("%Y-%m")
            url = 'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={0}&month='.format(oid) + date_month

            response = requests.get(url=url, headers=self.headers)
            json_data = response.json()
            date_list += json_data['data']

            date_stamp += 31 * 24 * 60 * 60
            if (date_stamp >= now):
                break

        return date_list


    def get_urls(self):
        """
        获取弹幕url
        :param oid: 用户id duration: 视频长度
        :return: 弹幕url_list列表
        """
        oid, pubdate = self.get_oid_pubdate()
        date_list = self.get_dates()

        url_list = []
        for i in range(len(date_list)):
            url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={0}&date={1}'.format(oid, date_list[i])
            url_list.append(url)

        return url_list

    def get_danmu_seg(self):
        """
        爬取并保存弹幕数据
        :param url
        :return:
        """
        print('正在爬取视频{}的弹幕数据'.format(self.bvid))
        urls = self.get_urls()
        os.makedirs("./seg/" + self.bvid)

        for i in range(len(urls)):
            seg = requests.get(urls[i], headers=self.headers)

            with open(r"./seg/" + self.bvid + "/seg_" + str(i) + ".so", "wb") as f:
                f.write(seg.content)

            print('链接{}的弹幕数据爬取成功'.format(urls[i]))

            if i % 10 == 0:
                time.sleep(random.uniform(3, 5))


if __name__ == '__main__':
    with open('videos.csv', 'r') as f:
        videos = list(csv.reader(f))[0]

    for i in range(len(videos)):
        danmu_seg = GetDanmuSeg(videos[i])
        print(danmu_seg.get_oid_pubdate())
        danmu_seg.get_danmu_seg()

    get_danmu(videos)

# print(time.time())


