#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from selenium.webdriver.common.by import By
from businessView.generalView import GeneralView


class SSView(GeneralView):
    def cell_location(self):  # 获取单元格坐标及长宽
        logging.info('======cell_location=====')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_edit_container').click()
        cell = self.driver.find_element(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/yozo_ss_frame_table_container"]'
                                                  '/android.view.ViewGroup/android.view.ViewGroup[2]')
        bounds = cell.get_attribute('bounds')
        print(bounds)
        coordinate_str = bounds.replace('][', '],[').replace('[', '').replace(']', '').split(',')
        loc_list = list(map(lambda x: int(x), coordinate_str))
        print(loc_list)
        width = loc_list[2] - loc_list[0]
        height = loc_list[3] - loc_list[1]
        return loc_list[0], loc_list[1], width, height
    
    def object_position(self, A, B):  # 获取单元格的坐标
        logging.info('======cell_position=====')
        x1, y1 = self.find_pic_position(A)
        x2, y2 = self.find_pic_position(B)
        width = x2 - x1
        height = y2 - y1
        x = x2 - width / 2
        y = y2 - height / 2
        return x, y, width, height