#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging
import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from businessView.loginView import LoginView
from common.common_func import Common


class CreateView(Common):

    def create_file(self, type, subtype=1):
        """
        #新建文档
        :param type: wp/pg/ss
        :param subtype:
        :return:
        """
        logging.info('==========create_file_%s==========' % type)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/fb_show_menu_main').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/fb_show_menu_%s' % type).click()

        logging.info('choose Template %s' % subtype)
        self.driver.find_elements(By.ID, 'com.yozo.office.en:id/iv_gv_image')[subtype - 1].click()

    def save_as_file(self, file_name, save_path, item=1):  # 另存为
        logging.info('==========save_as_file==========')
        if not self.get_element_result('//*[@text="另存为"]'):
            self.group_button_click('文件')
        self.driver.find_element(By.XPATH, '//*[@text="另存为"]').click()
        if self.get_element_result('//*[@text="保存路径"]'):
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_folder').click()
        self.save_step(save_path, file_name, item)

    def save_file(self):  # 点击保存图标或者保存选项，随机
        logging.info('==========save_file==========')
        if random.randint(0, 1) == 0:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_save').click()
        else:
            if not self.get_element_result('//*[@text=" Save "]'):
                self.group_button_click(' File ')
            self.driver.find_element(By.XPATH, '//*[@text=" Save "]').click()

    def save_new_file(self, file_name, save_path, item=1):  # 文件名，本地还是云端save_path=['local','cloud']，文件类型item=[1,2]
        logging.info('==========save_exist_file==========')
        self.save_file()
        self.save_step(save_path, file_name, item)

    def save_step(self, save_path, file_name, item):
        logging.info('==========save_step==========')
        logging.info('choose save path %s' % save_path)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_%s' % save_path).click()

        logging.info('whether need login')
        if self.get_toast_message('您尚未登录，请登录'):
            l = LoginView(self.driver)
            l.login_action('13915575564', 'zhang199412')
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_%s' % save_path).click()

        logging.info('file named %s' % file_name)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_file_name').set_text(file_name)

        logging.info('choose file type %s' % item)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_file_type').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/file_type_item%s' % item).click()

        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_save_btn').click()  # save

    def check_save_file(self):
        logging.info('==========check_create_file==========')
        return self.get_toast_message('保存成功')

    def cover_file(self, is_cover):
        """
        是否覆盖文档
        :param is_cover: True or False
        :return: None
        """
        logging.info('==========cover_file==========')
        try:
            self.driver.find_element(By.ID, 'android:id/message')
        except NoSuchElementException:
            pass
        else:
            if is_cover:
                self.driver.find_element(By.ID, 'android:id/button1').click()
            else:
                self.driver.find_element(By.ID, 'android:id/button2').click()
