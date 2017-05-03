# -*- coding:utf-8 -*-
import time
import uuid
from io import BytesIO
from PIL import Image
import random
from selenium.webdriver.common.action_chains import ActionChains


class VerifyCodeHandle(object):

    """"验证码破解基础类"""

    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()

    def input_by_id(self, text='百度', element_id='keyword'):
        """输入关键字
        :text: 要输入的文本
        :element_id: 输入框网页元素id
        """
        print("start input_by_id.... : ", text)
        input_el = self.driver.find_element_by_id(element_id)
        input_el.clear()
        input_el.send_keys(text)
        time.sleep(3.5)

    def click_by_id(self, element_id="btn_query"):
        """点击查询按钮
        :element_id: 查询按钮网页元素id
        """
        print("start click_by_id....")
        search_el = self.driver.find_element_by_id(element_id)
        search_el.click()
        time.sleep(3.5)

    def calculate_slider_offset(self):
        """计算滑块偏移位置，必须在点击查询按钮之后调用
        :returns: number
        """
        print("start calculate_slider_offset...")
        img1 = self.crop_captcha_image()
        self.drag_and_drop(x_offset=30)
        img2 = self.crop_captcha_image()
        w1, h1 = img1.size
        w2, h2 = img2.size
        if w1 != w2 or h1 != h2:
            return False
        left = 0
        flag = False
        for j in range(0, h1, 10):
            for i in range(55, w1):
                # 寻找不一样的
                if not self.is_pixel_equal(img1, img2, i, j):
                    # 寻找不一样的
                    if not self.is_pixel_equal(img1, img2, i+30, j):
                        left = i
                        flag = True
                    break
            if flag:
                break
        # if left == 55:
        #     left -= 5
        #     # left += 2
        left -= 6
        print("left:", left)
        return left

    def is_pixel_equal(self, img1, img2, x, y):
        # print("start is_pixel_equal....")
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        if (abs(pix1[0] - pix2[0] < 60) and abs(pix1[1] - pix2[1] < 60) and abs(pix1[2] - pix2[2] < 60)):
            return True
        else:
            return False

    def crop_captcha_image(self, element_id="gt_box"):
        """截取验证码图片
        :element_id: 验证码图片网页元素id
        :returns: StringIO, 图片内容
        """
        # print("start crop_captcha_image:", element_id)
        captcha_el = self.driver.find_element_by_class_name(element_id)
        location = captcha_el.location
        size = captcha_el.size
        # print("size:", size)
        left = int(location['x'])
        top = int(location['y'])
        # left = 1010
        # top = 535
        right = left + int(size['width'])
        bottom = top + int(size['height'])
        # right = left + 523
        # bottom = top + 235
        print(left, top, right, bottom)
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        captcha = screenshot.crop((left, top, right, bottom))
        id = uuid.uuid1()
        # print("id:", id)
        captcha.save("{}.png".format(id))
        return captcha

    def get_browser_name(self):
        """获取当前使用浏览器名册"""
        return str(self.driver).split('.')[2]

    def drag_and_drop(self, x_offset=0, y_offset=0, element_class='gt_slider_knob'):
        """拖拽滑块
        :x_offset: 相对滑块x坐标偏移
        :y_offset: 相对滑块y坐标偏移
        :element_class: 滑块网页元素css类名
        """
        print("拖拽滑块....")
        dragger = self.driver.find_element_by_class_name(element_class)
        # 第一种方法 drag_and_drop_by_offset
        # action = ActionChains(self.driver)
        # Actions(self.driver).drag_and_drop_by_offset(dragger, x_offset, y_offset).wait(5).perform()
        # 第二种方法 click_and_hold  move_by_offset
        # actions = ActionChains(self.driver)
        # actions.click_and_hold(dragger).move_by_offset(x_offset, y_offset).release().perform()
        # 第三种方法 click_and_hold  move_by_offset
        # action = ActionChains(self.driver)
        # action.click_and_hold(dragger)
        # action.move_by_offset(0, 10).move_by_offset(10, 0)
        # action.move_by_offset(x_offset-10, y_offset-10).release()
        # action.perform()
        # 第四种方法 编写一个外部类 使用
        # Actions(self.driver)\
        #     .click_and_hold(dragger)\
        #     .wait(random.uniform(0.005, 0.01)) \
        #     .move_by_offset(0, 10)\
        #     .move_by_offset(10, 0)\
        #     .wait(random.uniform(0.005, 0.01))\
        #     .move_by_offset(x_offset-10, y_offset-10)\
        #     .release()\
        #     .perform()
        # 第五种方法
        action = Actions(self.driver)
        action.click_and_hold(dragger)
        # step 设置步调的长度
        step = random.randint(2, 4)
        print("step:", step)
        for i in range(0, x_offset, step):
            action.move_by_offset(step, step)
            action.wait(random.uniform(0.0005, 0.01))
        action.release()
        action.perform()
        # 这个延时必须有， 在滑动后等待回复原状
        time.sleep(8)

    def move_to_element(self, element_class="gt_slider_knob"):
        """鼠标移动到网页元素上
        :element: 目标网页元素
        """
        print("鼠标移动到网页元素上...")
        time.sleep(3)
        element = self.driver.find_element_by_class_name(element_class)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()
        time.sleep(4.5)

    def crack(self):
        """执行破解程序
        """
        raise NotImplementedError


class Actions(ActionChains):
    def wait(self, time_s:float):
        self._actions.append(lambda: time.sleep(time_s))
        return self
