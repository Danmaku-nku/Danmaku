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
            # "cookie": "SESSDATA=c8a19b78%2C1620925524%2C5d1eb*b1",
            "cookie": "SESSDATA=76e605be%2C1633682904%2C90639%2A41",
            "origin": "http://www.bilibili.com",
            # "referer": "http://www.bilibili.com/video/BV1os41127rm",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
            # 换成自己的ua就行
        }

        self.oid_list, self.pubdate = self.get_oidlist_pubdate()

    def get_oidlist_pubdate(self):
        bvid_url = 'http://api.bilibili.com/x/player/pagelist?bvid={0}'.format(self.bvid)
        response = requests.get(bvid_url, headers=self.headers)
        json_page_list = response.json()
        page_list = json_page_list['data']

        oid_list = []
        for i in range(len(page_list)):
            oid_list.append(re.search(r"'cid': (\d+)", str(page_list[i])).group(1))

        bvid_url = 'http://api.bilibili.com/x/web-interface/view?bvid={0}'.format(self.bvid)
        response = requests.get(bvid_url, headers=self.headers)
        pubdate = re.search(r'"pubdate":(\d+)', response.text).group(1)

        return oid_list, pubdate

    def get_dates(self, oid):
        date_stamp = int(self.pubdate)
        now = time.time()

        date_list = []
        for i in range(24):  # how many month
            date_month = datetime.datetime.fromtimestamp(date_stamp).strftime("%Y-%m")
            url = 'http://api.bilibili.com/x/v2/dm/history/index?type=1&oid={0}&month='.format(oid) + date_month

            response = requests.get(url=url, headers=self.headers)
            time.sleep(random.uniform(0.01, 0.02))

            json_data = response.json()
            if json_data['data'] is not None:
                date_list += json_data['data']

            date_stamp += 31 * 24 * 60 * 60
            if (date_stamp >= now):
                break

        return date_list

    def get_urls(self, page):
        oid = self.oid_list[page]

        date_list = self.get_dates(oid)

        url_list = []
        for i in range(len(date_list)):
            url = 'http://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={0}&date={1}'.format(oid,
                                                                                                       date_list[i])
            url_list.append(url)

        return url_list

    def get_danmu_seg(self):
        print('正在爬取视频{}的弹幕数据'.format(self.bvid))
        for page in range(5,len(self.oid_list)):
            urls = self.get_urls(page)

            os.makedirs("./seg/" + self.bvid + "/page_" + str(page))
            file_num = 0
            for i in range(len(urls)):
                if i % 5 == 0:
                    seg = requests.get(urls[i], headers=self.headers)

                    with open(r"./seg/" + self.bvid + "/page_" + str(page) + "/seg_" + str(file_num) + ".so",
                              "wb") as f:
                        f.write(seg.content)

                    print('链接{}的弹幕数据爬取成功'.format(urls[i]))
                    file_num += 1
                    time.sleep(random.uniform(3, 5))
                    if file_num % 10 == 0:
                        time.sleep(random.uniform(50, 60))

            time.sleep(random.uniform(50, 60))


if __name__ == '__main__':
    with open('videos.csv', 'r') as f:
        videos = list(csv.reader(f))[0]

    for i in range(len(videos)):
        danmu_seg = GetDanmuSeg(videos[i])
        danmu_seg.get_danmu_seg()
        get_danmu(videos[i], len(danmu_seg.oid_list))
