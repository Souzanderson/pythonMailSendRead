import settings

class ConfigMail:
    def __init__(self):
        self.host = settings.MAIL_SETTINGS.get('host')
        self.key = settings.MAIL_SETTINGS.get('key')
        self.user = settings.MAIL_SETTINGS.get('user')
        