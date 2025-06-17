class BotDeviceException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

    def __str__(self):
        return f"{self.detail}"
    

class NotificationException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

    def __str__(self):
        return f"{self.detail}"