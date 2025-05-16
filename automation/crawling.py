from bs4 import BeautifulSoup as bs
import threading
from automation import driver
import time
from ai import gpt
from random import shuffle

import requests

# BASE_URL = "https://www.ibabynews.com"
# URL = [
#     {"category": "육아/교육", "link": "/news/articleList.html?sc_section_code=S1N4&view_type=sm"},
#     {"category": "여성/가족", "link": "/news/articleList.html?sc_section_code=S1N8&view_type=sm"},
#     {"category": "오피니언", "link": "/news/articleList.html?sc_section_code=S1N6&view_type=sm"},
# ]


BASE_URL = "https://m.entertain.naver.com/now"
NAVER_IT_URL = "https://news.naver.com/breakingnews/section/105/230"
NAVER_SOCIAL_URL = "https://news.naver.com/breakingnews/section/102/250"
IBOSS_URL = "https://www.i-boss.co.kr/ab-7214"
GOOGLE_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako"

LIST_LEN = 20

is_chrome_init = False

news_list = {}

def get_data_naver_social():
    driver.get_url(NAVER_SOCIAL_URL)

    time.sleep(2)

    print("크롤링을 시작합니다...")
    soup = bs(driver.get_pagesource(), 'lxml')

    lists = soup.find_all("li4", class_=lambda x: x and 'sa_item _LAZY_LOADING_WRAP' in x)
    print(len(lists))
    body_lists = soup.find_all("div", class_=lambda x: x and 'sa_text_lede' in x)

    a_tag_list = [li.find("a", href=True)["href"] for li in lists if li.find("a", href=True)]
    body_link_list = [[body_lists[i].text[:250], a_tag_list[i]] for i in range(len(a_tag_list))]
    print(a_tag_list)
    print(body_link_list)

    print("링크와 본문을 출력합니다...")
    for i in range(len(a_tag_list)):
        print("a_tag_list = " + body_link_list[i][0])
        print("body_link_list = " + body_link_list[i][1])
        print()
    time.sleep(2)


# 네이버 뉴스 크롤링
def get_data_naver_IT():

    driver.get_url(NAVER_IT_URL)

    time.sleep(2)

    print("크롤링을 시작합니다...")
    soup = bs(driver.get_pagesource(), 'lxml')

    lists = soup.find_all("li", class_=lambda x: x and 'sa_item _LAZY_LOADING_WRAP' in x)
    print(len(lists))
    body_lists = soup.find_all("div", class_=lambda x: x and 'sa_text_lede' in x)

    a_tag_list = [li.find("a", href=True)["href"] for li in lists if li.find("a", href=True)]
    body_link_list = [[body_lists[i].text[:250], a_tag_list[i]] for i in range(len(a_tag_list))]
    print(a_tag_list)
    print(body_link_list)

    print("링크와 본문을 출력합니다...")
    for i in range(len(a_tag_list)):
        print("a_tag_list = " + body_link_list[i][0])
        print("body_link_list = " + body_link_list[i][1])
        print()
    time.sleep(2)

# 네이버 뉴스 크롤링 (링크만 가져와서 건네주기)
def crawl_lists():
    try:
        global BASE_URL, is_chrome_init
        news_list.clear()
        if is_chrome_init is False:
            driver.init_chrome()
            is_chrome_init = True


        get_data_naver_IT()

        # soup = bs(driver.get_pagesource(), 'lxml')
        #
        # lists = soup.find_all("li", class_=lambda x: x and 'NewsItem_news_item__' in x)
        # body_lists = soup.find_all("p", class_=lambda x: x and 'NewsItem_description__' in x)
        #
        # a_tag_list = [li.find("a", href=True)["href"] for li in lists if li.find("a", href=True)]
        # body_link_list = [[body_lists[i].text[:250], a_tag_list[i]] for i in range(25)]
        #
        # if a_tag_list:
        #     print(len(a_tag_list))
        #     print("GPT와 작업을 시도합니다.")
        #     news_list['link'] =gpt.get_related_url(body_link_list)
        #
        #     time.sleep(3)
        #
        #     # gpt 확인 후 다음 해제
        #     driver.get_url(news_list['link'])
        #     body = driver.get_body()
        #
        #     # title, body = gemini.get_title_body(body)
        #     title, body = gpt.get_title_body(body)
        #     news_list['title'] = title
        #     news_list['body'] = body
        #
        # print(f"a_tag_list 길이: {len(a_tag_list)}")
        # print(f"선택된 링크: {news_list.get('link')}")
        # print(f"생성된 타이틀: {news_list.get('title')}")
    except Exception as e:
        print(f"[ERROR] 크롤링 중 예외 발생: {e}")

