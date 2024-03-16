class Parser:
    def __init__(self, config: str):
        self.config = config

    def parse(self):
        return None


def parse(config: str):
    return Parser(config).parse()
