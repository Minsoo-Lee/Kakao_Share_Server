from automation import driver, crawling as cr
from ai import gpt

news_maps = cr.crawl_function_list[3](3)
title_list = []
for key, value in news_maps.items():
    title_list.append(key)

index = gpt.get_related_title(title_list)

print(index)

title = title_list[index]
link = news_maps[title]

print(link)

body = cr.crawl_body_list[3](news_maps[title_list[index]])
summary = gpt.summarize_body(body)

print(summary)
print("=========================================================")
