import requests
from .config import BASE_URL, DEBUG


class InstagramAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = BASE_URL

    def get_profile_info(self):
        url = f"{self.base_url}/me"
        params = {
            "fields": "id,username,account_type,media_count,followers_count,follows_count,profile_picture_url,biography,name,website",
            "access_token": self.access_token,
        }
        try:
            response = requests.get(url, params=params)
            if DEBUG:
                print("Profile Info API Response (raw):", response.text)
            response.raise_for_status()
            profile_info = response.json()
            return profile_info
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile info: {e}")
            return None

    def get_media_list(self):
        url = f"{self.base_url}/me/media"
        params = {
            "fields": "id,caption,media_type,timestamp",
            "access_token": self.access_token,
        }
        try:
            response = requests.get(url, params=params)
            if DEBUG:
                print("Media List API Response (raw):", response.text)
            response.raise_for_status()
            media_list = response.json()
            return media_list
        except requests.exceptions.RequestException as e:
            print(f"Error fetching media list: {e}")
            return None

    def get_media_details(self, media_id):
        url = f"{self.base_url}/{media_id}"
        params = {
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,comments_count,like_count,is_comment_enabled,is_shared_to_feed",
            "access_token": self.access_token,
        }
        try:
            response = requests.get(url, params=params)
            if DEBUG:
                print(f"Media Details API Response (ID: {media_id}):", response.text)
            response.raise_for_status()
            media_details = response.json()
            return media_details
        except requests.exceptions.RequestException as e:
            print(f"Error fetching media details for {media_id}: {e}")
            return None
