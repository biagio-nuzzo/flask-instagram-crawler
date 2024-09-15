# config.py
import os

# Configurazioni generali
ACCESS_TOKEN = "<YOUR_TOKEN_ACCESS>"
API_VERSION = "v20.0"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"
DEBUG = False  # Imposta su True per attivare i print di debug, False per disattivarli

# Configurazioni database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instagram_data.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
