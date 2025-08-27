from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException
)
import time
import random
import json
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from selenium.webdriver.remote.webelement import WebElement


# 配置选项
@dataclass
class Config:
    URL: str = "https://guess.gsqclub.cn"
    LOW: float = 0.00
    HIGH: float = 150.00
    PRECISION: float = 0.01
    MAX_ATTEMPTS: int = 100
    ELEMENT_TIMEOUT: int = 10  # 元素等待超时时间(秒)
    ELEMENT_CONFIG_FILE: str = "element_config.json"  # 元素配置文件


@dataclass
class ElementConfig:
    name: str
    xpath: str
    fallback_xpaths: List[str] = None
    dynamic: bool = False
    dynamic_attr: str = None
    dynamic_value: str = None

    def get_xpaths(self) -> List[str]:
        """获取所有可能的XPath表达式"""
        return [self.xpath] + (self.fallback_xpaths or [])


class ElementLocator:
    """动态元素定位器"""

    def __init__(self, driver, config_file: str):
        self.driver = driver
        self.config_file = config_file
        self.element_configs = self._load_element_configs()

    def _load_element_configs(self) -> Dict[str, ElementConfig]:
        """从配置文件加载元素配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    return {
                        name: ElementConfig(**data)
                        for name, data in config_data.items()
                    }
            except Exception as e:
                print(f"加载元素配置失败: {e}")
        return {}

    def save_element_configs(self):
        """保存元素配置到文件"""
        config_data = {
            name: config.__dict__
            for name, config in self.element_configs.items()
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    def add_element_config(self, name: str, config: ElementConfig):
        """添加元素配置"""
        self.element_configs[name] = config
        self.save_element_configs()

    def locate_element(self, name: str, timeout: int = None) -> Optional[WebElement]:
        """定位元素，支持动态识别"""
        if name not in self.element_configs:
            print(f"元素配置不存在: {name}")
            return None

        config = self.element_configs[name]
        timeout = timeout or Config.ELEMENT_TIMEOUT

        # 尝试所有预定义的XPath
        for xpath in config.get_xpaths():
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                print(f"成功定位元素 '{name}' 使用XPath: {xpath}")
                return element
            except TimeoutException:
                print(f"元素定位超时 '{name}': {xpath}")
                continue

        # 如果是动态元素，尝试动态识别
        if config.dynamic and config.dynamic_attr and config.dynamic_value:
            print(f"尝试动态识别元素 '{name}'...")
            try:
                dynamic_xpath = f"//*[contains(@{config.dynamic_attr}, '{config.dynamic_value}')]"
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, dynamic_xpath))
                )
                print(f"成功动态定位元素 '{name}' 使用XPath: {dynamic_xpath}")

                # 更新配置并保存
                if dynamic_xpath not in config.get_xpaths():
                    config.fallback_xpaths = config.fallback_xpaths or []
                    config.fallback_xpaths.append(dynamic_xpath)
                    self.save_element_configs()
                    print(f"已更新元素 '{name}' 的配置")

                return element
            except Exception as e:
                print(f"动态定位元素失败 '{name}': {e}")

        return None

    def locate_and_wait_clickable(self, name: str, timeout: int = None) -> Optional[WebElement]:
        """定位元素并等待可点击 - 修复了XPath获取逻辑"""
        element = self.locate_element(name, timeout)
        if element:
            timeout = timeout or Config.ELEMENT_TIMEOUT
            try:
                # 获取元素的标签名和属性来构建唯一标识符
                tag_name = element.tag_name
                element_id = element.get_attribute("id")
                if element_id:
                    locator = (By.ID, element_id)
                else:
                    # 使用CSS选择器作为替代方案
                    class_name = element.get_attribute("class")
                    if class_name:
                        locator = (By.CSS_SELECTOR, f"{tag_name}.{class_name.replace(' ', '.')}")
                    else:
                        # 最后尝试使用XPath
                        locator = (By.XPATH, f"//{tag_name}[@href='{element.get_attribute('href')}']"
                        if element.get_attribute('href') else (By.XPATH, element.get_attribute('xpath')))

                return WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
            except Exception as e:
                print(f"元素不可点击: {e}")
        return element


def setup_driver():
    # 配置Chrome选项
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 初始化浏览器
    driver = webdriver.Chrome(options=options)
    # 设置一些driver属性模拟真实用户
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver


def bypass_verification_manually(driver):
    print("请在打开的浏览器中完成以下操作:")
    print("1. 处理可能出现的验证码")
    print("2. 完成登录流程")
    print("3. 导航到猜分数页面")
    input("准备就绪后按Enter键继续...")


def get_random_delay(base=0.5, variance=0.3):
    """生成随机延迟时间，模拟人类操作节奏"""
    return base + random.uniform(0, variance)


def retry_on_stale_element(max_retries=3):
    """重试装饰器，处理StaleElementReferenceException"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except StaleElementReferenceException as e:
                    if attempt == max_retries - 1:
                        print(f"多次尝试后仍失败: {e}")
                        raise
                    print(f"元素过时，重试 ({attempt + 1}/{max_retries})")
                    time.sleep(1)  # 短暂等待页面稳定

        return wrapper

    return decorator


