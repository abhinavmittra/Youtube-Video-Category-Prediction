from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
# import requests
# print("Enter your search")
# query=input()
# source = requests.get("https://www.youtube.com/results?search_query="+query).text


print("Enter your search")
query=input()
driver = webdriver.Chrome(r"C:\Users\Abhinav\Downloads\chromedriver.exe")
driver.get("https://www.youtube.com/results?search_query="+query)
SCROLL_PAUSE_TIME = 1
source = driver.page_source.encode('utf-8')

i=1
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while i<5:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    i=i+1
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
       print("break")
       break
    last_height = new_height
time.sleep(1)
source = driver.page_source.encode('utf-8')
print(source)
soup = BeautifulSoup(source, 'lxml')
video_dict = {'youId':[],'title':[], 'description':[],'category':[]}
keyword=query.replace(" ","")
for content in soup.find_all('div', class_= "yt-lockup-content"):
    try:
        title = content.h3.a.text
        x=content.h3.a['href']
        youId=x[x.index('=')+1:]
        description = content.find('div', class_="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2").text
        print(title)
        print(description)
        print(youId)
    except Exception as e:
        description = None
    video_dict['title'].append(title)
    video_dict['description'].append(title)
    video_dict['category'].append(keyword)
    video_dict['youId'].append(youId)
pdf = pd.DataFrame.from_dict(video_dict)
#pdf.to_csv(query+'.csv')