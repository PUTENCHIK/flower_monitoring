from pathlib import Path


class ConfigPaths:
    storage = Path("storage")


class ConfigDatabase:
    name = "database.db"


class ConfigData:
    min_value = 150
    max_value = 600
    default_low_level_boundary = 33
    default_medium_level_boundary = 66

class ConfigScheduler:
    check_interval_hours = 6


class Config:
    paths = ConfigPaths()
    database = ConfigDatabase()
    data = ConfigData()
    scheduler = ConfigScheduler()