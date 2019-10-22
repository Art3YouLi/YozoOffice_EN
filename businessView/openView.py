#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from common.common_func import Common


class OpenView(Common):

    def close_file(self):
        logging.info('======close_file=====')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_close').click()  # 关闭功能

    def check_close_file(self):
        """
        验证文档是否被关闭
        :return: flag
        """
        logging.info('==========check_close_file==========')
        time.sleep(1)
        flag = False
        try:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_close')
        except NoSuchElementException:
            logging.info('==========the file closed==========')
            flag = True

        return flag

    def open_file(self, file_name):
        logging.info('======open_file_%s=====' % file_name)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search').click()  # 点击搜索功能
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/et_search').send_keys(file_name)  # 输入搜索内容
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_search_search').click()  # 点击搜索按钮
        self.driver.find_element(By.XPATH, '//android.widget.TextView[@text="%s"]' % file_name).click()  # 打开对应文件

    def check_open_status(self, file_name):
        logging.info('======test_open_status_%s=====' % file_name)
        try:
            # 查找指定元素判断是否加载成功
            self.find_element(By.XPATH, "//*[@resource-id='com.yozo.office.en:id/yozo_ui_option_group_button']")
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_close').click()
            self.find_element(By.ID, 'com.yozo.office.en:id/iv_search_search').click()
        except NoSuchElementException:
            logging.error(file_name + 'open fail!')
            self.getScreenShot(file_name + 'open fail')
            return False
        else:
            logging.info(file_name + 'open success!')
            return True

    def open_random_file(self, keywords):
        """
        打开关键字搜索结果的文档，并返回文件名
        :param keywords: 关键字
        :return: 打开的文件名称
        """
        logging.info('======open_random_file=====')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search').click()  # 点击搜索功能
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/et_search').send_keys(keywords)  # 输入关键字
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_search_search').click()  # 点击搜索按钮
        time.sleep(1)
        results_list = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')
        num = random.randint(0, len(results_list)-2)
        result = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')[num]
        filename = result.text
        result.click()
        return filename

    def open_several_files(self):
        """
        打开一系列文件
        :return: None
        """
        logging.info('======open_several_files=====')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search').click()  # 点击搜索功能
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_search_search').click()  # 点击搜索按钮
        results_list = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')
        for result in results_list:
            result.click()
            self.close_file()
            time.sleep(2)
        Common(self.driver).swipeUp()
        results_list = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')
        results_list[-1].click()
        self.close_file()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_search_back').click()


