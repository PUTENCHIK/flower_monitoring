from pathlib import Path


class ConfigPaths:
    storage = Path("storage")


class ConfigDatabase:
    name = "database.db"


class ConfigData:
    min_value = 200
    max_value = 600


class Config:
    paths = ConfigPaths()
    database = ConfigDatabase()
    data = ConfigData()