channel_info_list = [{'Channel URL': 'https://www.youtube.com/channel/UCXxAXdFh-cuYXU289kd-pNQ',
                      'Total Video Count': '354000', 'Subscriber Count': '324', 'Total Views Count': '91739352'},
                     {'Channel URL': 'https://www.youtube.com/channel/UCXxAXdFh-cuYXU289kd-pNQ',
                      'Total Video Count': '354000', 'Subscriber Count': '324', 'Total Views Count': '91739352'}
                     ]
video_info_list = [{'Channel Title': '全明星運動會', 'Published At': 'UTC+8 2021-12-14 04:00:11+08:00',
                    'Video URL': 'https://www.youtube.com/watch?v=-M9CK7BhwR0',
                    'Title': '目標鎖定！他就是我的狀元！速度令人震驚、分隊令人震驚，錢姊一個指名，小傑的步調全部被打亂啦～',
                    'Description': '測試賽：【跳遠】、【50公尺游泳】、【美式躲避球】\n終於要分隊了，大家能去到自己心目中的隊伍嗎？',
                    'Like Count': '8045', 'Comment Count': '2341', 'View Count': '1052185'},
                   {'Channel Title': '全明星運動會', 'Published At': 'UTC+8 2021-12-14 04:00:11+08:00',
                    'Video URL': 'https://www.youtube.com/watch?v=-M9CK7BhwR0',
                    'Title': '目標鎖定！他就是我的狀元！速度令人震驚、分隊令人震驚，錢姊一個指名，小傑的步調全部被打亂啦～',
                    'Description': '測試賽：【跳遠】、【50公尺游泳】、【美式躲避球】\n終於要分隊了，大家能去到自己心目中的隊伍嗎？',
                    'Like Count': '8045', 'Comment Count': '2341', 'View Count': '1052185'}
                   ]
# channel_values = ['https://www.youtube.com/channel/UCXxAXdFh-cuYXU289kd-pNQ', '354000', '324', '91739352']
# video_values = ['全明星運動會', 'UTC+8 2021-12-14 04:00:11+08:00', 'https://www.youtube.com/watch?v=-M9CK7BhwR0',
#               '目標鎖定！他就是我的狀元！速度令人震驚、分隊令人震驚，錢姊一個指名，小傑的步調全部被打亂啦～',
#               '測試賽：【跳遠】、【50公尺游泳】、【美式躲避球】\n終於要分隊了，大家能去到自己心目中的隊伍嗎？', '8045', '2341', '1052185']
channel_values = []
video_values = []
all_values = []

for i in range(len(channel_info_list)):
    channel_values = []
    for value in channel_info_list[i].values():
        channel_values.append(value)
    all_values.append(channel_values)
print(all_values)

for i in range(len(video_info_list)):
    video_values = []
    for value in video_info_list[i].values():
        video_values.append(value)
        all_values[i].append(value)
print(all_values)
