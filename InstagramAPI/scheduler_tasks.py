# Modules
from .instagram_api import InstagramAPI
from .models import db, ProfileInfo, MediaList, MediaDetails
from .config import ACCESS_TOKEN

# Libraries
from time import sleep
from datetime import datetime
from pytz import timezone

# Definisci il fuso orario
TIMEZONE = "Europe/Rome"
LOCAL_TZ = timezone(TIMEZONE)


def fetch_profile_info(app):
    print("⏳ Fetching profile information...")
    with app.app_context():
        api = InstagramAPI(access_token=ACCESS_TOKEN)
        profile_info = api.get_profile_info()

        if profile_info:
            new_profile = ProfileInfo(
                ig_id=profile_info["id"],
                username=profile_info["username"],
                account_type=profile_info.get("account_type"),
                media_count=profile_info.get("media_count"),
                followers_count=profile_info.get("followers_count"),
                follows_count=profile_info.get("follows_count"),
                profile_picture_url=profile_info.get("profile_picture_url"),
                biography=profile_info.get("biography"),
                name=profile_info.get("name"),
                website=profile_info.get("website"),
                timestamp=datetime.now(LOCAL_TZ),
            )
            db.session.add(new_profile)
            db.session.commit()
            print("✅ Profile info saved successfully.")
        else:
            print("❌ Failed to fetch profile info.")
        sleep(3)


def fetch_media_list(app):
    print("⏳ Fetching media list...")
    with app.app_context():
        api = InstagramAPI(access_token=ACCESS_TOKEN)
        media_list = api.get_media_list()

        if media_list and "data" in media_list:
            new_media_count = 0
            for media in media_list["data"]:
                existing_media = MediaList.query.filter_by(id=media["id"]).first()
                if not existing_media:
                    new_media = MediaList(
                        id=media["id"],
                        caption=media.get("caption"),
                        media_type=media.get("media_type"),
                        timestamp=datetime.strptime(
                            media["timestamp"], "%Y-%m-%dT%H:%M:%S%z"
                        ),
                    )
                    db.session.add(new_media)
                    new_media_count += 1
            db.session.commit()
            print(f"✅ {new_media_count} new media added.")
        else:
            print("❌ Failed to fetch media list.")
        sleep(3)


def fetch_media_details(app):
    print("⏳ Fetching media details...")
    with app.app_context():
        api = InstagramAPI(access_token=ACCESS_TOKEN)
        media_list = MediaList.query.all()

        for media in media_list:
            media_details = api.get_media_details(media.id)
            if media_details:
                # Salva un nuovo snapshot delle informazioni del media
                new_details = MediaDetails(
                    media_id=media_details["id"],
                    caption=media_details.get("caption"),
                    media_type=media_details.get("media_type"),
                    media_url=media_details.get("media_url"),
                    permalink=media_details.get("permalink"),
                    thumbnail_url=media_details.get("thumbnail_url"),
                    timestamp=datetime.strptime(
                        media_details["timestamp"], "%Y-%m-%dT%H:%M:%S%z"
                    ),
                    username=media_details.get("username"),
                    comments_count=media_details.get("comments_count"),
                    like_count=media_details.get("like_count"),
                    is_comment_enabled=media_details.get("is_comment_enabled"),
                    is_shared_to_feed=media_details.get("is_shared_to_feed"),
                    fetched_at=datetime.now(LOCAL_TZ),  # Timestamp per questo snapshot
                )
                db.session.add(new_details)
                db.session.commit()
                print(f"✅ Details snapshot saved for media ID: {media.id}")
            else:
                print(f"❌ Failed to fetch details for media ID: {media.id}")
            sleep(2)
