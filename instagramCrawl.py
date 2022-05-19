from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

usrnme = input("Instagram account ID: ")
pswd = input("Instagram account PW: ")

target = []

while True:
    tgt = input("Please enter the target ID (Enter F to stop): ")
    if tgt.lower() != 'f':
        target.append(tgt)
    else:
        break

username = usrnme
password = pswd
driver_path = '.\chromedriver.exe'



options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")

driver = webdriver.Chrome(driver_path,options=options)

try:
    os.makedirs(f'./instaImages')
except:
    print("Main folder already exists")

time.sleep(2)
## url에 접근한다.
driver.get('https://www.instagram.com')
time.sleep(1)
driver.find_element_by_name("username").send_keys(username)
time.sleep(1)
driver.find_element_by_name("password").send_keys(password)
time.sleep(2)
driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[3]/button").click()
time.sleep(3)
for targ in target:
    driver.get(f'https://www.instagram.com/{targ}/')
    last_height = driver.execute_script("return document.body.scrollHeight")
    images = []
    try:
        os.makedirs(f'./instaImages/{targ}')
    except:
        print(f"{targ} folder already exists")

    count = 0
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        html = driver.page_source
        bs = BeautifulSoup(html, 'html.parser')
        imgs = bs.find_all('img', {'class': 'FFVAD'})
        for i in imgs:
            if i['src'] not in images:
                # print(i['src'])
                images.append(i['src'])
                urllib.request.urlretrieve(i['src'], f'./instaImages/{targ}/{count}.jpg')
                count += 1
    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')
    imgs = bs.find_all('img', {'class': 'FFVAD'})
    for i in imgs:
        if i['src'] not in images:
            # print(i['src'])
            images.append(i['src'])
            urllib.request.urlretrieve(i['src'], f'./instaImages/{targ}/{count}.jpg')
            count += 1
    if count == 0:
        print(f'Account {targ} is private')
    else:
        print(f'{targ}: {len(images)}')





