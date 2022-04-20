from scrappers import cio_scrapper
from article import Article


def main():
    articles: dict[str, list[Article]] = {}
    articles["cio"] = cio_scrapper()
    print(articles)


if __name__ == "__main__":
    main()