@retry_on_stale_element(max_retries=5)
def get_element_text(element):
    """获取元素文本内容，带有重试机制"""
    return element.text.strip()


@retry_on_stale_element(max_retries=5)
def clear_and_type(input_box, text):
    """清空输入框并输入文本，确保文本是字符串类型"""
    # 确保输入的是字符串
    text_str = str(text) if text is not None else ""

    input_box.clear()
    time.sleep(get_random_delay(0.3, 0.2))

    # 分步骤输入，模拟人类打字
    for char in text_str:
        input_box.send_keys(char)
        time.sleep(get_random_delay(0.1, 0.1))


@retry_on_stale_element(max_retries=5)
def click_element(element):
    """点击元素，支持多种点击方式"""
    try:
        # 先尝试常规点击
        element.click()
    except ElementClickInterceptedException:
        print("常规点击失败，尝试JavaScript点击")
        # 使用JavaScript点击作为备选方案
        driver = element.parent
        driver.execute_script("arguments[0].click();", element)
    time.sleep(get_random_delay(0.2, 0.1))


def initialize_element_configs(locator: ElementLocator):
    """初始化元素配置"""
    # 如果配置文件不存在，添加默认配置
    if not os.path.exists(Config.ELEMENT_CONFIG_FILE):
        # 定义元素配置
        element_configs = {
            "input_box": ElementConfig(
                name="input_box",
                xpath='/html/body/div[4]/div/div/div[2]/uni-view[1]/uni-view[1]/uni-view/uni-view/uni-view[2]/uni-input/div/input',
                dynamic=True,
                dynamic_attr="class",
                dynamic_value="input"
            ),
            "try_button": ElementConfig(
                name="try_button",
                xpath='(//uni-view[contains(@style, "background-color: rgb(212, 35, 122)") and .//uni-view[text()=" Try "]])[1]',
                dynamic=True,
                dynamic_attr="style",
                dynamic_value="background-color"
            ),
            "message_element": ElementConfig(
                name="message_element",
                xpath='/html/body/div[4]/div/div/div[2]/uni-view[2]/uni-view/uni-view/uni-view/uni-text/span',
                dynamic=True,
                dynamic_attr="class",
                dynamic_value="message"
            )
        }

        # 添加到定位器
        for name, config in element_configs.items():
            locator.add_element_config(name, config)


def main():
    driver = setup_driver()
    locator = ElementLocator(driver, Config.ELEMENT_CONFIG_FILE)

    try:
        # 初始化元素配置
        initialize_element_configs(locator)

        driver.get(Config.URL)
        bypass_verification_manually(driver)

        # 二分法猜数
        low = Config.LOW
        high = Config.HIGH
        attempts = 0

        while high - low > Config.PRECISION and attempts < Config.MAX_ATTEMPTS:
            mid = round((low + high) / 2, 2)
            print(f"\n尝试 {attempts + 1}: 猜测值 = {mid}")

            # 每次循环都重新定位所有元素
            input_box = locator.locate_and_wait_clickable("input_box")
            if not input_box:
                print("无法定位输入框，尝试重新获取...")
                input_box = locator.locate_element("input_box")
                if not input_box:
                    print("无法获取输入框，退出循环")
                    break

            try_button = locator.locate_and_wait_clickable("try_button")
            if not try_button:
                print("无法定位尝试按钮，尝试重新获取...")
                try_button = locator.locate_element("try_button")
                if not try_button:
                    print("无法获取尝试按钮，退出循环")
                    break

            # 模拟人类输入行为
            clear_and_type(input_box, mid)

            # 模拟人类点击行为
            time.sleep(get_random_delay(0.5, 0.3))
            click_element(try_button)

            # 等待页面响应和更新
            time.sleep(get_random_delay(1.5, 0.5))

            # 重新定位消息元素，因为页面可能已刷新
            message_element = locator.locate_element("message_element")
            if not message_element:
                print("无法定位消息元素，尝试重新获取...")
                message_element = locator.locate_element("message_element")
                if not message_element:
                    print("无法获取消息元素，退出循环")
                    break

            message = get_element_text(message_element)
            attempts += 1

            print(f"提示: {message}")

            if "too big" in message.lower():
                high = mid
            elif "too small" in message.lower():
                low = mid
            else:
                print(f"猜对了！分数是：{mid}")
                break

        if attempts >= Config.MAX_ATTEMPTS:
            print(f"达到最大尝试次数 ({Config.MAX_ATTEMPTS})")
            print(f"最终范围: {low} - {high}")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        input("按Enter键关闭浏览器...")
        driver.quit()


if __name__ == "__main__":
    main()