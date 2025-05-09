from pathlib import Path


class ConfigApp:
    name = "src.app:app"
    port = 5050
    host = "0.0.0.0"
    port_vue = 5173
    origins = [
        "http://localhost",
        f"http://localhost:{port_vue}",
    ]


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
    check_interval_hours = 1


class Config:
    app = ConfigApp()
    paths = ConfigPaths()
    database = ConfigDatabase()
    data = ConfigData()
    scheduler = ConfigScheduler()