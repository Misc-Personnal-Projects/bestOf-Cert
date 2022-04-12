from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
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


cio_articles: dict[str, list[str]] = {}
css_selector: str = ""
results: list[WebElement] = []
article_url: str = ""
page: WebElement

while idx_page <= nb_pages:

    css_selector = ".gsc-cursor-page:nth-child({})".format(idx_page)
    page = driver.find_element(By.CSS_SELECTOR, css_selector)
    page.click()
    WebDriverWait(driver, 5).until(lambda x: 'gsc-loading-resultsRoot' not in result_wrapper.get_attribute('class'))

    results = driver.find_elements(By.CSS_SELECTOR, "a.gs-title")

    for result in results:
        if len(result.accessible_name) > 1:
            deepDiveDriver = webdriver.Chrome(options=chrome_options)
            article_url = result.get_attribute("href")
            deepDiveDriver.get(article_url)
            # TODO: Bug with cert_name.text that is empty although li_cert[0].text is not
            li_cert: list[WebElement] = deepDiveDriver.find_elements(By.XPATH, "//div[@class='legacy_content']/ul[1]/*")
            certifications_names: list[str] = [cert_name.text for cert_name in li_cert]
            cio_articles[result.text] = [article_url, certifications_names]
            deepDiveDriver.close()
            deepDiveDriver.quit()

    idx_page += 1

for k, v in cio_articles.items():
    print(k + " " + v)

# must close the driver after task finished
driver.close()
driver.quit()
