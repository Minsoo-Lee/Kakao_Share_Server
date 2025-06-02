from bs4 import BeautifulSoup as bs
from config.url import *
import re

import requests

def from_ai_times(index):
    news_maps = {}
    print("AI 타임즈에서 기사를 수집합니다...")
    response = requests.get(NEWS_LINKS[index] + SUB_LINKS[index])

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        titles = soup.select("h4.titles")

        for title in titles:
            a_tag = title.select_one("a")
            text = re.sub(r"\[.*?]\s*", "", a_tag.get_text().strip())
            news_maps[text] = NEWS_LINKS[index] + a_tag["href"]

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

def from_ai_times_kr(index):
    news_maps = {}
    print("인공지능신문에서 기사를 수집합니다...")
    response = requests.get(NEWS_LINKS[index] + SUB_LINKS[index])

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        titles = soup.select("h4.titles")

        for title in titles:
            a_tag = title.select_one("a")
            news_maps[a_tag.get_text()] = NEWS_LINKS[index] + a_tag["href"]

    for key, value in news_maps.items():
        print(f"key = {key}")
        print(f"value = {value}")

    return news_maps

def body_from_ai_times_kr(link):
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

def from_the_ai(index):
    news_maps = {}
    print("인공지능신문에서 기사를 수집합니다...")
    response = requests.get(NEWS_LINKS[index] + SUB_LINKS[index])

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        titles = soup.select("h2.titles")

        for title in titles:
            a_tag = title.select_one("a")
            news_maps[a_tag.get_text().strip()] = NEWS_LINKS[index] + a_tag["href"]

    for key, value in news_maps.items():
        print(f"key = {key}")
        print(f"value = {value}")

    return news_maps

def body_from_the_ai(link):
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

def from_ai_matters(index):
    news_maps = {}
    print("인공지능신문에서 기사를 수집합니다...")
    response = requests.get(NEWS_LINKS[index])

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        titles = soup.select("h4.ultp-block-title")

        for title in titles:
            a_tag = title.select_one("a")
            news_maps[a_tag.get_text().strip()] = a_tag["href"]

    for key, value in news_maps.items():
        print(f"key = {key}")
        print(f"value = {value}")

    return news_maps

def body_from_ai_matters(link):
    response = requests.get(link)

    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        article_div = soup.find("div", class_="ultp-builder-content")
        p_tags = article_div.find_all("p")
        body = ""
        for p_tag in p_tags:
            if "뉴스입니다" in p_tag.get_text():
                break
            body += p_tag.get_text() + "\n"

        return body
    else: return None

crawl_function_list = [from_ai_times, from_ai_times_kr, from_the_ai, from_ai_matters]
crawl_body_list = [body_from_ai_times, body_from_ai_times_kr, body_from_the_ai, body_from_ai_matters]