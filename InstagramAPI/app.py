# Built-in
import os
import threading

# Flask
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, upgrade
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Config
from .config import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    ACCESS_TOKEN,
)

# Modules
from .database import db
from .models import ProfileInfo, MediaList, MediaDetails
from .api import api
from .scheduler import start_scheduler
from .instagram_api import InstagramAPI

# Inizializza l'app Flask
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

# Inizializza SQLAlchemy e Flask-Migrate con l'app Flask
db.init_app(app)
migrate = Migrate(app, db)

# Configura Flask-Admin
admin = Admin(app, name="Admin Panel", template_mode="bootstrap3")
admin.add_view(ModelView(ProfileInfo, db.session))
admin.add_view(ModelView(MediaList, db.session))
admin.add_view(ModelView(MediaDetails, db.session))

# Registra il blueprint delle API con un prefisso URL
app.register_blueprint(api, url_prefix="/api")


def initialize_database():
    """Inizializza il database, lancia le migrazioni e avvia i test."""
    with app.app_context():
        try:
            # Controlla se la directory di migrazione esiste
            if not os.path.exists("migrations"):
                print("📂 Migrazione non trovata. Inizializzazione della migrazione...")
                os.system("flask db init")

            # Crea una nuova migrazione e aggiorna il database
            print("⚙️ Applicazione delle migrazioni al database...")
            os.system('flask db migrate -m "Initial migration"')

            # Applica le migrazioni al database
            upgrade()

            print("✅ Migrazioni applicate con successo.")

        except Exception as e:
            print(f"❌ Errore durante l'inizializzazione del database: {e}")


def run_tests():
    """Esegue i test per verificare che tutti i metodi Instagram funzionino correttamente."""
    print("\n🔍 Testing Instagram API methods...")
    api = InstagramAPI(access_token=ACCESS_TOKEN)

    # Test get_profile_info
    profile_info = api.get_profile_info()
    if profile_info:
        print("✅ Profile info fetched successfully.")
    else:
        print("❌ Failed to fetch profile info.")

    # Test get_media_list
    media_list = api.get_media_list()
    if media_list:
        print("✅ Media list fetched successfully.")
    else:
        print("❌ Failed to fetch media list.")

    # Test get_media_details
    if media_list and "data" in media_list and len(media_list["data"]) > 0:
        first_media_id = media_list["data"][0]["id"]
        media_details = api.get_media_details(first_media_id)
        if media_details:
            print(
                f"✅ Media details fetched successfully for media ID {first_media_id}."
            )
        else:
            print(f"❌ Failed to fetch media details for media ID {first_media_id}.")
    else:
        print("⚠️ No media found to fetch details.")


def start_flask_server():
    """Avvia il server Flask per esporre le API."""
    print("\n🚀 Starting the Flask application...")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)


def start_services():
    """Inizializza i servizi: Database, Test, API e Scheduler."""
    initialize_database()  # Passo 1: Inizializza il database
    run_tests()  # Passo 2: Esegui i test dei metodi Instagram

    # Passo 3: Avvia il server Flask in un thread separato
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()

    # Avvia lo scheduler
    with app.app_context():
        start_scheduler(app)


if __name__ == "__main__":
    # Avvia l'applicazione Flask
    start_services()
