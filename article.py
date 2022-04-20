class Article:
    name: str = ""
    url: str = ""
    certifications: list[str] = []

    def __init__(self, name: str, url: str, certifications: list[str]):
        self.name = name
        self.url = url
        self.certifications = certifications
