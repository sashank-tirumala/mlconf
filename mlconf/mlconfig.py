class MLConfig:
    def __init__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
