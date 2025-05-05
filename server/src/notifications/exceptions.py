class BotDeviceException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

    def __str__(self):
        return f"{self.detail}"