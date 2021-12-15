import requests


YOUTUBE_API_KEY = "AIzaSyBNmtaOJYMTlBkeH5w5dL4VWl4MfxQIPa0"


def get_html_to_jdon(self, path):
    api_url = f"{self.base_url}{path}&key={self.api_key}"
    r = requests.get(api_url)
    if r.status_code == requests.codes.ok:
        data = r.json()
    else:
        data = None
    return data
