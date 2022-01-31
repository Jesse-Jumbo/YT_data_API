import requests
import json
import csv

from datetime import datetime, timezone, timedelta


filenameJ = 'youtube_trending_video.json'
filenameC = 'youtube_trending_video.csv'

YOUTUBE_API_KEY = "your api key"

all_trending_video = {'yt_trending_video': [], 'update_time': "" }

fever_video_data = {"channel_info": [], "video_info": []}

channel_info_list = []

video_info_list = []
all_keys = []
all_values = []

def main():
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)

    for itme in youtube_spider.get_popular_video_list()['items']:
        youtube_channel_id = itme['snippet']['channelId']

        channel_info = youtube_spider.get_channel_info(youtube_channel_id)
        channel_info_list.append(channel_info)

    for item in youtube_spider.get_popular_video_list()['items']:
        video_id = item['id']
        video_info = youtube_spider.get_video_info(video_id)
        video_info_list.append(video_info)


    for data in range(len(video_info_list)):
        fever_video_data['channel_info'] = channel_info_list[data]
        fever_video_data['video_info'] = video_info_list[data]
        all_trending_video['yt_trending_video'].append(fever_video_data.copy())
    all_trending_video['update_time'] = "UTC+8 " + datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    save_to_json(all_trending_video)

    # write to csv
    # 蒐集channel_info的keys
    for key in channel_info_list[0].keys():
        all_keys.append(key)
    # 蒐集video_info的keys
    for key in video_info_list[0].keys():
        all_keys.append(key)
    # 蒐集channel_info的values
    for i in range(len(channel_info_list)):
        channel_values = []
        for value in channel_info_list[i].values():
            channel_values.append(value)
        all_values.append(channel_values)
    # 蒐集video_info的values
    for i in range(len(video_info_list)):
        video_values = []
        for value in video_info_list[i].values():
            video_values.append(value)
            all_values[i].append(value)
        all_values[i].append(all_trending_video['update_time'])

    with open(filenameC, 'w', newline='', encoding='UTF-8') as csvfiel:
        r = csv.writer(csvfiel)
        r.writerow(all_keys + ['update_time'])
        for i in all_values:
            r.writerow(i)



def save_to_json(data):
    with open(filenameJ, 'w') as w_f:
        save_data = data
        w_f.write(json.dumps(save_data, sort_keys=True, indent=4))


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

    def get_popular_video_list(self, list_type='mostPopular', part='snippet%2CcontentDetails%2Cstatistics', max_results=50, regionCode='TW'):
        path = f'videos?part={part}&chart={list_type}&maxResults={max_results}&regionCode={regionCode}'
        data = self.get_html_to_json(path)
        if not data:
            return []

        return data

    def get_channel_info(self, channel_id, part='contentDetails%2Cstatistics'):
        """取得頻道上傳影片清單的ID"""
        # UC7ia-A8gma8qcdC6GDcjwsQ
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}

        data_item = data['items'][0]

        try:
            subscriber = data_item['statistics']['subscriberCount']
        except KeyError:
            # subscriber hidden
            subscriber = "subscriber is hidden"

        channel_url = f"https://www.youtube.com/channel/{data_item['id']}"

        info = {
            'channel_url': channel_url,
            'total_video_count': subscriber,
            'subscriber_count': data_item['statistics']['videoCount'],
            'total_views_count': data_item['statistics']['viewCount']
        }
        return info

    def get_video_info(self, video_id, part='snippet,statistics'):
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}

        data_item = data['items'][0]

        try:
            origin_time = str(data_item['snippet']['publishedAt'])
            reset_time = datetime.strptime(origin_time, '%Y-%m-%dT%H:%M:%SZ')
            time = "UTC+8 " + str(reset_time.replace(tzinfo=timezone(timedelta(hours=8))))
        except ValueError:
            time = None

        video_url = f"https://www.youtube.com/watch?v={data_item['id']}"

        info = {
            'channel_title': data_item['snippet']['channelTitle'],
            'published_at': time,
            'video_url': video_url,
            'title': data_item['snippet']['title'],
            # 'like_count': data_item['statistics']['likeCount'],
            'comment_count': data_item['statistics']['commentCount'],
            'view_count': data_item['statistics']['viewCount']
        }
        return info


if __name__ == "__main__":
    main()



