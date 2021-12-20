import requests
import json
import csv
import pandas as pd
from pandas.io.json import json_normalize
from pprint import pprint
from datetime import datetime, timezone, timedelta

YOUTUBE_API_KEY = "AIzaSyBNmtaOJYMTlBkeH5w5dL4VWl4MfxQIPa0"

filenameJ = 'youtube_fever_video.json'
filenameC = 'youtube_fever_video.csv'

all_fever_viedo = {'YT Trending Video': [], 'Update Time': "" }

fever_video_data = {"Channel Info": [], "Video Info": []}

channel_info_list = []
video_info_list = []
all_keys = []
all_values = []

def main():
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)

    for channel_id in youtube_spider.get_popular_video()['items']:
        youtube_channel_id = channel_id['snippet']['channelId']

        channel_info = youtube_spider.get_channel(youtube_channel_id)
        channel_info_list.append(channel_info)

    for id in youtube_spider.get_popular_video()['items']:
        video_id = id['id']
        video_info = youtube_spider.get_video(video_id)
        video_info_list.append(video_info)

        # r.writeheader()
        # r.writerow(video_info.values())

        # next_page_token = ''
        # while 1:
        #     comments, next_page_token = youtube_spider.get_comments(video_id, page_token=next_page_token)
        #     comments_info_list.append(comments)
        #     print(channel_info_list)
        #     print(video_info_list)
        #     print(comments_info_list)
        #     # 如果沒有下一頁留言，則跳離
        #     if not next_page_token:
        #         break

    for data in range(len(video_info_list)):
        fever_video_data['Channel Info'] = channel_info_list[data]
        fever_video_data['Video Info'] = video_info_list[data]
        # fever_video_data['CommentsInfo'] = comments_info_list[data]
        all_fever_viedo['YT Trending Video'].append(fever_video_data.copy())
    all_fever_viedo['Update Time'] = "UTC+8 " + datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    with open(filenameJ, 'w') as w_f:
        youtube_fever_video = all_fever_viedo
        w_f.write(json.dumps(youtube_fever_video, sort_keys=True, indent=4))


    for key in channel_info_list[0].keys():
        all_keys.append(key)

    for i in range(len(channel_info_list)):
        channel_values = []
        for value in channel_info_list[i].values():
            channel_values.append(value)
        all_values.append(channel_values)

    for key in video_info_list[0].keys():
        all_keys.append(key)

    for i in range(len(video_info_list)):
        video_values = []
        for value in video_info_list[i].values():
            video_values.append(value)
            all_values[i].append(value)
        all_values[i].append(all_fever_viedo['Update Time'])

    with open(filenameC, 'w', newline='', encoding='UTF-8') as csvfiel:
        r = csv.writer(csvfiel)
        r.writerow(all_keys + ['Update Time'])
        for i in all_values:
            r.writerow(i)






    #     all_fever_viedo['YT Trending Video'][i]['ChannelInfo'],
    #                        # all_fever_viedo['YT Trending Video'][i]['ChannelInfo']['SubscriberCount'],
    #                        # all_fever_viedo['YT Trending Video'][i]['ChannelInfo']['TotalVideoCount'],
    #                        # all_fever_viedo['YT Trending Video'][i]['ChannelInfo']['TotalViewsCount'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['ChannelTitle'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['CommentCount'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['LikeCount'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['Description'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['PublishedAt'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['Video_url'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['ViewCount'],
    #                        # all_fever_viedo['YT Trending Video'][i]['VideoInfo']['Title'], all_fever_viedo['Update Time']

class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_popular_video(self, list_type='mostPopular', part='snippet%2CcontentDetails%2Cstatistics', max_results=50, regionCode='TW'):
        path = f'videos?part={part}&chart={list_type}&maxResults={max_results}&regionCode={regionCode}'
        data = self.get_html_to_json(path)
        if not data:
            return []

        return data

    def get_channel(self, channel_id, part='contentDetails%2Cstatistics'):
        """取得頻道上傳影片清單的ID"""
        # UC7ia-A8gma8qcdC6GDcjwsQ
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        # 以下整理並提取需要的資料
        data_item = data['items'][0]

        try:
            subscriber = data_item['statistics']['subscriberCount']
        except KeyError:
            # subscriber hidden
            subscriber = None

        url_ = f"https://www.youtube.com/channel/{data_item['id']}"

        info = {
            'Channel URL': url_,
            'Total Video Count': subscriber,
            'Subscriber Count': data_item['statistics']['videoCount'],
            'Total Views Count': data_item['statistics']['viewCount']
        }
        return info

    def get_video(self, video_id, part='snippet,statistics'):
        """取得影片資訊"""
        # jyordOSr4cI
        # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        # 以下整理並提取需要的資料
        data_item = data['items'][0]

        try:
            # 2019-09-29T04:17:05Z
            o_time = str(data_item['snippet']['publishedAt'])
            r_time = datetime.strptime(o_time, '%Y-%m-%dT%H:%M:%SZ')
            time = "UTC+8 " + str(r_time.replace(tzinfo=timezone(timedelta(hours=8))))
        except ValueError:
            # 日期格式錯誤
            time = None

        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {
            'Channel Title': data_item['snippet']['channelTitle'],
            'Published At': time,
            'Video URL': url_,
            'Title': data_item['snippet']['title'],
            'Description': data_item['snippet']['description'],
            'Like Count': data_item['statistics']['likeCount'],
            'Comment Count': data_item['statistics']['commentCount'],
            'View Count': data_item['statistics']['viewCount']
        }
        return info

    def get_comments(self, video_id, page_token='', part='snippet', max_results=100):
        """取得影片留言"""
        # jyordOSr4cI
        path = f'commentThreads?part={part}&videoId={video_id}&maxResults={max_results}&pageToken={page_token}'
        data = self.get_html_to_json(path)
        if not data:
            return [], ''
        # 下一頁的數值
        next_page_token = data.get('nextPageToken', '')

        # 以下整理並提取需要的資料
        comments = []
        for data_item in data['items']:
            data_item = data_item['snippet']
            top_comment = data_item['topLevelComment']
            try:
                # 2020-08-03T16:00:56Z
                time_ = str(datetime.strptime(top_comment['snippet']['publishedAt'], '%Y-%m-%d %H:%M:%S'))
            except ValueError:
                # 日期格式錯誤
                time_ = None

            ru_name = top_comment['snippet'].get('authorDisplayName', '')
            if not ru_name:
                ru_name = ''

            comments.append({
                'ru_name': ru_name,
                'reply_time': time_,
                'reply_content': top_comment['snippet']['textOriginal'],
                'rm_positive': int(top_comment['snippet']['likeCount']),
                'rn_comment': int(data_item['totalReplyCount'])
            })
        return comments, next_page_token


if __name__ == "__main__":
    main()
