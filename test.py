import requests
import json
from datetime import datetime

YOUTUBE_API_KEY = "AIzaSyBNmtaOJYMTlBkeH5w5dL4VWl4MfxQIPa0"

filename = 'youtube_fever_video.json'

all_fever_viedo = []
fever_video_data = {"link": "", "video title": "", "channel name": "", "channel link": "",  "views": 0, "uploaded": "", "likes times": "", "subscribers": "", "comments": ""}

video_title_link_list = []
video_title_list = []
video_channel_name_list = []
video_channel_link_list = []
video_views_list = []
video_post_time_list = []
video_like_times_list = []
subscribers_list = []

def main():
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)

    data = youtube_spider.get_popular_video()

    for channel_id in data['items']:
        uploads_id = youtube_spider.get_channel_uploads_id(channel_id['snippet']['channelId'])

    for id in data['items']:
        vid_id = id['id']
    # for channel_name in vid['items']:
    #     video_channel_name_list.append(channel_name['snippet']['channelTitle'])
    #
    # for views in vid['items']:
    #     video_views_list.append(views['statistics']['viewCount'])
    #
    # for like in vid['items']:
    #     video_like_times_list.append(like['statistics']['likeCount'])

        for video_id in vid_id:
            print("----------------------")
            video_info = youtube_spider.get_video(video_id)
            print(video_info)

            next_page_token = ''
            while 1:
                comments, next_page_token = youtube_spider.get_comments(video_id, page_token=next_page_token)
                print(comments)
                # 如果沒有下一頁留言，則跳離
                if not next_page_token:
                    break

    with open(filename, 'w') as w_f:
        youtube_fever_video = vid
        w_f.write(json.dumps(youtube_fever_video, sort_keys=True, indent=4))

        # print(youtube_fever_video)

class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        """取得頻道上傳影片清單的ID"""
        # UC7ia-A8gma8qcdC6GDcjwsQ
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_popular_video(self, list_type='mostPopular', part='snippet%2CcontentDetails%2Cstatistics', max_results=50, regionCode='TW'):
        path = f'videos?part={part}&chart={list_type}&maxResults={max_results}&regionCode={regionCode}'
        data = self.get_html_to_json(path)
        if not data:
            return []
        return data

    def get_video(self, video_id, part='snippet,statistics'):
        """取得影片資訊"""
        # jyordOSr4cI
        # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        # 以下整理並提取需要的資料
        for data_item in data['items']:

            try:
                # 2019-09-29T04:17:05Z
                time_ = datetime.strptime(data_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                # 日期格式錯誤
                time_ = None

            url_ = f"https://www.youtube.com/watch?v={data_item['id']}"

            info = {
                'id': data_item['id'],
                'channelTitle': data_item['snippet']['channelTitle'],
                'publishedAt': time_,
                'video_url': url_,
                'title': data_item['snippet']['title'],
                'description': data_item['snippet']['description'],
                'likeCount': data_item['statistics']['likeCount'],
                'commentCount': data_item['statistics']['commentCount'],
                'viewCount': data_item['statistics']['viewCount']
            }
            return info

    def get_comments(self, video_id, page_token='', part='snippet', max_results=10):
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
                time_ = datetime.strptime(top_comment['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                # 日期格式錯誤
                time_ = None

            if 'authorChannelId' in top_comment['snippet']:
                ru_id = top_comment['snippet']['authorChannelId']['value']
            else:
                ru_id = ''

            ru_name = top_comment['snippet'].get('authorDisplayName', '')
            if not ru_name:
                ru_name = ''

            comments.append({
                'reply_id': top_comment['id'],
                'ru_id': ru_id,
                'ru_name': ru_name,
                'reply_time': time_,
                'reply_content': top_comment['snippet']['textOriginal'],
                'rm_positive': int(top_comment['snippet']['likeCount']),
                'rn_comment': int(data_item['totalReplyCount'])
            })
        return comments, next_page_token


if __name__ == "__main__":
    main()