from scrappers import cio_scrapper
from article import Article
import json

def main():
    cio_articles: list[dict[str, any]] = cio_scrapper()

    f = open("./output/articles.json", "w+")
    json.dump({"cio",  cio_articles}, f)
    f.close()


if __name__ == "__main__":
    main()