def get_paragraph(article_url):
    response = requests.get(article_url)
    article_text = ""  # 기사 내용을 저장할 변수 초기화

    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            if p is not None:
                text = p.get_text(strip=True)
                if text is not None and len(text) > 0:
                    # print(text)
                    article_text += text + "\n"  # 추출된 텍스트를 변수에 추가

        return article_text if len(article_text) > 0 else None  # 내용이 있으면 반환, 없으면 None 반환
    return None


def crawl_lists_title():
    try:
        global BASE_URL, is_chrome_init
        news_list.clear()
        if is_chrome_init is False:
            driver.init_chrome()
            is_chrome_init = True
        article_list = from_naver(NAVER_IT_URL)
        article_list += from_naver(NAVER_SOCIAL_URL) + from_iboss() + from_google()

        # 뒤에도 보게 하도록 리스트를 랜덤하게 셔플
        print("기사를 랜덤하게 셔플합니다.")
        shuffle(article_list)
        print("=============== 섞은 후 (예시 10개) ===============")


        # 출력 코드
        for i in range(10):
            print("title = " + article_list[i][0])
            print("title = " + article_list[i][1])
            print("-----------------------------------------------------------------")
        print("===============================================================")

        print("GPT에게 응답을 요구합니다...")
        index = 100000
        while index >= len(article_list) or index < 0:
            index = gpt.get_related_index(article_list)

        news_list['link'] = article_list[index][1]
        news_list['title'] = article_list[index][0]
        news_list['body'] = gpt.get_body_from_url(article_list[index][1], news_list['title'])

        print("============== news list ==============")
        link = news_list['link']
        if "iboss" in link:
            print("source = 아이보스")
        elif "google" in link:
            print("source = 구글")
        elif "naver" in link:
            print("source = 네이버")
        print("title = " + news_list['title'])
        print("body = " + news_list['body'])
        print("link = " + news_list['link'])

    except Exception as e:
        print(f"[ERROR] 크롤링 중 예외 발생: {e}")



def from_naver(url):
    driver.get_url(url)

    time.sleep(2)
    print("네이버에서 기사를 긁어옵니다...")

    soup = bs(driver.get_pagesource(), 'lxml')

    lists = soup.find_all("li", class_=lambda x: x and 'sa_item _LAZY_LOADING_WRAP' in x)

    title_list = soup.find_all("strong", class_=lambda x: x and 'sa_text_strong' in x)
    href_list = [li.find("a", href=True)["href"] for li in lists if li.find("a", href=True)]

    time.sleep(2)
    return [[title_list[i].text, href_list[i]] for i in range(LIST_LEN)]

def from_iboss():
    driver.get_url(IBOSS_URL)

    time.sleep(2)
    print("아이보스에서 기사를 긁어옵니다...")
    soup = bs(driver.get_pagesource(), 'lxml')

    # 1. span.subject_text 아래 있는 a 태그 모두 찾기
    articles = soup.find_all("span", class_="subject_text")
    title_list = []
    href_list = []

    for a in articles:
        a_tag = a.find("a", href=True)
        if a_tag:
            title_list.append(a_tag.text.strip())
            href_list.append(IBOSS_URL + a_tag["href"])

    time.sleep(2)
    return [[title_list[i], href_list[i]] for i in range(min(20, len(title_list), len(href_list)))]

def from_google():
    driver.get_url(GOOGLE_URL)

    time.sleep(2)
    print("구글뉴스에서 기사를 긁어옵니다...")
    soup = bs(driver.get_pagesource(), 'lxml')

    # 1. span.subject_text 아래 있는 a 태그 모두 찾기
    articles = soup.find_all("article")
    title_list = []
    href_list = []

    for article in articles:
        a_tags = article.find_all("a", href=True)
        for a in a_tags:
            text = a.get_text(strip=True)
            if text:  # 내용이 있는 a 태그만 대상
                title_list.append(text)
                href_list.append(GOOGLE_URL + a["href"])
                break  # 제목 있는 a 하나만 가져오면 됨
        # for a in a_tag:
        #     text = a.get_text(strip=True)
        #     print("text = " + text)
        #     if text:
        #         title_list.append(text)
        #         href_list.append(GOOGLE_URL + a_tag["href"])
        #         break

    time.sleep(2)
    return [[title_list[i], href_list[i]] for i in range(min(20, len(title_list), len(href_list)))]
