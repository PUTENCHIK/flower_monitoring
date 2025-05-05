from pathlib import Path


class ConfigPaths:
    storage = Path("storage")


class ConfigDatabase:
    name = "database.db"


class ConfigData:
    min_value = 190
    max_value = 470


class ConfigScheduler:
    check_interval_hours = 6


class Config:
    paths = ConfigPaths()
    database = ConfigDatabase()
    data = ConfigData()
    scheduler = ConfigScheduler()