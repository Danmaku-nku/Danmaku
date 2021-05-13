import subprocess

video_path = "./original_video/"
video_name = "Planet_Earth_I-2.mp4"
temp_video_path = "./temp_videos"

sub_list_path = "../old_results/DSNet/sub_list_DSNet_8.csv"

with open(sub_list_path, encoding='utf-8') as result:
    starts = []
    ends = []
    header_line = result.readline()  # 读取并弹出第一行
    for line in result:
        col = line.split(',')  # 每行分隔为列表，好处理列格式
        col[1] = float(col[1])
        col[2] = float(col[2])

        starts.append(col[1])
        ends.append(col[2])



def sec2str(x):
    y = int(x)
    h = int(y / 3600)
    m = int((y % 3600) / 60)
    s = x - 60 * m + 3600 * h
    s = str(s)
    result = str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + s[0:6]

    return result


for i in range(len(starts)):
    starts[i] = sec2str(starts[i])
    ends[i] = sec2str(ends[i])


'''
#Cut and Merge
'''

for i in range(len(starts)):
    tag_start = starts[i]
    tag_end = ends[i]
    cmd = 'ffmpeg' + ' -ss ' + tag_start + ' -to ' + tag_end  + ' -accurate_seek -i ' + video_path + video_name + \
          ' -c copy -avoid_negative_ts 1 ' + temp_video_path + '/output' + str(i) + '.mp4'
    # cmd = 'ffmpeg' + ' -ss ' + tag_start + ' -to ' + tag_end + ' -i ' + video_path + video_name + \
    #       ' -c:v libx264 -preset superfast -c:a copy ' + temp_video_path + '/output' + str(i) + '.mp4'

    with open(temp_video_path + '/filelist.txt', 'a', encoding='utf-8') as f:
        text = 'file   ' + "'" + 'output' + str(i) + '.mp4' + "' \n"
        f.write(text)

    subprocess.call(cmd, shell=True)

cmd = 'ffmpeg -f concat -safe 0 -i ' + temp_video_path + '/filelist.txt -c copy ' + 'output.mp4'

subprocess.call(cmd, shell=True)

# cmd = 'ffmpeg -i ' + video_path + video_name + '  -vn ' + 'output.mp3'
#
# subprocess.call(cmd, shell=True)
