import scrappers as s
import json

#TODO Create function to generate json
#TODO Add query words to scrapper params
#TODO Create a logs

def main():
    print("="*10)
    print("CIO scrapping begin...")
    #cio_articles: list[dict[str, any]] = s.cio_scrapper()
    print("CIO scrapping end")

    print("=" * 10)
    print("Indeed scrapping begin...")
    indeed_articles: list[dict[str, any]] = s.indeed_scrapper()
    print("Indeed scrapping end")

    f = open("./output/articles-pm-cert.json", "w+")
    json.dump({
        #"cio":  cio_articles,
        "indeed": indeed_articles
    }, f)
    f.close()


if __name__ == "__main__":
    main()
