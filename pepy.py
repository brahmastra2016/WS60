# https://stackoverflow.com/questions/41435983/selenium-in-python-on-mac-geckodriver-executable-needs-to-be-in-path
# https://github.com/mozilla/geckodriver/releases

from gazpacho import Soup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import requests
import re

url = 'https://pepy.tech/project/gazpacho'
options = Options()
options.headless = True
browser = Firefox(executable_path='/usr/local/bin/geckodriver', options=options)
browser.get(url)
html = browser.page_source
print(html)
soup = Soup(html)
results = soup.find('tr', {'class': 'MuiTableRow-root'})
results
results[1].find('td').text
results[2].find('td').text)
