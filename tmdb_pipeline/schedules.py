from dagster import ScheduleDefinition, define_asset_job

# On crée un job Dagster à partir d’un nom d’asset (clean_movies_data)
clean_movies_job = define_asset_job(
    name="clean_movies_job",
    selection=["clean_movies_data"]
)

# On crée le schedule qui exécute ce job chaque jour à 9h
daily_clean_schedule = ScheduleDefinition(
    job=clean_movies_job,
    cron_schedule="0 9 * * *",  # tous les jours à 9h
    name="daily_clean_schedule"
)
