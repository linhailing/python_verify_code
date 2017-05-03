# -*- coding:utf-8 -*-
import time

from verifyCode import VerifyCodeHandle
from selenium import webdriver


class RunHandle(VerifyCodeHandle):
    """工商滑动验证码破解类"""
    def __init__(self, driver):
        super(RunHandle, self).__init__(driver)

    def crack(self):
        """"执行破解程序"""
        self.input_by_id()
        self.click_by_id()
        if self.driver.page_source:
            time.sleep(2)
            x_offset = self.calculate_slider_offset()
            print("x_offset:", x_offset)
            # x_offset += 60
            self.drag_and_drop(x_offset=x_offset)


def main():
    driver = webdriver.Chrome()
    driver.get('http://www.gsxt.gov.cn/index.html')
    cracker = RunHandle(driver)
    cracker.crack()
    print(driver.get_window_size)
    time.sleep(3)
    driver.save_screenshot('screen.png')
    driver.close()


if __name__ == "__main__":
    main()
