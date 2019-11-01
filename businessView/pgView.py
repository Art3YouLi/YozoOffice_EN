#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from businessView.generalView import GeneralView


class PGView(GeneralView):
    def edit_format(self, format):  # 版式
        # format = ['标题与副标题', '标题', '标题与文本', '标题与两栏文本', '标题与竖排文本-上下', '标题与竖排文本-左右',
        #           '空白','标题与图片','标题、文本与图片','标题、图片与文本','标题、图片与竖排文本','标题、竖排文本与图片']
        logging.info('==========edit_format==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_option_id_edit_format').click()
        range = '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout'
        format_ele = '//*[@text="%s"]' % format
        self.swipe_search2(format_ele, range)
        self.driver.find_element(By.XPATH, format_ele).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()


