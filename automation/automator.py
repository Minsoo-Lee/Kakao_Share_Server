import os
import threading
from datetime import datetime

from flask.cli import load_dotenv

from automation import driver
import time

from automation.driver import check_login_needed
from automation import crawling
from apscheduler.schedulers.background import BackgroundScheduler

from web import server

if_login_success = False
is_chrome_init = False
# is_server_init = False
chat_rooms = []

def start_task():
    global chat_rooms
    chat_rooms = os.getenv("ROOM").split(':')

    def safe_task():
        try:
            # if 19 <= datetime.now().hour <= 20:
            #     pass
            # else:
            set_task()
        except Exception as e:
            print(f"[SAFE_TASK ERROR] {e}")

    task_thread = threading.Thread(target=safe_task, daemon=False)
    task_thread.start()



    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        lambda: threading.Thread(target=safe_task, daemon=False).start(),
        'cron',
        day_of_week='mon-fri',
        hour='9-17/4',
        minute=0,
        misfire_grace_time=60
    )

    # @sched.scheduled_job('cron', hour='*/1', minuite='0', id='프로세스 id 넣을것')

def set_task():
    global if_login_success, chat_rooms
    try:
        print("크롤링을 시작합니다.")
        # crawling.crawl_lists_title()
        crawling.crawl_news()
        print("크롤링을 완료했습니다.\n카카오톡 공유를 시작합니다.")

        enter_url()

        for room in chat_rooms:
            driver.click_share_button()
            time.sleep(2)

            # 팝업창 전환 후 로그인
            driver.activate_popup()
            time.sleep(2)

            # 로그인 화면이 뜨는지 확인
            if check_login_needed():
                driver.execute_login(os.getenv("ID"), os.getenv("PW"))

                # 못 찾을 경우 2초마다 확인
                while True:
                    time.sleep(2)
                    if driver.check_login_done():
                        break

            # 로그인 후 버튼 비활성화
            driver.ready_chatroom()
            if driver.is_chatroom_exist(room):
                print("채팅방을 선택합니다 : " + room)
                driver.click_chatroom()
                driver.click_share()
                print("메세지 공유를 완료하였습니다.")
                driver.close_popup()
                print("팝업창을 종료합니다.")
                driver.deactivate_popup()
            else:
                raise Exception(f"{room} 채팅방을 찾을 수 없습니다.")
    except Exception as e:
        print(f"[set_task ERROR] {e}")

def enter_url():
    print("로컬 url에 접속합니다...")
    url = os.getenv("APP_BASE_URL", "http://localhost:9005") + "/run"
    driver.get_url(url)
    print("url에 접속 성공")
    time.sleep(5)


