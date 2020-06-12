import secrets


class Token:

    def __init__(self, token):
        self.token = token

    def decode(self):
        return {
            'c10d50257062466994bf1eeaa67d29d0': ['IE', 'android'],  # IE Android
            }[self.token]

    def generator(self):
        return secrets.token_hex(16)
