import traceback

from bs4 import BeautifulSoup as bs
import threading

from pyasn1_modules.rfc6402 import bodyIdMax

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
IBOSS_URL = "https://www.i-boss.co.kr"
# GOOGLE_URL = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtdHZHZ0pMVWlnQVAB?hl=ko&gl=KR&ceid=KR%3Ako"
GOOGLE_URL = "https://www.google.com/search?sca_esv=9a5e0d52e8e6d667&sxsrf=AHTn8zpgotSk2g98GiUyDIt0zAI2JvIJwQ:1747397951848&q=%EA%B5%90%EC%9C%A1&tbm=nws&source=lnms&fbs=ABzOT_CZsxZeNKUEEOfuRMhc2yCIN42EXxa9ZSNEwtiPEbQrp-oREuj69PlSffsqaZff35ttlTfDht-WBlJ2aWSHHA1tbDwCB-lbeuNcJdOYidBlctfWWHzdvZiE_XhVRdtnTJhPIpOPMz9G8fuPY-9ugU3rcYoKVhtXR2vHa1EnDoKao07ACNN9l-1Xib0UvA7f7ZjkeMj4I2LmKtS6iT-8ojUPBGEifg&sa=X&ved=2ahUKEwjk5M3R_KeNAxXgklYBHSAqANEQ0pQJegQIHBAB&biw=1365&bih=934&dpr=1"

is_chrome_init = False

news_list = {}

### AI 단톡방을 타겟으로 한 서비스 ###
AI_TIMES = "https://www.aitimes.com"
AI_TIMES_KR = "https://www.aitimes.kr/news/articleList.html?page=1&total=20190&sc_section_code=&sc_sub_section_code=&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&box_idxno=&sc_multi_code=&sc_is_image=&sc_is_movie=&sc_user_name=&sc_order_by=E&view_type=sm"
THE_AI = "https://www.newstheai.com/news/articleList.html?view_type=sm"
AI_METRO = "https://aimatters.co.kr/category/news-report/ai-news"

# 한시간마다 돌아가면서 크롤링하기 때문
NEWS_LINKS = [AI_TIMES, AI_TIMES_KR, THE_AI, AI_METRO]  # 리스트를 돌아가면서 순회
news_index = 0
news_map = {}


def crawl_news():
    try:
        global BASE_URL, is_chrome_init
        news_list.clear()
        if is_chrome_init is False:
            driver.init_chrome()
            is_chrome_init = True

        news_maps = from_ai_times()
        title_list = []
        for key, value in news_maps.items():
            title_list.append(key)

        index = gpt.get_related_title(title_list)
        title = title_list[index]
        link = news_maps[title]

        body = body_from_ai_times(news_maps[title_list[index]])
        summary = gpt.summarize_body(body)

        # summary = summary.replace('1.', '1️⃣')
        # summary = summary.replace('2.', '2️⃣')
        # summary = summary.replace('3.', '3️⃣')

        for i in range(1, 4):
            summary = summary.replace(f"{i}.", f"{i}️⃣")

        print(summary)

        news_list['title'] = title
        news_list['summary'] = summary
        news_list['link'] = link

        # print("GPT에게 응답을 요구합니다...")
        # index = get_one(article_list)
        #
        # news_list['link'] = article_list[index][1]
        # news_list['title'] = article_list[index][0]
        # news_list['body'] = gpt.get_body_from_url(article_list[index][1], news_list['title'])

    except Exception as e:
        print(f"[ERROR] 크롤링 중 예외 발생: {e}")


def from_ai_times():
    news_maps = {}
    print("AI 타임즈에서 기사를 수집합니다...")
    response = requests.get(AI_TIMES + "/news/articleList.html?sc_sub_section_code=S2N110&view_type=sm")

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        titles = soup.select("h4.titles")

        for title in titles:
            a_tag = title.select_one("a")
            news_maps[a_tag.get_text()] = AI_TIMES + a_tag["href"]

    return news_maps

