from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import threading
from automation import driver
import time
from ai import gpt

import requests

url="https://n.news.naver.com/mnews/article/016/0002471881"

chrome_options = Options()

# ✅ 필수: Headless 서버 환경에서 필요한 옵션
chrome_options.add_argument('--headless')  # 화면 없이 실행
chrome_options.add_argument('--no-sandbox')  # 보안 샌드박스 비활성화
chrome_options.add_argument('--disable-dev-shm-usage')  # 메모리 사용 제한 해제
chrome_options.add_argument('--disable-gpu')  # GPU 비활성화 (가끔 필요)
chrome_options.add_argument('--window-size=1920x1080')  # 뷰포트 설정

# 선택 옵션
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})
chrome_options.add_experimental_option("detach", True)

# ChromeDriver 경로가 환경에 따라 다르다면 명시 필요
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

soup = bs(driver.page_source, 'lxml')

# 1. span.subject_text 아래 있는 a 태그 모두 찾기
articles = soup.find("article", class_="go_trans _article_content")
print(articles.text)