# Built-it
import time

# Third-party
from apscheduler.schedulers.background import BackgroundScheduler

from .scheduler_tasks import fetch_profile_info, fetch_media_list, fetch_media_details
from .scheduler_config import SCHEDULED_JOBS, LOCAL_TZ


def start_scheduler(app):
    # Inizializza lo scheduler
    scheduler = BackgroundScheduler(timezone=LOCAL_TZ)

    # Aggiungi i job usando la configurazione dal file scheduler_config.py
    for job in SCHEDULED_JOBS:
        scheduler.add_job(
            id=job["id"],
            func=globals()[
                job["func"].split(":")[1]
            ],  # Ottieni il riferimento alla funzione tramite globals()
            trigger="interval",
            minutes=job["minutes"],
            args=[app],  # Passa l'app Flask come argomento
            timezone=job["timezone"],
        )
        print(f"Scheduled job '{job['id']}' to run every {job['minutes']} minutes.")

    # Avvia lo scheduler
    scheduler.start()
    print("✅ Scheduler started.")

    try:
        while True:
            time.sleep(2)  # Mantieni lo script in esecuzione
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("🛑 Scheduler stopped.")
