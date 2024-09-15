from pytz import timezone

# Definisci il fuso orario per lo scheduler
TIMEZONE = "Europe/Rome"
LOCAL_TZ = timezone(TIMEZONE)

# Mappatura dei job dello scheduler
SCHEDULED_JOBS = [
    {
        "id": "fetch_profile_info",
        "func": ".scheduler_tasks:fetch_profile_info",  # Formato 'modulo_nome:funzione_nome'
        "trigger": "interval",
        "minutes": 1,
        "timezone": LOCAL_TZ,
    },
    {
        "id": "fetch_media_list",
        "func": ".scheduler_tasks:fetch_media_list",
        "trigger": "interval",
        "minutes": 1,
        "timezone": LOCAL_TZ,
    },
    {
        "id": "fetch_media_details",
        "func": ".scheduler_tasks:fetch_media_details",
        "trigger": "interval",
        "minutes": 2,
        "timezone": LOCAL_TZ,
    },
]
