from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

# Start Selenium Because the website use SPA

# Get all the pages according the the pagination

# Loop through each page (click on each page button to load the result)



# ChromeDriver.exe has been added to PATH
driver = webdriver.Chrome()

text: str = "certifications"
url: str = "https://www.cio.com/search?q=" + text

driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")

#links = soup.find_all("a", attrs={"class": "gs-title"})
pages = soup.select("div.gsc-cursor > div.gsc-cursor-page")

for page in pages:
    el = driver.find_element(By.TAG_NAME, page.name)
    el.click()

    links = soup.select(".gsc-table-cell-thumbnail > a.gs-title")

    for link in links:
        if len(link.text) > 1:
            print(link.text + " " + link.get("href"))

driver.quit()



#for link in links:

