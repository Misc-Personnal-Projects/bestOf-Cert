from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from bs4 import BeautifulSoup

# *********************************************
# CONFIGURE SELENIUM WITH CHROME DRIVER
# *********************************************
# Use Selenium because the website use js to render some page element
# like the result of search
chrome_options = Options()
chrome_options.add_argument('--headless')
# ChromeDriver.exe has been added to PATH (env variable)
driver = webdriver.Chrome(options=chrome_options)

# *********************************************
# CONFIGURE URL TO SCRAP
# *********************************************
url: str = "https://www.cio.com/search?q=certifications"

# *********************************************
# START SELENIUM
# *********************************************
cio_articles: dict[str, str] = {}

# Set timeout time
wait = WebDriverWait(driver, 10)
# retrieve url in headless browser
driver.get(url)

result_wrapper: WebElement = driver.find_element(By.CSS_SELECTOR, "div.gsc-results.gsc-webResult")
nb_pages: int = len(driver.find_elements(By.CSS_SELECTOR, "div.gsc-cursor > div.gsc-cursor-page"))
idx_page: int = 1

while idx_page <= nb_pages:

    css_selector: str = ".gsc-cursor-page:nth-child({})".format(idx_page)
    page = driver.find_element(By.CSS_SELECTOR, css_selector)
    page.click()
    print(result_wrapper.get_attribute('class'))
    WebDriverWait(driver, 5).until(lambda d: 'gsc-loading-resultsRoot' not in result_wrapper.get_attribute('class'))

    results: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, "a.gs-title")

    for result in results:
        if len(result.accessible_name) > 1:
            cio_articles[result.accessible_name] = result.get_attribute("href")

    idx_page += 1
    print()

# must close the driver after task finished
driver.close()
driver.quit()
