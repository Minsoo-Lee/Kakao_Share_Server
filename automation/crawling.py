from bs4 import BeautifulSoup as bs
import threading
from automation import driver
import time
from ai import gpt

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
index = 0

# URL = f"{BASE_URL}/news/articleList.html?sc_sub_section_code=S2N1&view_type=sm"

news_list = {}

# www.ibabynews.com 크롤링
# def crawl_lists():
#     global URL, BASE_URL, index
#     news_list.clear()
#     log.append_log("크롤링을 시작합니다.")
#     response = requests.get(BASE_URL + URL[index]['link'])
#     print(f"======= request url = [{BASE_URL + URL[index]['link']}] =======================")
#     gemini.init_gemini()
#
#     if response.status_code == 200:  # 정상 응답 반환 시 아래 코드블록 실행
#         soup = bs(response.content, 'html.parser')  # 응답 받은 HTML 파싱
#         lists = soup.find_all("div", {"class": 'list-block'})
#
#         # 차라리 여기서 3개를 추출하는 것이 빠를지도
#         # 아직 컨셉이 잡힌 것이 없으니 놔두자
#         for i in range(3):
#             article_info = {}
#
#             # 링크 추출
#             a_tag = lists[i].find("a", href=True)
#             article_url = BASE_URL + a_tag["href"]
#             article_info["url"] = article_url
#
#             # 날짜 추출
#             date_div = lists[i].find("div", class_="list-dated")
#             tmp_text = date_div.get_text(strip=True)
#             date_text = tmp_text.split("|")[2].strip().split(" ")[0]
#             article_info["date"] = date_text
#
#             # 이미지 소스 추출
#             # img_tag = lists[i].find("img", src=True)
#             # print(f"img_tag: {img_tag}")
#             # img_url = BASE_URL + img_tag["src"][1:]
#             # print(f"img_url: {img_url}")
#             # article_info["img"] = img_url
#
#             # 제목 추출
#             # 쓰레드 동기화가 걸린다면, 이건 나중에 추가하는 것도 고려해볼 만 함
#             # 빠른 테스트를 위해 제목 고정
#             # 원래는 이거로 동적 생성
#             paragraph = get_paragraph(article_url)
#             title = gemini.get_response(paragraph)
#             article_info["title"] = title
#             # article_info["title"] = "title"
#
#             response = requests.get(article_url)
#             if response.status_code == 200:
#                 soup_img = bs(response.content, 'html.parser')
#                 lists_img = soup_img.find_all("div", {"class": 'IMGFLOATING'})
#                 print(len(lists_img))
#
#                 if len(lists_img) == 0:
#                     article_info["img"] = None
#                 else:
#                     img_tag = lists_img[0].find("img", src=True)
#                     img_url = BASE_URL + img_tag["src"]
#                     article_info["img"] = img_url
#                     print(img_url)
#
#
#             # description 은 "육아"로 고정
#             article_info["description"] = URL[index]['category']
#
#             news_list.append(article_info)
#     # print(json.dumps(news_list, indent=4, ensure_ascii=False))
#     log.append_log("크롤링이 완료되었습니다.")
#     index += 1

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
        for i in range(len(article_list)):
            print("title = " + article_list[i][0])
            print("title = " + article_list[i][1])
            if (i + 1) % 20 == 0:
                print("===============================================================")
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