def body_from_ai_times(link):
    response = requests.get(link)

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        article_div = soup.find("article", id="article-view-content-div")
        p_tags = article_div.find_all("p")
        body = ""
        for p_tag in p_tags:
            if "뉴스입니다" in p_tag.get_text():
                break
            body += p_tag.get_text() + "\n"

        return body
    else: return None


### 예전 코드들 (키즈 에이전시 포함) ###

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
        # article_list = from_naver(NAVER_IT_URL)
        # article_list += from_naver(NAVER_SOCIAL_URL) + from_iboss() + from_google()

        # 1개씩 가져올 경우 다르게
        article_list = from_naver(NAVER_IT_URL)
        article_list.extend(from_naver(NAVER_SOCIAL_URL))
        # article_list.append(from_iboss())
        article_list.extend(from_google())
        print(gpt.get_related_index(article_list))

        print("GPT에게 응답을 요구합니다...")
        index = get_one(article_list)

        news_list['link'] = article_list[index][1]
        news_list['title'] = article_list[index][0]
        news_list['body'] = gpt.get_body_from_url(article_list[index][1], news_list['title'])

        print("============== news list ==============")
        link = news_list['link']
        if "i-boss" in link:
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

    # return [[title_list[i].text, href_list[i]] for i in range(LIST_LEN)]

    article_list = [[title_list[i].text, href_list[i]] for i in range(len(title_list))]
    # for i in range(len(article_list)):
    #     print(article_list[i][0])
    # index = get_one(article_list)

    # 출력결과
    # print("title = " + article_list[index][0])
    # print("title = " + article_list[index][1])
    # return article_list[index]
    return article_list


def from_iboss():
    driver.get_url(IBOSS_URL + "/ab-7214")

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
    # return [[title_list[i], href_list[i]] for i in range(min(20, len(title_list), len(href_list)))]
    article_list = [[title_list[i], href_list[i]] for i in range(len(title_list))]
    for i in range(len(article_list)):
        print(article_list[i][0])
    index = get_one(article_list)

    # print("title = " + article_list[index][0])
    # print("title = " + article_list[index][1])
    return article_list[index]


def from_google():
    driver.get_url(GOOGLE_URL)

    time.sleep(2)
    print("구글뉴스에서 기사를 긁어옵니다...")
    soup = bs(driver.get_pagesource(), 'lxml')

    # n0jPhd ynAwRc tNxQIb nDgy9d

    title_lists_1 = soup.find_all("div", class_=lambda x: x and 'n0jPhd ynAwRc tNxQIb nDgy9d' in x)
    title_lists_2 = soup.find_all("div", class_=lambda x: x and 'n0jPhd ynAwRc MBeuO nDgy9d' in x)
    title_list = []
    for title_div in title_lists_1:
        text = title_div.get_text(strip=True)  # 또는 title_div.text.strip()
        title_list.append(text)
    for title_div in title_lists_2:
        text = title_div.get_text(strip=True)  # 또는 title_div.text.strip()
        title_list.append(text)

    url_lists = soup.find_all("a", class_=lambda x: x and 'WlydOe' in x)
    href_list = [li['href'] for li in url_lists if li.has_attr('href')]
    # print(title_list)

    # for title in title_list:
    #     print(title)
    # for url in href_list:
    #     print(url)

    time.sleep(2)
    # return [[title_list[i], href_list[i]] for i in range(min(20, len(title_list), len(href_list)))]
    article_list = [[title_list[i], href_list[i]] for i in range(len(title_list))]
    # index = get_one(article_list)

    # print("title = " + article_list[index][0])
    # print("title = " + article_list[index][1])
    # return article_list[index]
    return article_list


def get_one(article_list):
    index = len(article_list)
    while index >= len(article_list) or index < 0:
        index = gpt.get_related_index(article_list)
    return index
