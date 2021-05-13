danmu_list_path = "../get_live_commenting/danmu/BV1Ux411S7oh/p_1.csv"

video_path = "./original_video/"
video_name = "Planet_Earth_I-2.mp4"

edge = 3 # 掐头去尾 必须大于等于1
delay_second = 3 # 弹幕滞后秒数
summary_len_expectation = 180

# Standard PySceneDetect imports:
import os
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager

# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector


def find_scenes(video_path):
    # type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
    video_manager = VideoManager([video_path])
    stats_manager = StatsManager()
    # Construct our SceneManager and pass it our StatsManager.
    scene_manager = SceneManager(stats_manager)

    # Add ContentDetector algorithm (each detector's constructor
    # takes detector options, e.g. threshold).
    scene_manager.add_detector(ContentDetector())

    # We save our stats file to {VIDEO_PATH}.stats.csv.
    stats_file_path = '%s.stats.csv' % video_path

    scene_list = []

    try:
        # If stats file exists, load it.
        if os.path.exists(stats_file_path):
            # Read stats from CSV file opened in read mode:
            with open(stats_file_path, 'r') as stats_file:
                stats_manager.load_from_csv(stats_file)

        # Set downscale factor to improve processing speed.
        video_manager.set_downscale_factor()

        # Start video_manager.
        video_manager.start()

        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager)

        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list()
        # Each scene is a tuple of (start, end) FrameTimecodes.
        '''
        print('List of scenes obtained:')
        for i, scene in enumerate(scene_list):
            print(
                'Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
                    i + 1,
                    scene[0].get_timecode(), scene[0].get_frames(),
                    scene[1].get_timecode(), scene[1].get_frames(),))
        '''
        # We only write to the stats file if a save is required:
        if stats_manager.is_save_required():
            base_timecode = video_manager.get_base_timecode()
            with open(stats_file_path, 'w') as stats_file:
                stats_manager.save_to_csv(stats_file, base_timecode)

    finally:
        video_manager.release()

    return scene_list


def str2sec(x):
    h, m, s = x.strip().split(':')  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + float(s)  # int()函数转换成整数运算


sub_list = []

scene_list = find_scenes(video_path + video_name)

for i, scene in enumerate(scene_list):
    sub_list.append(str2sec(scene[1].get_timecode()))

# print(sub_list)

with open(danmu_list_path, encoding='utf-8') as result:
    time_list = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        time_list.append(float(col[0])/(47*60+53)*(49*60+57)) # B站和自己的视频有个等比缩放

danmu_num_for_sub = []
time_index = 0
for i in range(len(sub_list)):
    danmu_num_for_sub.append(0)
    while(time_index < len(time_list) and time_list[time_index] <= sub_list[i] + delay_second):
        danmu_num_for_sub[i] += 1
        time_index += 1

# print(len(sub_list))
# print(len(danmu_num_for_sub))
# print(sub_list)
# print(danmu_num_for_sub)

danmu_density_for_sub = [0.0]
for i in range(1,len(sub_list)):
    danmu_density_for_sub.append(danmu_num_for_sub[i] / (sub_list[i]-sub_list[i-1]))

for i in range(edge):
    danmu_density_for_sub[i] = 0
    danmu_density_for_sub[-i-1] = 0

import numpy as np

starts_old = []
ends_old = []
summary_len = 0
danmu_density_for_sub_np = np.array(danmu_density_for_sub)

# print(danmu_num_for_sub)
# print(danmu_num_for_sub_np)
# print(danmu_num_for_sub_np.argmax())

while(summary_len < summary_len_expectation):
    sub_index = danmu_density_for_sub_np.argmax()
    danmu_density_for_sub_np[sub_index] = 0
    starts_old.append(sub_list[sub_index-1])
    ends_old.append(sub_list[sub_index])
    summary_len += sub_list[sub_index] - sub_list[sub_index-1]

starts_old.sort()
ends_old.sort()

# print(starts_old)
# print(ends_old)

for i in range(len(starts_old)-1):
    if(ends_old[i]+1 >= starts_old[i+1]):# 两个片段间距小于1秒就合并
        starts_old[i+1] = starts_old[i]
        starts_old[i] = -1
        ends_old[i] = -1

starts = []
ends = []

for i in range(len(starts_old)):
    if(starts_old[i] != -1):
        starts.append(starts_old[i])
        ends.append(ends_old[i])

# print(starts)
# print(ends)

len_sum = 0
for i in range(len(starts)):
    len_sum += ends[i] - starts[i]
print(len_sum)

import  pandas as pd

column_names = ["starts", "ends"]
sub_list_result = pd.DataFrame(columns=column_names)

for i in range(len(starts)):
    sub_list_result = sub_list_result.append({ "starts": starts[i],"ends": ends[i]},ignore_index=True)

sub_list_result.to_csv("./sub_list.csv",index=True)