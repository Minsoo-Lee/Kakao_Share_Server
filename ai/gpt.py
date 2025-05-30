from collections import deque

import openai
import os
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, \
    ChatCompletionUserMessageParam

# .env 파일에서 API 키 불러오기
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("API_KEY"))

### 새 코드 (AI 단톡방 타겟) ###
openai.api_key = os.getenv("API_KEY")
prev_list = deque(maxlen=20)

def get_related_title(title_list):
    prompt = f"""
                내가 AI 기사 제목들을 보여 줄게.

                {title_list}
                
                참고로 너는 이전에 다음 기사들을 골랐어:
                {list(prev_list)}
        
                이 기사 제목들을 전부 확인하고, AI 관련된 일을 하는 사람들이 가장 필요로 할 기사 제목의 인덱스를 하나 말해줘.
                대신에, 너가 전에 골랐던 기사들은 반드시 피해 줘.
                다른 말 하지 말고, 너가 선택한 기사 제목의 인덱스를 숫자로만 그대로 말해줘.
                """

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )

    # GPT가 고른 인덱스
    index = int(response.output_text)
    title = title_list[index]

    # 제목 저장 (자동으로 오래된 건 제거됨)
    prev_list.append(title)

    return index

# 본문을 스크랩해 오는 경우 토큰이 너무 많이 낭비될 우려가 있음
# 따라서, 본문을 스크랩해 오는 대신 link를 접속하는 방식으로 전환
# 정확성이 많이 떨어질 경우 본문을 스크랩해 오는 방식으로 대체 -> 아예 링크를 접속 못한다고 선그음... 본문을 전달하는거로...

def summarize_body(body):
    prompt = f"""
            내가 AI 기사를 보여 줄게.

            {body}

            첫 번째로, 반드시 이 기사 본문을 꼼꼼히 읽어줘.
            그 후에, 너가 꼼꼼하게 읽은 내용을 다음과 같은 형태로 3줄로 요약해 줘.
            요약한 내용들은 각 번호마다 공백 포함 100자 이내로, 명사형으로 끝나게 해.
            
            1. (너가 요약한 내용 1)
            2. (너가 요약한 내용 2)
            3. (너가 요약한 내용 3)
            
            반드시 저 틀을 지켜서 해줘.
            """

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )

    return response.output_text


def get_why_important(summary):
    prompt = f"""
            너가 방금 요약해준 AI 기사를 보여 줄게.
            
            {summary}

            첫 번째로, 반드시 이 요약본을 꼼꼼히 읽어줘.
            그 후에, 너가 꼼꼼하게 읽은 내용을 바탕으로 이 기사가 왜 중요한지 설명해 줘.
            그 내용은 공백 포함 150자 이내로 해 줘. 말투는 친근하게 부탁해.
            그리고 왜 중요한지 설명만 응답으로 건네줘.

            반드시 저 틀을 지켜서 해줘.
            """

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=prompt,
    )

    return response.output_text


### 예전 코드 (키즈 에이전시 관련) ###

def get_related_index(article_list):
    # prompt = f"""
    #     내가 너에게 보내준 {body_urls}은 엔터 관련 뉴스들로 구성되어있어.
    #     각 행마다 1열은 본문 요약본, 2열은 링크가 들어 있어.
    #     본문을 모두 다 읽고, 학부모들에게 보여주면 좋을만한 기사 url 하나만 뽑아서 출력해줘. 다음과 같은 조건을 갖추어야해.
    #
    #     1. 기사를 선별하는 이유는 자녀를 엔터사업쪽으로 키우려는 부모님들을 위한 일이야.
    #     따라서 "키즈"와 "엔터", "학부모"가 겹치는 기사를 선별해야 하는데, "학부모"를 1순위, "키즈"를 2순위로 고려해.
    #     2. 반드시 모든 본문들을 다 확인한 후에 가장 관련성이 높은 기사를 하나만 말해.
    #     3. 다른말 필요 없이 url만 말해줘. 특히 하이픈(-)이나 쌍따옴표("), 홑따옴표(')같은 특수문자는 절대로 쓰지마. 절대.
    #         오로지 url만 말해줘.
    #     4. 너가 선택한 본문이 1번에 부합하는지 반드시 다시 확인해 봐. 아니면 다시 1번을 수행해.
    #     5. 1~4까지의 과정 중 하나라도 지켜지지 않은게 있다면 다시 답변을 생성해.
    #     """
        # 출력은 다른 말 필요 없이 url만 건네줘.

    # prompt = f"""
    #         내가 너에게 보내준 {article_list}은 엔터 관련 뉴스들로 구성되어있어.
    #         각 행마다 1열은 제목, 2열은 링크가 들어 있어.
    #         제목을 모두 다 읽고, 다음과 같은 조건을 갖춘 제목의 url의 인덱스 하나만 뽑아서 출력해 줘.
    #
    #         1. 기사를 선별하는 이유는 "키즈 에이전시" 관련 엔터 기사에 흥미가 있는 고객들에게 유의미한 정보를 제공하기 위해서야.
    #             아래의 우선순위대로 기사를 추출해 줘. 반드시 아래 우선순위와 관련 있는 기사여야 해.
    #             1) 키즈 에이전시
    #             2) 육아
    #             3) 교육
    #
    #         2. 반드시 모든 제목들을 다 확인한 후에 가장 관련성이 높은 기사를 하나만 말해.
    #         3. 다른말 필요 없이 인덱스 숫자만 말해줘. 특히 하이픈(-)이나 쌍따옴표("), 홑따옴표(')같은 특수문자는 절대로 쓰지마. 절대.
    #             오로지 인덱스 숫자만 말해줘.
    #         4. 너가 선택한 본문이 1번에 부합하는지 반드시 다시 확인해 봐. 아니면 다시 1번을 수행해.
    #         5. 1~4까지의 과정 중 하나라도 지켜지지 않은게 있다면 다시 답변을 생성해.
    #         6. 무슨 일이 있더라도 다른 말 하지 말고, 반드시 인덱스를 정수형으로만 말해줘. 제목도 말 하지 말고 오로지 인덱스로만 답변해 줘
    #         """

    prompt = f"""
            내가 1열은 제목, 2열은 링크가 들어 있는 뉴스 기사 제목들 리스트를 보여줄게.
            이 리스트 중에서 교육 카테고리와 가장 관련 있는 뉴스 기사를 추출할거야.
            
            {article_list}
            
            다른 말 필요 없이, 대괄호 빼고 무조건 인덱스 숫자로만 말해줘. 너가 반환한 숫자를 파이썬에서 int로 형변환할 거야.
            """

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            # {"role": "system", "content": "너는 키즈에이전시 관계자야. 너는 많은 학부모들을 관리하고 있으며 그들에게 유의미한 정보를 전달하려고 해."},
            # {"role": "system", "content": "너는 엔터테인먼트 기사를 다루는 마케터야. 고객들이 원하는 주제를 가진 엔터테인먼트 기사를 하나 " +
            #                               "선별할 수 있는 능력이 있어"},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return int(content)


