from article import Article

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

cio_articles: list[Article] = []
css_selector: str = ""
results: list[WebElement] = []
article_url: str = ""
article_title: str = ""
page: WebElement

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

# *********************************************
# CONFIGURE URL TO SCRAP
# *********************************************
# TODO: Add an list of url with a Scrap function associated
url: str = "https://www.cio.com/search?q=certifications"

# *********************************************
# START SCRAPING
# *********************************************
# TODO: Loop through all url to scrap an apply the scrapping function
# retrieve url in headless browser

# *********************************************
# SCRAPPING FUNCTION
# *********************************************
driver.get(url)

result_wrapper: WebElement = driver.find_element(By.CSS_SELECTOR, "div.gsc-results.gsc-webResult")
nb_pages: int = len(driver.find_elements(By.CSS_SELECTOR, "div.gsc-cursor > div.gsc-cursor-page"))
idx_page: int = 1

while idx_page <= nb_pages:

    css_selector = ".gsc-cursor-page:nth-child({})".format(idx_page)
    page = driver.find_element(By.CSS_SELECTOR, css_selector)
    page.click()
    WebDriverWait(driver, 5).until(lambda x: 'gsc-loading-resultsRoot' not in result_wrapper.get_attribute('class'))

    results = driver.find_elements(By.CSS_SELECTOR, "a.gs-title")
    i: int = len(results)

    for result in results:
        print(i)
        i -= 1
        if len(result.accessible_name) > 1:
            deepDiveDriver = webdriver.Chrome(options=chrome_options)
            article_url = result.get_attribute("href")
            article_title = result.text
            deepDiveDriver.get(article_url)

            li_cert: list[WebElement] = deepDiveDriver.find_elements(By.XPATH, "//div[@class='legacy_content']/ul[1]/*")
            certifications_names: list[str] = [cert_name.text for cert_name in li_cert]

            current_article = Article(article_title, article_url, certifications_names)
            cio_articles.append(current_article)

            deepDiveDriver.close()
            deepDiveDriver.quit()

    print("{}<={}".format(idx_page, nb_pages))
    idx_page += 1

for article in cio_articles:
    print(article.name + " " + article.url)

    for certification in article.certifications:
        print("- " + certification + "\n")

# must close the driver after task finished
driver.close()
driver.quit()
