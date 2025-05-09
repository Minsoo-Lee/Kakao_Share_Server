import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

driver = None
URL = "https://localhost:"
PORT = "9005"
main_window = None
inp_check = None

def init_chrome():
    global driver, main_window
    if driver is None:
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

        time.sleep(1)

    main_window = driver.current_window_handle


def get_url(url):
    global driver
    # print("url = " + url)
    driver.get(url)
    time.sleep(1)


def click_share_button():
    # 이 부분은 UI 건들면 바뀔 수 있음
    try:
        driver.find_element(By.XPATH, "/html/body/button").click()
        time.sleep(1)
    except Exception as e:
        print(e)


def activate_popup():
    global main_window

    # 팝업창 뜰 시간 필요
    time.sleep(1)
    all_windows = driver.window_handles

    for handle in all_windows:
        if handle != main_window:
            driver.switch_to.window(handle)
            break
    time.sleep(1)

def check_login_needed():
    try:
        driver.find_element(By.XPATH, "/html/body/div/div/div/main/article/div/div/form/div[1]/div/input")
        print("Login needed")
        return True
    except:
        print("Please Login")
        return False

def execute_login(id, pw):
    driver.find_element(By.XPATH, "/html/body/div/div/div/main/article/div/div/form/div[1]/div/input").send_keys(id)
    driver.find_element(By.XPATH, "/html/body/div/div/div/main/article/div/div/form/div[2]/div/input").send_keys(pw)
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div/div/div/main/article/div/div/form/div[4]/button[1]").click()
    time.sleep(1)

def close_popup():
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/button").click()
    time.sleep(1)

def deactivate_popup():
    driver.switch_to.window(main_window)
    time.sleep(1)


def check_login_done():
    try:
        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/div")
        return True
    except:
        print("로그인 인증이 아직 완료되지 않았습니다.")
        time.sleep(2)
        return False

def ready_chatroom():
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/ul/li[2]/a").click()
    time.sleep(1)

def is_chatroom_exist(room_name):
    global inp_check

    unit_chats = driver.find_elements(By.CLASS_NAME, "unit_chat")

    for chat in unit_chats:
        try:
            label = chat.find_element(By.CLASS_NAME, "tit_name")

            if label.text.strip() == room_name:
                # 해당 chat 내의 체크박스 요소 저장
                inp_check_candidate = chat.find_element(By.CLASS_NAME, "inp_check")
                inp_check = inp_check_candidate
                print("room_name = " + room_name + " / " + label.text.strip())
                return True

        except Exception as e:
            continue

    return False

def click_chatroom():
    global inp_check
    inp_check.click()
    time.sleep(1)

def click_share():
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/button/div/span").click()
    time.sleep(1)

def get_pagesource():
    return driver.page_source

def get_body():
    element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/div/div[1]/div/div[2]/article/div[1]")
    return element.text