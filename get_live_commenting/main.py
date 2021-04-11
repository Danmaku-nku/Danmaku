# import random
# import re
# import time
#
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# #from spider.bullet_chat.ua_choose import get_ua  # 随机获取ua函数
#
#
# class BulletChat:
#     def __init__(self, bvid, start_time='2020-10-13', end_time='2020-10-14'):
#         self.bvid = bvid
#         self.start_time = start_time
#         self.end_time = end_time
#         self.headers = {
#             "cookie": "c8a19b78%2C1620925524%2C5d1eb*b1",  # 爬取弹幕需要登陆，通过开发者模式获取你的登录cookie
#             "origin": "https://www.bilibili.com",
#             # "referer": "https://www.bilibili.com/video/BV1os41127rm",
#             "sec-fetch-dest": "empty",
#             "sec-fetch-mode": "cors",
#             "sec-fetch-site": "same-site",
#             "user-agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36" # 换成自己的ua就行
#         }
#         # 初始化直接生成一个csv文件
#         pd.Series().to_csv(self.bvid + '.csv', header=False)
#
#     def get_oid(self):
#         """
#         通过视频编号获取用户的id->oid
#         :param bvid: 视频编号
#         :return: oid
#         """
#         bvid_url = 'https://api.bilibili.com/x/player/pagelist?bvid={0}'.format(self.bvid)
#         response = requests.get(bvid_url, headers=self.headers)
#         oid = re.search(r'"cid":(\d+)', response.text).group(1)
#         return oid
#
#     def get_chat_urls(self):
#         """
#         获取指定时间内的弹幕
#         :param oid: 用户id
#         :param start_time: 爬取开始时间
#         :param end_time: 爬取结束时间
#         :return: 弹幕url列表
#         """
#         url_list = []
#         oid = self.get_oid()
#         date_list = [i for i in pd.date_range(start=self.start_time, end=self.end_time).strftime('%Y-%m-%d')]
#         for date in date_list:
#             url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={0}&date={1}'.format(oid, date)
#             url_list.append(url)
#         return url_list
#
#     def get_bullet_chat(self):
#         """
#         爬取并保存弹幕数据
#         :param url_list: 弹幕url列表
#         :return:
#         """
#         print('正在爬取视频编号为{}的弹幕数据'.format(self.bvid))
#         urls = self.get_chat_urls()
#         for i in range(len(urls)):
#             chat_response = requests.get(urls[i], headers=self.headers)
#             chat_response.encoding = 'utf-8'
#             soup = BeautifulSoup(chat_response.text)
#             data = soup.find_all('d')
#             chat_data = [data[i].text for i in range(len(data))]
#
#             # 以pandas Series格式写入数据
#             chat_series = pd.Series(chat_data)
#             chat_series.to_csv(self.bvid + '.csv', mode="a", header=False, index=False)
#             print('链接{}的弹幕数据爬取成功'.format(urls[i]))
#
#             if i % 10 == 0:
#                 time.sleep(random.uniform(3, 5))
#
#
# if __name__ == '__main__':
#     code = input('请输入视频编号：')
#     bullet_chat = BulletChat(code)
#     bullet_chat.get_bullet_chat()


from bilibili_api import video, Verify, Danmaku

# v = video.get_video_info(bvid="BV1dk4y1C72G")
# print(v)

verify = Verify("c8a19b78%2C1620925524%2C5d1eb*b1", "74dd49deed8699010a455f33b788741a")
danmu = Danmaku("养鸡站")
