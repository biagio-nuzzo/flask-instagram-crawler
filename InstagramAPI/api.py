from flask import Blueprint, jsonify, request
from sqlalchemy import func
from datetime import datetime, timedelta
from .models import db, ProfileInfo, MediaList, MediaDetails

api = Blueprint("api", __name__)


@api.route("/profile/last", methods=["GET"])
def get_last_profile_info():
    """Restituisce le ultime informazioni del profilo salvate."""
    last_profile = ProfileInfo.query.order_by(ProfileInfo.timestamp.desc()).first()
    if last_profile:
        return (
            jsonify(
                {
                    "ig_id": last_profile.ig_id,
                    "username": last_profile.username,
                    "account_type": last_profile.account_type,
                    "media_count": last_profile.media_count,
                    "followers_count": last_profile.followers_count,
                    "follows_count": last_profile.follows_count,
                    "profile_picture_url": last_profile.profile_picture_url,
                    "biography": last_profile.biography,
                    "name": last_profile.name,
                    "website": last_profile.website,
                    "timestamp": last_profile.timestamp,
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "No profile information found."}), 404


@api.route("/media/list", methods=["GET"])
def get_media_list():
    """Restituisce la lista dei media presenti nel database."""
    media_list = MediaList.query.all()
    if media_list:
        result = []
        for media in media_list:
            result.append(
                {
                    "id": media.id,
                    "caption": media.caption,
                    "media_type": media.media_type,
                    "timestamp": media.timestamp,
                }
            )
        return jsonify(result), 200
    else:
        return jsonify({"error": "No media found."}), 404


@api.route("/media/details", methods=["GET"])
def get_media_details():
    """Restituisce l'ultimo snapshot dei dettagli di un media specifico."""
    media_id = request.args.get("id")
    if not media_id:
        return jsonify({"error": "Media ID is required."}), 400

    # Ottieni l'ultimo snapshot dei dettagli del media
    last_media_details = (
        MediaDetails.query.filter_by(media_id=media_id)
        .order_by(MediaDetails.fetched_at.desc())
        .first()
    )

    if last_media_details:
        result = {
            "media_id": last_media_details.media_id,
            "caption": last_media_details.caption,
            "media_type": last_media_details.media_type,
            "media_url": last_media_details.media_url,
            "permalink": last_media_details.permalink,
            "thumbnail_url": last_media_details.thumbnail_url,
            "timestamp": last_media_details.timestamp,
            "username": last_media_details.username,
            "comments_count": last_media_details.comments_count,
            "like_count": last_media_details.like_count,
            "is_comment_enabled": last_media_details.is_comment_enabled,
            "is_shared_to_feed": last_media_details.is_shared_to_feed,
            "fetched_at": last_media_details.fetched_at,
        }
        return jsonify(result), 200
    else:
        return jsonify({"error": f"No details found for media ID {media_id}."}), 404


@api.route("/media/trend", methods=["GET"])
def get_media_trend():
    """Estrae dal database l'andamento degli ultimi n mesi di un post specifico."""
    media_id = request.args.get("media_id")
    n_months = request.args.get("n", type=int, default=3)  # Default a 3 mesi

    if not media_id:
        return jsonify({"error": "Media ID is required."}), 400

    # Calcola la data limite per i dati degli ultimi n mesi
    current_date = datetime.utcnow()
    n_months_ago = current_date - timedelta(
        days=n_months * 30
    )  # Approx 30 days per month

    # Filtra i dati degli ultimi n mesi per il media_id specificato
    media_trend_data = (
        MediaDetails.query.filter(
            MediaDetails.media_id == media_id, MediaDetails.fetched_at >= n_months_ago
        )
        .order_by(MediaDetails.fetched_at.asc())
        .all()
    )

    if not media_trend_data:
        return (
            jsonify(
                {
                    "error": f"No trend data found for media ID {media_id} in the last {n_months} months."
                }
            ),
            404,
        )

    # Crea una lista dei dati di trend per la risposta
    trend_result = []
    for data in media_trend_data:
        trend_result.append(
            {
                "fetched_at": data.fetched_at,
                "like_count": data.like_count,
                "comments_count": data.comments_count,
                "caption": data.caption,
                "timestamp": data.timestamp,
            }
        )

    return jsonify({"media_id": media_id, "trend_data": trend_result}), 200


@api.route("/calculate/engagement-rate", methods=["GET"])
def calculate_engagement_rate():
    """Calcola l'engagement rate basato sui dati presenti nel database."""
    # Ottieni l'ultimo profilo salvato
    profile = ProfileInfo.query.order_by(ProfileInfo.timestamp.desc()).first()
    if not profile:
        return (
            jsonify(
                {"error": "No profile information found to calculate engagement rate."}
            ),
            404,
        )

    # Ottieni il numero totale di follower
    followers_count = profile.followers_count
    if not followers_count or followers_count <= 0:
        return (
            jsonify(
                {"error": "Invalid follower count for engagement rate calculation."}
            ),
            400,
        )

    # Ottieni l'ultimo snapshot di like e commenti per ogni media
    last_snapshots = (
        db.session.query(
            MediaDetails.media_id,
            func.max(MediaDetails.fetched_at).label("last_fetched"),
            MediaDetails.like_count,
            MediaDetails.comments_count,
        )
        .group_by(MediaDetails.media_id)
        .subquery()
    )

    # Somma i like e i commenti dagli ultimi snapshot
    total_likes = db.session.query(func.sum(last_snapshots.c.like_count)).scalar() or 0
    total_comments = (
        db.session.query(func.sum(last_snapshots.c.comments_count)).scalar() or 0
    )

    # Calcola l'engagement rate
    engagement_rate = ((total_likes + total_comments) / followers_count) * 100

    response = {
        "followers_count": followers_count,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "engagement_rate_per_post": engagement_rate,
    }

    return jsonify(response), 200


@api.route("/profile/stats", methods=["GET"])
def get_profile_stats():
    """Restituisce il numero di follower, follow e post negli ultimi 30, 60 o 90 giorni con uno step settimanale."""
    days = request.args.get("days", type=int, default=30)  # Default a 30 giorni
    if days not in [30, 60, 90]:
        return jsonify({"error": "Invalid value for days. Must be 30, 60, or 90."}), 400

    # Calcola la data limite per i dati degli ultimi n giorni
    current_date = datetime.utcnow()
    days_ago = current_date - timedelta(days=days)

    # Query per ottenere le informazioni settimanali del profilo negli ultimi n giorni usando strftime per ottenere anno e settimana
    profile_stats = (
        db.session.query(
            func.strftime("%Y-%m-%d", ProfileInfo.timestamp).label("week"),
            func.max(ProfileInfo.followers_count).label("followers_count"),
            func.max(ProfileInfo.follows_count).label("follows_count"),
            func.max(ProfileInfo.media_count).label("media_count"),
        )
        .filter(ProfileInfo.timestamp >= days_ago)
        .group_by("week")
        .order_by("week")
        .all()
    )

    if not profile_stats:
        return (
            jsonify({"error": f"No profile stats found for the last {days} days."}),
            404,
        )

    # Crea una lista dei dati settimanali per la risposta
    stats_result = []
    for stat in profile_stats:
        stats_result.append(
            {
                "week": stat.week,
                "followers_count": stat.followers_count,
                "follows_count": stat.follows_count,
                "media_count": stat.media_count,
            }
        )

    return jsonify({"days": days, "weekly_stats": stats_result}), 200
