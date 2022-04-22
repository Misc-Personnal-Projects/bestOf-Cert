class Article:
    name: str = ""
    url: str = ""
    certifications: list[str] = []

    def __init__(self, name: str, url: str, certifications: list[str]):
        self.name = name
        self.url = url
        self.certifications = certifications

    def to_dict(self) -> dict:
        return {"name": self.name, "url": self.url, "certifications": self.certifications}