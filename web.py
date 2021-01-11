from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
import time
import os
import logging

logging.basicConfig(filename=f'test.log', filemode='a',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
desired_cap = {
    "deviceName": "Android Emulator",
    "platformName": "Android",
    "app": os.path.abspath(
        '/Users/rodrigosanmiguel/Desktop/SpiderOak/testing-automation-mobile/tools/CrossClave.apk')
}

# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_cap)
# driver.implicitly_wait(60)


def ensure_click(element):
    MAX_ATTEMPTS = 20

    for i in range(0, MAX_ATTEMPTS):
        try:
            element.click()

        except ElementClickInterceptedException:
            time.sleep(5)
            logging.warning(f"Retrying click!! Click number {i + 1} did not work!")
        else:
            break


class Web:
    """
    This class abstracts the visible screen and allows searching for components in it.
    """

    # seconds until timeout; if after this time the elements are not visible, a TimeoutException
    # will be raised
    TIMEOUT = 45

    def __init__(self, web_driver):
        # """ Init the class using the web driver (i.e., chromedriver) """
        super().__init__()

        self._web_driver_wait = WebDriverWait(web_driver, Web.TIMEOUT)
        self._web_driver = web_driver

        # self._mobile_driver_wait = (mobile_driver, Web.TIMEOUT)

        # self.web_driver = web_driver
        # self._web_driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_cap)
        # self.web_driver.implicitly_wait(60)
        # self.mobile_driver = driver.Remote("http://127.0.0.1:4723/wd/hub", desired_cap)

    def open(self, url):
        # self._web_driver.get(url)
        self._web_driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_cap)

    def find_by_xpath(self, xpath):
        # find a single visible element using its XPATH
        return self._web_driver_wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def finds_by_xpath(self, xpath):
        # return a list of present elements using XPATH
        return self._web_driver_wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    def find_by_text(self, target_text, only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"{prefix}//*[text()='{target_text}']")

    def find_by_android_text(self, target_text, only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"//android.view.View[@text=('{target_text}')]")

    def find_by_android_text_input(self,  only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"//android.widget.EditText")

    def hide_keyword(self):
        return self._web_driver.hide_keyboard()

    def find_text_input(self, placeholder, only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"{prefix}//input[@placeholder='{placeholder}']")

    def find_all_text_inputs(self, placeholder):
        return self.finds_by_xpath(f"//input[@placeholder='{placeholder}']")

    def find_text_area(self):
        return self._web_driver.find_element_by_tag_name('textarea')

    def find_button_by_text(self, target_text):
        return self.find_by_xpath(f"//span[contains(@class, 'Button__label') and text()='{target_text}']")

    def find_button_by_android_text(self, target_text):
        return self.find_by_xpath(f"//*[@text=('{target_text}')]")

    def find_real_button_by_text(self, target_text):
        xpath = f"//button[.//text()='{target_text}']"
        return self._web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def find_team_by_text(self, team_name):
        return self.find_by_xpath(f"//div[contains(@class, 'TeamSwitcher__listItemText')]/span[text()='{team_name}']")

    def find_by_partial_class(self, class_partial_name, only_current_childs=False):
        # since Classes are generated automatically and we can never know a class exact name,
        # this method searches for a part of the class name
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"{prefix}//*[contains(@class, '{class_partial_name}')]")

    def finds_by_partial_class(self, class_partial_name):
        # returns a list of elements with that partial class
        return self.finds_by_xpath(f"//*[contains(@class, '{class_partial_name}')]")

    def finds_by_class(self, class_name):
        # returns a list of elements with that partial class
        return self.finds_by_xpath(f"//*[contains(@class, '{class_name}')]")

    def finds_by_QA_id(self, item_id):
        return self.finds_by_xpath(f"//*[@data-qa-testid='{item_id}']")

    def find_by_id(self, item_id):
        # return self._web_driver_wait.until(EC.presence_of_element_located((By.XPATH, f"//*[@id='{item_id}']")))
        return self._web_driver.find_element_by_xpath(f"//*[@id='{item_id}']")

    def find_by_QA_id(self, item_id, only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"{prefix}//*[@data-qa-testid='{item_id}']")

    def find_by_QA_icon_type(self, icon_type, only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return self.find_by_xpath(f"{prefix}//*[@data-qa-icon-type='{icon_type}']")

    def text_not_present(self, target_text):
        return len(self._web_driver.find_elements_by_xpath(f"//*[text()='{target_text}']")) == 0

    def QA_id_not_present(self, item_id):
        return len(self._web_driver.find_elements_by_xpath(f"//*[@data-qa-testid='{item_id}']")) == 0

    def partial_class_not_present(self, class_partial_name, only_current_childs=False):
        prefix = "." if only_current_childs else ""
        return len(
            self._web_driver.find_elements_by_xpath(f"{prefix}//*[contains(@class, '{class_partial_name}')]")) == 0

    def double_click_on_element(self, element):
        act = ActionChains(self._web_driver)
        act.double_click(element).perform()

    def visible_spinner(self):
        """ Returns true if at least one spinner is visible in the screen """
        return len(self._web_driver.find_elements_by_xpath("//div[contains(@class, 'Spinner__')]")) > 0

    def visible_android_spinner(self):
        """ Returns true if at least one spinner is visible in the screen """
        return len(self._web_driver.find_elements_by_xpath("//*[@class ='android.widget.Image[1]']")) > 0


    def wait_page_loaded(self):
        return len(self._web_driver.find_elements_by_xpath(
            "//hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")) > 0

    def visible_loading(self):
        return len(self._web_driver.find_elements_by_xpath("//div[contains(@text, 'Loading...')]")) > 0

    def find_team_in_settings(self, team_name):
        return self.find_by_xpath(f"//div[contains(@class, 'MenuLayout__item') and text()='{team_name}']")

    def find_space(self, space_name):
        return self.find_by_xpath(f"//div[contains(@class, 'SpaceListItem__spaceName') and text()='{space_name}']")

    def wait_for_spinner(self):
        """ This method blocks until a Spinner is no longer visible in the screen.
        When it cannot find a spinner in the screen, it will unblock."""
        # TODO/FIXME: use the invisibility_of_element_located EC to better implement this?
        SPINNER_POLL_INTERVAL = 3
        while self.visible_android_spinner():
            time.sleep(SPINNER_POLL_INTERVAL)

    def wait_loading(self):
        LOAD_POLL_INTERVAL = 3
        while self.visible_loading():
            time.sleep(LOAD_POLL_INTERVAL)

    def reload(self):
        return self._web_driver.switch_to_default_content()
