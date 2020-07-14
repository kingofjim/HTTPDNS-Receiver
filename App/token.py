import secrets


class Token:

    def __init__(self, token):
        self.token = token

    def decode(self):
        return {
            'c10d50257062466994bf1eeaa67d29d0': ['ie', 'android'],  # IE Android
            '8235bb08bb1ba0491471164357218575': ['hqt', 'android'],  # QT Android
            'fd692f27f0bd624ab5545fe839d2d6f4': ['hqt', 'ios'],  # QT iOS
            '81475c20a598c3bd3e766bbcb1b95ae9': ['hqt', 'web'],  # QT Web
            }[self.token]

    @staticmethod
    def generator():
        return secrets.token_hex(16)
