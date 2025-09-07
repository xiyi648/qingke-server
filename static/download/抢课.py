from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
from datetime import datetime

# 可配置参数（按超星页面实际位置修改）
TARGET_HOUR = 14
TARGET_MINUTE = 0
TARGET_SECOND = 0

# 元素XPATH（必核对）
FIRST_ELEMENT_XPATH = "//*[@id='first27437']/div"          # 选课入口
SECOND_ELEMENT_XPATH = "/html/body/div/div/div/div[2]/div[1]/ul/li[2]"  # 选课列表
SCHOOL_ELECTIVE_BTN1_XPATH = "//*[@id='app']/section/section/main/div/div[2]/div[1]/div/div/div/div/div/div/div/table/tbody/tr[4]/td[11]"  # 校本1（20440）
SCHOOL_ELECTIVE_BTN2_XPATH = "//*[@id='app']/section/section/main/div/div[2]/div[1]/div/div/div/div/div/div/div/table/tbody/tr[14]/td[11]"  # 校本2（20451）
SPORTS_PAGE_XPATH = "//*[@id='app']/section/aside/div/ul/li[3]/ul/li[2]"  # 体育选课入口
WUSHU_BTN_XPATH = "//*[@id='app']/section/section/main/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[11]"  # 武术
VOLLEYBALL_BTN_XPATH = "//*[@id='app']/section/section/main/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[11]"  # 排球
BASKETBALL_BTN_XPATH = "//*[@id='app']/section/section/main/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr[3]/td[11]"  # 篮球

# 抢课参数
CLICK_INTERVAL = (0.2, 0.6)
RETRY_WAIT = 0.3
WAIT_TIMEOUT = 6


def init_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(
        executable_path='/data/data/com.termux/files/usr/bin/chromedriver',
        options=options
    )
    driver.set_page_load_timeout(8)
    driver.set_script_timeout(4)
    return driver


def get_sport_choice():
    print("===== 选择体育选修课 =====")
    while True:
        sport_input = input("输入序号（1=武术 / 2=排球 / 3=篮球）：")
        if sport_input == "1":
            print(f"已选：武术\n")
            return WUSHU_BTN_XPATH, "武术"
        elif sport_input == "2":
            print(f"已选：排球\n")
            return VOLLEYBALL_BTN_XPATH, "排球"
        elif sport_input == "3":
            print(f"已选：篮球\n")
            return BASKETBALL_BTN_XPATH, "篮球"
        else:
            print("输入无效！仅输1/2/3\n")


def wait_for_early_login(driver):
    print("===== 提前登录 =====")
    driver.get("https://i.chaoxing.com")
    input("登录成功后按【回车】→ 到点抢课（过点直接开始）！\n")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, FIRST_ELEMENT_XPATH))
        )
        print("✅ 登录成功，进入选课准备页\n")
    except:
        print("⚠️ 未找到选课入口，到点重试\n")


def wait_until_target_time():
    print("===== 等待抢课开始 =====")
    while True:
        now = datetime.now()
        if now.hour > TARGET_HOUR or (now.hour == TARGET_HOUR and now.minute >= TARGET_MINUTE and now.second >= TARGET_SECOND):
            print(f"⏰ 当前时间：{now.strftime('%H:%M:%S')}，开始抢课！\n")
            break
        if now.second == 0:
            target_time = datetime(now.year, now.month, now.day, TARGET_HOUR, TARGET_MINUTE, TARGET_SECOND)
            delta = target_time - now
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            seconds = delta.seconds % 60
            print(f"距离14点还有：{hours}小时{minutes}分钟{seconds}秒", end='\r')
        time.sleep(1)


def high_freq_click(driver, xpath, desc):
    print(f"→ 抢：{desc}")
    retry_count = 4
    while retry_count > 0:
        try:
            element = WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print(f"✅ 抢到：{desc}")
            time.sleep(random.uniform(*CLICK_INTERVAL))
            return True
        except:
            retry_count -= 1
            print(f"⚠️ 未抢到{desc}，剩{retry_count}次机会")
            time.sleep(RETRY_WAIT)
            driver.refresh()
            time.sleep(0.5)
    print(f"❌ {desc}抢失败")
    return False


if __name__ == "__main__":
    print("===== 超星抢课脚本启动 =====\n")
    
    selected_sport_xpath, selected_sport_name = get_sport_choice()
    driver = init_browser()
    try:
        wait_for_early_login(driver)
        wait_until_target_time()
        
        high_freq_click(driver, FIRST_ELEMENT_XPATH, "选课入口")
        high_freq_click(driver, SECOND_ELEMENT_XPATH, "选课列表")
        high_freq_click(driver, SCHOOL_ELECTIVE_BTN1_XPATH, "校本课1（20440）")
        high_freq_click(driver, SCHOOL_ELECTIVE_BTN2_XPATH, "校本课2（20451）")
        high_freq_click(driver, SPORTS_PAGE_XPATH, "体育选课入口")
        high_freq_click(driver, selected_sport_xpath, f"体育课（{selected_sport_name}）")
        
        print("\n===== 抢课结束！去超星检查结果 =====\n")
        
    except KeyboardInterrupt:
        print("\n❌ 脚本手动停止")
    finally:
        time.sleep(2)
        driver.quit()
        print("浏览器已关闭")