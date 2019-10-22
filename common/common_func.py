#!/user/bin/env python3
# -*- coding: utf-8 -*-

import math
import operator
import cv2 as cv
import time, os
import csv
import logging

from functools import reduce
from PIL import Image
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from common.tool import get_project_path
from baseView.baseView import BaseView


class Common(BaseView):

    def find_image_cv(self, obj_path, src_path):
        source = cv.imread(src_path)
        template = cv.imread(obj_path)
        print('source')
        print(source.shape)
        print('template')
        print(template.shape)
        result = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
        print('result')
        print(result)
        print(len(result))
        pos_start = cv.minMaxLoc(result)[3]
        test = cv.minMaxLoc(result)
        print('pos_start')
        print(pos_start)
        print('test')
        print(test)
        x = int(pos_start[0]) + int(template.shape[1] / 2)
        y = int(pos_start[1]) + int(template.shape[0] / 2)
        # similarity = cv.minMaxLoc(result)[1]
        # if similarity < 0.85:
        #     return (-1, -1)
        # else:
        print("pass")
        print(str(x) + ',' + str(y))
        return x, y

    def swipe_search2(self, target, range):
        if not self.get_element_result(target):
            eles = self.driver.find_elements(By.XPATH, range)
            self.swipe_ele1(eles[-1], eles[0])
            self.swipe_search2(target, range)

    def swipe_ele2(self, eleA, eleB):
        y_ele1 = eleA.location['y']
        x_ele1 = eleA.location['x']
        x_ele2 = eleB.location['x']
        self.driver.swipe(x_ele1, y_ele1, x_ele2, y_ele1, 3000)

    def swipe_ele1(self, eleA, eleB):
        y_ele1 = eleA.location['y']
        x_ele1 = eleA.location['x']
        y_ele2 = eleB.location['y']
        self.driver.swipe(x_ele1, y_ele1, x_ele1, y_ele2, 3000)

    def swipe_ele(self, eleA, eleB):
        ele1 = self.get_element(eleA)
        ele2 = self.get_element(eleB)
        y_ele1 = ele1.location['y']
        x_ele1 = ele1.location['x']
        y_ele2 = ele2.location['y']
        self.driver.swipe(x_ele1, y_ele1, x_ele1, y_ele2, 3000)

    def drag_element(self, ele1, ele2):  # 拖动
        logging.info('drag')
        action = TouchAction(self.driver)

        action.long_press(el=ele1).move_to(el=ele2).release()
        action.perform()

    def drag_coordinate(self, x1, y1, x2, y2):  # 拖动
        logging.info('drag')
        action = TouchAction(self.driver)

        action.long_press(x=x1, y=y1).move_to(x=x2, y=y2).release()
        action.perform()

    def long_press(self, x, y):  # 长按
        logging.info('long_press')
        action = TouchAction(self.driver)

        action.long_press(x=x, y=y).wait(1000).release()
        action.perform()

    def tap(self, x, y, count=1):  # 点击
        time.sleep(1)
        logging.info('Tap')
        action = TouchAction(self.driver)

        action.tap(x=x, y=y, count=count)
        action.perform()

    def zoom(self):  # 缩小
        logging.info('Zoom')
        action1 = TouchAction(self.driver)  # 第一个手势
        action2 = TouchAction(self.driver)  # 第二个手势
        zoom_action = MultiAction(self.driver)  # 放大手势

        x, y = self.get_size()
        action1.press(x=x * 0.4, y=y * 0.4).move_to(x=x * 0.2, y=y * 0.2).release()
        action2.press(x=x * 0.6, y=y * 0.6).move_to(x=x * 0.8, y=y * 0.8).release()

        zoom_action.add(action1, action2)  # 加载
        time.sleep(2)
        zoom_action.perform()  # 执行

    def pinch(self):  # 缩小
        logging.info('==========Pinch==========')
        action1 = TouchAction(self.driver)  # 第一个手势
        action2 = TouchAction(self.driver)  # 第二个手势
        pinch_action = MultiAction(self.driver)  # 放大手势

        x, y = self.get_size()
        action1.press(x=x * 0.8, y=y * 0.3).move_to(x=x * 0.5, y=y * 0.5).release()
        action2.press(x=x * 0.3, y=y * 0.8).move_to(x=x * 0.5, y=y * 0.5).release()

        pinch_action.add(action1, action2)  # 加载
        time.sleep(2)
        pinch_action.perform()  # 执行

    def group_button_click(self, option):
        logging.info('==========group_button_click_%s==========' % option)
        if self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_group_button').text == option:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_expand_button').click()
        else:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_group_button').click()
            self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="%s"]' % option).click()

    def get_elements_attribute(self, elements, attr):
        logging.info('==========get_elements_attribute==========')
        try:
            # attr1 = (By.XPATH, '//*[@resource-id="%s"]' % elements)
            eles = self.driver.find_elements(By.XPATH, elements)
        except NoSuchElementException:
            logging.error("%s locate fail" % str(elements))
            self.getScreenShot("%s locate fail" % str(elements))
            raise
        else:
            logging.info("%s locate success" % str(elements))
            eles_attr = map(lambda x: x.get_attribute(attr), eles)
            return eles_attr

    def get_element(self, ele):
        logging.info('get_element')
        return self.driver.find_element(By.XPATH, ele)

    def get_element_result(self, ele):
        logging.info('==========get_element_result==========')
        try:
            self.driver.find_element(By.XPATH, ele)
        except NoSuchElementException:
            logging.error('get element: %s fail!' % ele)
            return False
        else:
            logging.info('get element: %s success!' % ele)
            return True

    def get_toast_message(self, toast_message):
        logging.info('==========get_toast_message==========')
        message = '//*[@text="' + toast_message + '"]'
        try:
            # WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(By.XPATH, message))
            self.driver.find_element(By.XPATH, message)
        except NoSuchElementException:
            logging.error('get toast message: %s fail!' % toast_message)
            return False
        else:
            logging.info('get toast message: %s success!' % toast_message)
            return True

    def get_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipeLeft(self):
        logging.info('swipeLeft')
        l = self.get_size()
        x1 = int(l[0] * 0.9)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.1)
        self.swipe(x1, y1, x2, y1, 1000)

    def swipeRight(self):
        logging.info('swipeRight')
        l = self.get_size()
        x1 = int(l[0] * 0.9)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.1)
        self.swipe(x2, y1, x1, y1, 1000)

    def swipeUp(self):
        logging.info('swipeUp')
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.8)
        y2 = int(l[1] * 0.2)
        self.swipe(x1, y1, x1, y2, 1000)

    def swipeDown(self):
        logging.info('swipeDown')
        l = self.get_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.8)
        y2 = int(l[1] * 0.2)
        self.swipe(x1, y2, x1, y1, 1000)

    def getTime(self, timestr):
        # self.now = time.strftime("%Y-%m-%d %H_%M_%S")
        self.now = time.strftime(timestr)
        return self.now

    def getScreenShot4Compare(self, file_name):
        image_file = os.path.dirname(os.path.dirname(__file__)) + '/screenshots/%s.png' % file_name

        logging.info('get %s screenshot' % file_name)
        self.driver.get_screenshot_as_file(image_file)

    def compare_pic(self, pic1, pic2):  # 图片对比
        logging.info('compare %s with %s' % (pic1, pic2))
        pic_path = get_project_path() + '/screenshots/'
        image1 = Image.open(pic_path + pic1)
        image2 = Image.open(pic_path + pic2)
        h1 = image1.histogram()
        h2 = image2.histogram()
        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        print(result)
        return result

    def getScreenShot(self, module):
        time = self.getTime("%Y-%m-%d %H_%M_%S")
        image_file = os.path.dirname(os.path.dirname(__file__)) + '/screenshots/%s_%s.png' % (module, time)

        logging.info('get %s screenshot' % module)
        self.driver.get_screenshot_as_file(image_file)

    def get_csv_data(self, csv_file, line):
        logging.info('=====get_csv_data======')
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader, 1):
                if index == line:
                    return row

    def exist(self, element):
        try:
            self.find_element(By.XPATH, element)
        except NoSuchElementException:
            logging.info('=====%s element not exist!======' % element)
            return False
        else:
            logging.info('=====%s element exist!======' % element)
            return True

    @staticmethod
    def clear_special_str(a):
        c = ['.', '_', '-']
        for i in c:
            a = a.replace(i, '')
        return a
