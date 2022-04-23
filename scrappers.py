from article import Article

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


# *********************************************
# CIO MAGAZINE
# *********************************************
def cio_scrapper() -> list[dict]:
    cio_articles: list[Article] = []

    # *********************************************
    # CONFIGURE SELENIUM WITH CHROME DRIVER
    # *********************************************
    # Use Selenium because the website use js to render some page element
    # like the result of search
    chrome_options = Options()
    # headless browser == no display, but js code is run
    chrome_options.add_argument('--headless')
    # ChromeDriver.exe has been added to PATH (env variable)
    driver = webdriver.Chrome(options=chrome_options)

    url: str = "https://www.cio.com/search?q=certifications"
    driver.get(url)

    # Get Pages Number to configure the loop
    result_wrapper: WebElement = driver.find_element(By.CSS_SELECTOR, "div.gsc-results.gsc-webResult")
    nb_pages: int = len(driver.find_elements(By.CSS_SELECTOR, "div.gsc-cursor > div.gsc-cursor-page"))

    for i in range(1, nb_pages):

        # Navigate to the page
        css_selector: str = ".gsc-cursor-page:nth-child({})".format(i)
        page: WebElement = driver.find_element(By.CSS_SELECTOR, css_selector)
        page.click()
        # Mage sure the element on the page are correctly loaded before move on with the scrap
        WebDriverWait(driver, 5).until(lambda x: 'gsc-loading-resultsRoot' not in result_wrapper.get_attribute('class'))

        xpath_selector: str = '//div[@class="gsc-wrapper"]//div[@class="gs-title"]/a[@class="gs-title"]'
        results: list[WebElement] = driver.find_elements(By.XPATH, xpath_selector)
        nb_articles: int = len(results)

        for idx, result in enumerate(results):
            if len(result.accessible_name) > 1:
                current_article: Article = get_cio_article_details(result.get_attribute("href"), result.text)
                if current_article is not None:
                    cio_articles.append(current_article)
                    print("-- Article {}/{} scrapped".format(idx+1, nb_articles))

        print("Page {}/{} scrapped".format(i, nb_pages))

    # must close the driver after task finished
    driver.close()
    driver.quit()

    return [article.to_dict() for article in cio_articles]


def get_cio_article_details(url: str, title: str) -> Article:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    article_driver = webdriver.Chrome(options=chrome_options)
    article_url: str = url
    article_title: str = title
    article_driver.get(article_url)

    # "//div[@class='legacy_content']/ul[1]/*"
    xpath_selector: str = "//div[@class='legacy_content']/h2 |  //div[@class='legacy_content']/h3"
    titles: list[WebElement] = article_driver.find_elements(By.XPATH, xpath_selector)
    certifications_names: list[str] = [cert_name.text for cert_name in titles]

    if len(certifications_names) > 0 and certifications_names[0] != '':
        current_article = Article(article_title, article_url, certifications_names)
    else:
        current_article = None

    article_driver.close()
    article_driver.quit()

    return current_article


# *********************************************
# INDEED
# *********************************************
def indeed_scrapper() -> list[dict]:
    indeed_articles: list[Article] = []

    # *********************************************
    # CONFIGURE SELENIUM WITH CHROME DRIVER
    # *********************************************
    # Use Selenium because the website use js to render some page element
    # like the result of search
    chrome_options = Options()
    # headless browser == no display, but js code is run
    chrome_options.add_argument('--headless')
    # ChromeDriver.exe has been added to PATH (env variable)
    driver = webdriver.Chrome(options=chrome_options)

    url: str = "https://www.indeed.com/career-advice/search?q=it+certifications"
    driver.get(url)

    xpath_selector: str = "//h2[@class='card-heading css-t1a24f e1tiznh50']/a"
    results: list[WebElement] = driver.find_elements(By.XPATH, xpath_selector)
    nb_articles: int = len(results)

    for idx, result in enumerate(results):

        if len(result.accessible_name) > 1:
            current_article: Article = get_indeed_article_details(result.get_attribute("href"), result.text)
            if current_article is not None:
                indeed_articles.append(current_article)
                print(""
                      "Article {}/{} scrapped".format(idx, nb_articles))

    # must close the driver after task finished
    driver.close()
    driver.quit()

    return [article.to_dict() for article in indeed_articles]


def get_indeed_article_details(url: str, title: str) -> Article:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    article_driver = webdriver.Chrome(options=chrome_options)
    article_url: str = url
    article_title: str = title
    article_driver.get(article_url)

    # "//div[@class='legacy_content']/ul[1]/*"
    xpath_selector: str = "//h3[@class='rich-text-component css-26ec2o e1tiznh50']"
    titles: list[WebElement] = article_driver.find_elements(By.XPATH, xpath_selector)
    certifications_names: list[str] = [cert_name.text for cert_name in titles]

    if len(certifications_names) > 0 and certifications_names[0] != '':
        current_article = Article(article_title, article_url, certifications_names)
    else:
        current_article = None

    article_driver.close()
    article_driver.quit()

    return current_article
