from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = "https://www.reuters.com/search/news?blob=soybean&sortBy=date&dateRange=all"
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(r"C:\Users\Abhinav\Downloads\chromedriver.exe")
driver.get(url)
html = driver.page_source.encode('utf-8')
page_num = 0

#while driver.find_elements_by_css_selector('.search-result-more-txt'):
while page_num<10:
    driver.find_element_by_css_selector('.search-result-more-txt').click()
    page_num += 1
    print("getting page number "+str(page_num))
    time.sleep(1)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'lxml')
links = soup.find_all('div', attrs={"class":'search-result-indiv'})
articles = [a.find('a')['href'] for a in links if a != '']
print(articles)