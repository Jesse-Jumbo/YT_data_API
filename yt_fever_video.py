import requests
import json
from pprint import pprint
from datetime import datetime


YOUTUBE_API_KEY = "AIzaSyBNmtaOJYMTlBkeH5w5dL4VWl4MfxQIPa0"
filename = 'youtube_fever_video.json'

all_fever_viedo = {'yt fever video': [], 'Update time': "" }

fever_video_data = {"ChannelInfo": [], "VideoInfo": []}

channel_info_list = []
video_info_list = []

def main():
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)

    for channel_id in youtube_spider.get_popular_video()['items']:
        youtube_channel_id = channel_id['snippet']['channelId']

        channel_info = youtube_spider.get_channel(youtube_channel_id)
        channel_info_list.append(channel_info)
        print(channel_info_list)

    for id in youtube_spider.get_popular_video()['items']:
        video_id = id['id']

        video_info = youtube_spider.get_video(video_id)
        video_info_list.append(video_info)

        next_page_token = ''
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
        fever_video_data['ChannelInfo'] = channel_info_list[data]
        fever_video_data['VideoInfo'] = video_info_list[data]
        # fever_video_data['CommentsInfo'] = comments_info_list[data]
        all_fever_viedo['yt fever video'].append(fever_video_data.copy())
    all_fever_viedo['Update time'] = datetime.today().strftime('%A, %B %d, %Y %H:%M:%S')

    with open(filename, 'w') as w_f:
        youtube_fever_video = all_fever_viedo
        w_f.write(json.dumps(youtube_fever_video, sort_keys=True, indent=4))


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
            'ChannelLink': url_,
            'TotalVideoCount': subscriber,
            'SubscriberCount': data_item['statistics']['videoCount'],
            'TotalViewsCount': data_item['statistics']['viewCount']
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
            time_ = data_item['snippet']['publishedAt']
        except ValueError:
            # 日期格式錯誤
            time_ = None

        url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {
            'ChannelTitle': data_item['snippet']['channelTitle'],
            'PublishedAt': time_,
            'Video_url': url_,
            'Yitle': data_item['snippet']['title'],
            'Description': data_item['snippet']['description'],
            'LikeCount': data_item['statistics']['likeCount'],
            'CommentCount': data_item['statistics']['commentCount'],
            'ViewCount': data_item['statistics']['viewCount']
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
