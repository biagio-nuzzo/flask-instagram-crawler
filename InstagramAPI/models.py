from .database import db
from datetime import datetime


# Modello per le informazioni del profilo
class ProfileInfo(db.Model):
    __tablename__ = "profile_info"

    id = db.Column(db.Integer, primary_key=True)  # ID univoco del record
    ig_id = db.Column(
        db.String(50), nullable=False
    )  # ID del profilo Instagram
    username = db.Column(db.String(80), nullable=False)  # Nome utente del profilo
    account_type = db.Column(
        db.String(20), nullable=True
    )  # Tipo di account (es. business, personal)
    media_count = db.Column(
        db.Integer, nullable=False
    )  # Numero di post pubblicati dal profilo
    followers_count = db.Column(
        db.Integer, nullable=False
    )  # Numero di follower del profilo
    follows_count = db.Column(
        db.Integer, nullable=False
    )  # Numero di persone seguite dal profilo
    profile_picture_url = db.Column(
        db.String(255), nullable=True
    )  # URL dell'immagine del profilo
    biography = db.Column(db.Text, nullable=True)  # Biografia del profilo
    name = db.Column(db.String(100), nullable=True)  # Nome del profilo
    website = db.Column(db.String(255), nullable=True)  # Sito web associato al profilo
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )  # Data e ora del record

    def __repr__(self):
        return f"<ProfileInfo {self.username}>"


# Modello per la lista dei media
class MediaList(db.Model):
    __tablename__ = "media_list"

    id = db.Column(db.String(50), primary_key=True)  # ID univoco del media su Instagram
    caption = db.Column(db.String(255))  # Didascalia del media
    media_type = db.Column(db.String(50))  # Tipo di media (es. immagine, video, album)
    permalink = db.Column(db.String(255), nullable=True)  # URL permanente al media
    media_url = db.Column(
        db.String(255), nullable=True
    )  # URL del contenuto multimediale
    thumbnail_url = db.Column(
        db.String(255), nullable=True
    )  # URL della miniatura per i video
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # Data e ora di creazione del media su Instagram

    def __repr__(self):
        return f"<MediaList {self.id}>"


# Modello per i dettagli dei media
class MediaDetails(db.Model):
    __tablename__ = "media_details"

    id = db.Column(db.Integer, primary_key=True)  # ID univoco del record
    media_id = db.Column(
        db.String(50), db.ForeignKey("media_list.id"), nullable=False
    )  # ID del media correlato
    caption = db.Column(db.String(255))  # Didascalia del media
    media_type = db.Column(db.String(50))  # Tipo di media (es. immagine, video, album)
    media_url = db.Column(
        db.String(255), nullable=True
    )  # URL del contenuto multimediale
    permalink = db.Column(db.String(255), nullable=True)  # URL permanente al media
    thumbnail_url = db.Column(
        db.String(255), nullable=True
    )  # URL della miniatura del media
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow
    )  # Data e ora del media su Instagram
    username = db.Column(
        db.String(80), nullable=True
    )  # Nome utente che ha creato il media
    comments_count = db.Column(db.Integer, default=0)  # Numero di commenti sul media
    like_count = db.Column(db.Integer, default=0)  # Numero di "Mi piace" sul media
    is_comment_enabled = db.Column(
        db.Boolean, default=True
    )  # Flag per indicare se i commenti sono abilitati
    is_shared_to_feed = db.Column(
        db.Boolean, default=False
    )  # Flag per indicare se il contenuto è condiviso nel feed
    fetched_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )  # Data e ora del recupero del media

    def __repr__(self):
        return f"<MediaDetails {self.media_id}>"
