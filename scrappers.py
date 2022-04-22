from article import Article

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


def cio_scrapper() -> list[Article]:
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
    idx_page: int = 1

    while idx_page <= nb_pages:

        # Navigate to the page
        css_selector: str = ".gsc-cursor-page:nth-child({})".format(idx_page)
        page: WebElement = driver.find_element(By.CSS_SELECTOR, css_selector)
        page.click()
        # Mage sure the element on the page are correctly loaded before move on with the scrap
        WebDriverWait(driver, 5).until(lambda x: 'gsc-loading-resultsRoot' not in result_wrapper.get_attribute('class'))

        #
        results: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, "a.gs-title")
        i: int = len(results)

        for result in results:
            print(i)
            i -= 1
            if len(result.accessible_name) > 1:
                current_article: Article = get_article_details(result.get_attribute("href"), result.text)
                if current_article is not None:
                    cio_articles.append(current_article)

        print("{}<={}".format(idx_page, nb_pages))
        idx_page += 1

    # must close the driver after task finished
    driver.close()
    driver.quit()

    return cio_articles


def get_article_details(url : str, title: str) -> Article:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    article_driver = webdriver.Chrome(options=chrome_options)
    article_url: str = url
    article_title: str = title
    article_driver.get(article_url)

    li_cert: list[WebElement] = article_driver.find_elements(By.XPATH,
                                                             "//div[@class='legacy_content']/ul[1]/*")
    certifications_names: list[str] = [cert_name.text for cert_name in li_cert]

    if len(certifications_names) > 0:
        current_article = Article(article_title, article_url, certifications_names)
    else:
        current_article = None

    article_driver.close()
    article_driver.quit()

    return current_article
