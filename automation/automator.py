import os
import threading

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

def start_task():

    def safe_task():
        try:
            set_task()
        except Exception as e:
            print(f"[SAFE_TASK ERROR] {e}")

    task_thread = threading.Thread(target=safe_task, daemon=False)
    task_thread.start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: threading.Thread(target=safe_task, daemon=False).start(),
        'interval',
        minutes=60
    )

    scheduler.start()

    # @sched.scheduled_job('cron', hour='*/1', minuite='0', id='프로세스 id 넣을것')


def set_task():
    global if_login_success
    try:
        print("=====================================================================")
        print("리스트를 랜덤으로 셔플하여 지피티한테 전달합니다.\n이 버전은 10분 단위로 3시까지 실행됩니다.")
        print("=====================================================================")
        print("크롤링을 시작합니다.")
        crawling.crawl_lists_title()
        print("크롤링을 완료했습니다.\n카카오톡 공유를 시작합니다.")
        enter_url()

        # 로그인 화면이 뜨는지 확인
        if check_login_needed():
            driver.execute_login(os.getenv("ID"), os.getenv("PW"))

            # 못 찾을 경우 2초마다 확인
            while True:
                time.sleep(2)
                if driver.check_login_done():
                    break
            # 이렇게 해도 되나?
            # while driver.check_login_done() is False:
            #     time.sleep(2)

        # 로그인 후 버튼 비활성화
        driver.ready_chatroom()
        if driver.is_chatroom_exist(os.getenv("ROOM")):
            print("채팅방을 선택합니다 : " + os.getenv("ROOM"))
            driver.click_chatroom()
            driver.click_share()
            print("메세지 공유를 완료하였습니다.")
            driver.close_popup()
            print("팝업창을 종료합니다.")
            driver.deactivate_popup()
    except Exception as e:
        print(f"[set_task ERROR] {e}")

def enter_url():
    print("로컬 url에 접속합니다...")
    url = os.getenv("APP_BASE_URL", "http://localhost:9005") + "/run"
    driver.get_url(url)
    print("url에 접속 성공")
    time.sleep(5)

    driver.click_share_button()
    time.sleep(2)

    # 팝업창 전환 후 로그인
    driver.activate_popup()
