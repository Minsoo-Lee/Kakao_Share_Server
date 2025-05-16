from automation.automator import start_task
from web.server import run_flask
import time
import threading

if __name__ == '__main__':
    print("리스트를 랜덤으로 셔플하여 지피티한테 전달합니다.\n이 버전은 10분 단위로 3시까지 실행됩니다.")
    print("프로그램을 실행합니다")
    print("작업을 수행합니다")
    # run_flask()
    start_task()
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # 프로그램 종료 시 서버도 종료되도록 설정
    flask_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("종료합니다.")


