# config.py
import os

# Configurazioni generali
ACCESS_TOKEN = "IGQWRPWUl6d1RMN1c0ckNCcFVYQTlhY0VsVlB6OGVsaVRySHZAsVWFGeFRCX1BTMGs4VU1WWkU2anN0WTVDbFBaOHQyM0d5VlVoTFVtSlRER1hBTV85MzBiTnpselZAEalZA4ZAUNRMjNrRWtMYlRpSUlfUG5MYXFxTWcZD"
API_VERSION = "v20.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"
DEBUG = False  # Imposta su True per attivare i print di debug, False per disattivarli

# Configurazioni database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instagram_data.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