def get_title_body(body):
    print("GPT로부터 응답을 받아옵니다.")
    # print("=============body===========")
    # print(body)
    # print("============================")
    prompt = f"""
        여기 뉴스 기사가 있어.

        {body}

        이 기사를 읽고 제목을 15자가 넘지 않게, 본문은 150자 이내로 요약해 줘.
        그리고 문장 요약할 때 특수문자는 , . 이 두개만 써야 해. 다른 건 절대 쓰지 마
        물음표, 느낌표도 절대 쓰지마 제발 하지 말라는건 하지 마.
        쌍따옴표("), 홑따옴표(') 이 두개도 절대 쓰지 마
        그리고 제목과 본문 사이에 [!@#$%]라는 문자열을 넣어줘
        예시를 두 개 들어줄게.
        ================================================================================================================
        이시영, 아들과 사이판 여행 중[!@#$%]배우 이시영이 아들 정윤 군과 사이판 그로토에서 여행을 즐겼다. 스노클링 등 액티비티를 하며 추억을 쌓고, 식도락도 만끽했다. 이시영은 2017년 결혼해 2018년 아들을 출산했지만, 올해 초 이혼 절차를 밟고 있다. 드라마 꽃보다 남자, 넷플릭스 스위트홈 등 다양한 작품에 출연했다.
        ----------------------------------------------------------------------------------------------------------------
        매독, 조선을 공포로 몰아넣다[!@#$%]15세기 유럽, 콜럼버스가 아메리카 대륙에서 가져온 매독이 창궐, 1496년 이후 조선까지 전파되었다. 치료법을 몰라 사람의 간과 쓸개를 먹으면 낫는다는 미신이 퍼져, 사람 사냥과 시신 도굴이 만연했다. 선조는 포상금까지 내걸었지만, 매독은 페니실린 개발 전까지 인류를 공포에 떨게 했다. KBS 2TV 셀럽병사의 비밀에서 매독의 역사를 다룬다. 매주 화요일 오후 8시 30분 방송.
        ================================================================================================================
        처음 나오는게 제목이고, 나중에 나오는게 본문이야. 이제 잘 할 수 있지?
        """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 뉴스 기사를 주어진 조건에 맞게 일목요연하게 잘 요약하는 편집자입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    # print(content)
    result = content.split("[!@#$%]")
    # print(result)
    title = result[0].strip()
    body = result[1].strip()
    # print(title)
    # print(body)
    return title, body

def get_body_from_url(url, title):
    prompt = f"""
            여기 뉴스 기사 링크와 제목이 있어.

            링크: {url}
            제목: {title}

            이 링크에 접속해서 기사를 읽고, 본문을 140 ~ 150자로 정리해 줘.
            그리고 문장 요약할 때 특수문자는 , . 이 두개만 써야 해. 다른 건 절대 쓰지 마
            물음표, 느낌표도 절대 쓰지마 제발 하지 말라는건 하지 마.
            쌍따옴표("), 홑따옴표(') 이 두개도 절대 쓰지 마
            그리고 다음 사항들을 꼭 지켜줘.
            
            1. 반드시 링크에 접속해서 기사를 꼼꼼하게 읽어 줘.
            2. 핵심을 뽑아서, 너가 요약한 내용을 읽고도 이해가 갈 수 있도록 해야 해.
            3. 하이픈(-)이나 쌍따옴표("), 홑따옴표(')같은 특수문자는 절대로 쓰지마. 절대.
            4. 너가 선택한 요약한 본문이 제목과 부합하는지 반드시 다시 확인해 봐. 아니면 다시 1번을 수행해.
            5. 1~4까지의 과정 중 하나라도 지켜지지 않은게 있다면 다시 답변을 생성해.
            """

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "당신은 뉴스 기사를 주어진 조건에 맞게 일목요연하게 잘 정리하는 편집자입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    print(content)
    return content