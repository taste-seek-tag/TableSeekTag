from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time, os

ROOT_PATH    = '/config/workspace/project'
PROJECT_PATH = f'{ROOT_PATH}/MidnightTable/TableSeekTag/src'
DATASET_PATH = f'{PROJECT_PATH}/data/zomato'

## chromedriver의 위치 입니다.
driver_path = f'{ROOT_PATH}/utils/'

## scraping 해주는 함수 입니다.
def scraping(url):
    driver.get(url)
    return driver.find_elements(By.CSS_SELECTOR, '#root > div > main > div')


csv = pd.read_csv(f'{DATASET_PATH}/HyderabadResturants.csv')
total_cuisine = []

## csv에서 cuisine 데이터만 모으는 부분 입니다.
cuisines = [cuisine.split(', ') for cuisine in csv['cuisine']]
for cuisine in cuisines: total_cuisine.extend([cuisine for cuisine in cuisine])


options = webdriver.ChromeOptions()

## 개인 데이터 서버에 올린 도커 vscode server를 이용하여 headless로 진행하였습니다.
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

## headless로 진행하였을 때 zomato 식당 페이지에 접속하면, 403 forbidden이 나와
## headless 상태에서도 접근할 수 있도록 Agent를 옵션으로 추가해 주었습니다.
options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')

driver = webdriver.Chrome(f'{driver_path}/chromedriver', chrome_options = options)
os.makedirs(f'{DATASET_PATH}/scraping_datas', exist_ok = True)

try:
    for idx, link in enumerate(csv['links'], 1):
        start_time = time.time()
        
        try: elements = scraping(link)[0].text
        except: pass

        open(f'{DATASET_PATH}/scraping_datas/scraping_{str(idx).zfill(5)}.txt', 'w').write(elements)
        print(f'[{str(idx).zfill(5)} / {str(len(csv["links"])).zfill(5)}] spent time | {time.time() - start_time:2f} (sec)')
        time.sleep(1)

except Exception as e: print(f'[ERROR] \n\n{e}\n\n')
finally: driver.quit()
