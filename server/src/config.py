from pathlib import Path


class ConfigPaths:
    storage = Path("storage")


class ConfigDatabase:
    name = "database.db"


class Config:
    paths = ConfigPaths()
    database = ConfigDatabase()