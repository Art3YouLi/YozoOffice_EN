#!/user/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
import time
import unittest
import os

from ddt import ddt, data
from selenium.webdriver.common.by import By
from common.myunit import StartEnd
from businessView.generalView import GeneralView
from businessView.openView import OpenView
from businessView.createView import CreateView
from businessView.wpView import PGView
from airtest.core.api import *
from airtest.core.settings import Settings as ST

@ddt
class TestSs:
    @unittest.skip('skip test_ss_data_table')
    def test_ss_data_table(self):  # 数据排序，工作表格式
        logging.info('==========test_ss_data_table==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        for i in range(10):
            time.sleep(1)
            cv.tap(110 + 263 * 1.5, 295 + 55 * (1.5 + i))  # 双击进入编辑
            cv.tap(110 + 263 * 1.5, 295 + 55 * (1.5 + i))
            self.driver.press_keycode(random.randint(7, 16))
        ss = SSView(self.driver)
        ss.group_button_click('查看')
        time.sleep(1)
        ss.data_sort('降序')
        ss.data_sort('升序')
        ss.sheet_style('隐藏编辑栏')
        ss.sheet_style('隐藏编辑栏')
        ss.sheet_style('隐藏表头')
        ss.sheet_style('隐藏表头')
        ss.sheet_style('隐藏网格线')
        # ss.sheet_style('冻结窗口') 功能未完成
        # ss.sheet_style('取消冻结')
        ss.sheet_style('100%')
        time.sleep(3)

    @unittest.skip('skip test_ss_font_attr')
    def test_ss_font_attr(self):
        logging.info('==========test_ss_font_attr==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)  # 双击进入编辑
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        for i in range(5):
            self.driver.press_keycode(45)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        gv = GeneralView(self.driver)
        gv.group_button_click('编辑')
        type = 'ss'
        gv.font_name(type)
        gv.font_size(23)
        gv.font_style(type, '加粗')
        gv.font_style(type, '倾斜')
        gv.font_style(type, '删除线')
        gv.font_style(type, '下划线')
        gv.font_color(type)

    @unittest.skip('skip test_ss_cell_attr')
    def test_ss_cell_attr(self):
        logging.info('==========test_ss_cell_attr==========')
        cv = CreateView(self.driver)
        ss = SSView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        x, y, width, height = ss.cell_location()
        self.driver.press_keycode(45)
        self.driver.press_keycode(45)
        self.driver.press_keycode(45)
        self.driver.press_keycode(45)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        ss.group_button_click('编辑')
        time.sleep(1)

        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ss.swipe_ele(ele2, ele1)
        ss.cell_align('水平居中', '下对齐')

    @unittest.skip('skip test_ss_cell_border')
    def test_ss_cell_border(self):  # 遍历边框所有功能
        logging.info('==========test_ss_cell_border==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')

        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        time.sleep(1)
        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ss.swipe_ele(ele2, ele1)
        ss.cell_border()

    @unittest.skip('skip test_ss_num_style')
    def test_ss_num_style(self):
        logging.info('==========test_ss_num_style==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)  # 双击进入编辑
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.press_keycode(15)
        self.driver.press_keycode(7)
        self.driver.press_keycode(7)
        self.driver.press_keycode(7)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="单元格填充"]'
        ss.swipe_ele(ele2, ele1)
        ss.swipe_ele(ele3, ele1)
        ss.cell_num_style()

    @unittest.skip('skip test_ss_merge_wrap')
    def test_ss_merge_wrap(self):
        logging.info('==========test_ss_merge_wrap==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)  # 双击进入编辑
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        for i in range(20):
            self.driver.press_keycode(45)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        cv.drag_coordinate(110 + 263 * 2, 295 + 55 * 2, 110 + 263 * 3, 295 + 55 * 2)

        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="单元格填充"]'
        ele4 = '//*[@text="数字格式"]'
        ss.swipe_ele(ele2, ele1)
        ss.swipe_ele(ele3, ele1)
        ss.swipe_ele(ele4, ele1)
        ss.cell_merge_split()
        ss.cell_merge_split()
        ss.cell_auto_wrap()
        ss.cell_auto_wrap()
        time.sleep(3)

    @unittest.skip('skip test_ss_cell_inser_delete_fit')
    def test_ss_cell_insert_delete_fit(self):  # 插入删除行宽列高清除
        logging.info('==========test_ss_cell_inser_delete_fit==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)  # 双击进入编辑
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        for i in range(20):
            self.driver.press_keycode(45)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        gv = GeneralView(self.driver)
        gv.font_style(type, '删除线')

        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="单元格填充"]'
        ele4 = '//*[@text="数字格式"]'
        ele5 = '//*[@text="插入单元格"]'
        ele6 = '//*[@text="删除单元格"]'
        ele7 = '//*[@text="设置行高列宽"]'
        ss.swipe_ele(ele2, ele1)
        ss.swipe_ele(ele3, ele1)
        ss.swipe_ele(ele4, ele1)
        ss.cell_insert('右移')
        ss.cell_insert('下移')
        ss.cell_insert('插入整行')
        ss.cell_insert('插入整列')
        ss.cell_delete('删除整列')
        ss.cell_delete('删除整行')
        ss.cell_delete('上移')
        ss.cell_delete('左移')
        ss.swipe_ele(ele5, ele1)
        ss.cell_set_size(5, 5)
        ss.group_button_click('编辑')
        ss.cell_clear('清除格式')
        gv.undo_option()
        ss.cell_clear('清除内容')
        gv.undo_option()
        ss.cell_clear('清除所有')
        gv.undo_option()
        ss.swipe_ele(ele6, ele7)
        ss.cell_fit_height()
        ss.cell_fit_width()
        time.sleep(3)

    @unittest.skip('skip test_ss_table_style')
    def test_ss_table_style(self):  # 表格样式
        logging.info('==========test_ss_table_style==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        cv.drag_coordinate(110 + 263 * 2, 295 + 55 * 2, 110 + 263 * 3, 295 + 55 * 4)
        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="单元格填充"]'
        ele4 = '//*[@text="数字格式"]'
        ele5 = '//*[@text="插入单元格"]'
        ss.swipe_ele(ele2, ele1)
        ss.swipe_ele(ele3, ele1)
        ss.swipe_ele(ele4, ele1)
        ss.swipe_ele(ele5, ele1)
        ss.table_style()

    @unittest.skip('skip test_formula1')
    def test_formula1(self):  # 其他类型公式
        logging.info('==========test_formula1==========')
        cv = CreateView(self.driver)
        ss = SSView(self.driver)
        cv.create_file('ss')
        time.sleep(1)

        x, y, width, height = ss.cell_location()  # cell B8
        for i in range(10):
            ss.tap(x + width * 0.5, y - height * (6.5 - i))
            ss.cell_edit()
            self.driver.press_keycode(random.randint(7, 16))

        cv.tap(110 + 263 * 2.5, 295 + 55 * 0.5)
        ss.formula_all('最近使用', 'MAX')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 1.5)
        ss.formula_all('数学和三角', 'ABS')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 2.5)
        ss.formula_all('财务', 'DOLLARDE')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        time.sleep(0.5)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 5.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 3.5)
        ss.formula_all('逻辑', 'AND')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        time.sleep(0.5)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 5.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 4.5)
        ss.formula_all('文本', 'ASC')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 5.5)
        ss.formula_all('日期和时间', 'NOW')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 6.5)
        ss.formula_all('查找与引用', 'COLUMN')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 7.5)
        ss.formula_all('统计', 'AVERAGE')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        # cv.tap(110 + 263 * 2.5, 295 + 55 * 8.5)
        # ss.formula_all('工程', 'DEC2BIN')
        # cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        # self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 9.5)
        ss.formula_all('信息', 'ISBLANK')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        cv.tap(110 + 263 * 2.5, 295 + 55 * 10.5)
        ss.formula_all('所有公式', 'ABS')
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

    @unittest.skip('skip test_formula')
    @data(*auto_sum)
    def test_formula(self, formula):
        logging.info('==========test_formula==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)

        ss = SSView(self.driver)
        x, y, width, height = ss.cell_location()  # cell B8
        for i in range(5):
            ss.tap(x + width * 0.5, y - height * (6.5 - i))
            ss.cell_edit()
            self.driver.press_keycode(random.randint(7, 16))

        ss.tap(x + width * 1.5, y - height * 6.5)  # 求和
        ss.auto_sum(formula)
        ss.tap(x + width * 0.5, y - height * 6.5)
        ss.drag_coordinate(x + width, y - height * 6, x + width, y - height * 2)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

    @unittest.skip('skip test_pop_cell_row_col1')
    def test_pop_cell_row_col1(self):  # 单元格、行、列相关操作
        logging.info('==========test_pop_cell_row_col1==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file(type)
        gv = GeneralView(self.driver)
        ss = SSView(self.driver)
        time.sleep(1)

        x, y, width, height = ss.cell_location()  # 新建默认B8
        cv.tap(x + width * 0.5, y - height * 5.5)
        ss.cell_edit()  # 进入编辑
        for i in range(8):
            self.driver.press_keycode(random.randint(29, 54))
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        time.sleep(0.5)
        cv.tap(x + width * 0.5, y - height * 5.5)  # 复制粘贴
        gv.pop_menu_click('copy')
        cv.tap(x + width * 0.5, y - height * 4.5)
        cv.tap(x + width * 0.5, y - height * 4.5)
        gv.pop_menu_click('paste')
        cv.tap(x + width * 1.5, y - height * 4.5)
        cv.tap(x + width * 1.5, y - height * 4.5)
        gv.pop_menu_click('paste')

        cv.tap(x + width * 1.5, y - height * 4.5)
        gv.pop_menu_click('cut')
        cv.tap(x + width * 0.5, y - height * 3.5)
        cv.tap(x + width * 0.5, y - height * 3.5)
        gv.pop_menu_click('paste')

        x, y = gv.find_pic_position('drag_point2')  # 多选单元格
        gv.drag_coordinate(x, y, x + width, y + height)

    @unittest.skip('skip test_pop_cell_row_col2')
    def test_pop_cell_row_col2(self):  # 单元格、行、列相关操作
        logging.info('==========test_pop_cell_row_col2==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file(type)
        gv = GeneralView(self.driver)
        ss = SSView(self.driver)
        time.sleep(1)

        x, y, width, height = ss.cell_location()  # 新建默认B8
        cv.tap(x + width * 0.5, y - height * 5.5)  # 点击B2
        ss.cell_edit()  # 进入编辑
        for i in range(8):
            self.driver.press_keycode(random.randint(29, 54))
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        time.sleep(0.5)

        x1, y1, x2, y2 = ss.row_col_loc()
        ss.tap(x2 - 10, y2 + height * 1.5)
        gv.pop_menu_click('insert')
        ss.tap(x2 - 10, y2 + height * 1.5)
        gv.pop_menu_click('delete')
        ss.tap(x2 - 10, y2 + height * 1.5)
        gv.pop_menu_click('copy')
        ss.tap(x2 - 10, y2 + height * 4.5)
        x3, y3 = gv.find_pic_position('copy')
        x4, y4 = gv.find_pic_position('insert')
        gv.swipe(x3, y3, x4, y4)
        gv.pop_menu_click('paste')
        ss.tap(x2 - 10, y2 + height * 1.5)
        gv.pop_menu_click('cut')
        ss.tap(x2 - 10, y2 + height * 0.5)
        gv.pop_menu_click('paste')
        ss.tap(x2 - 10, y2 + height * 1.5)
        gv.pop_menu_click('hide')
        ss.tap(x2 - 10, y2 + height * 1.5)
        x3, y3 = gv.find_pic_position('hide')
        x4, y4 = gv.find_pic_position('copy')
        gv.swipe(x3, y3, x4, y4)
        gv.pop_menu_click('hide_cancel')
        ss.tap(x2 - 10, y2 + height * 4.5)
        x, y = gv.find_pic_position('row_down')
        gv.drag_coordinate(x, y, x, y + height * 2)
        gv.drag_coordinate(x2 - 10, y, x2 - 10, y + height * 2)

    @unittest.skip('skip test_pop_cell_row_col3')
    def test_pop_cell_row_col3(self):  # 单元格、行、列相关操作
        logging.info('==========test_pop_cell_row_col3==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file(type)
        gv = GeneralView(self.driver)
        ss = SSView(self.driver)
        time.sleep(1)

        x, y, width, height = ss.cell_location()  # 新建默认B8
        cv.tap(x + width * 0.5, y - height * 5.5)
        ss.cell_edit()  # 进入编辑
        for i in range(8):
            self.driver.press_keycode(random.randint(29, 54))
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        time.sleep(0.5)

        x1, y1, x2, y2 = ss.row_col_loc()
        ss.tap(x2 + width * 1.5, y2 - 10)
        gv.pop_menu_click('insert')
        ss.tap(x2 + width * 1.5, y2 - 10)
        gv.pop_menu_click('delete')
        ss.tap(x2 + width * 1.5, y2 - 10)
        gv.pop_menu_click('copy')
        ss.tap(x2 + width * 2.5, y2 - 10)
        x3, y3 = gv.find_pic_position('copy')
        x4, y4 = gv.find_pic_position('insert')
        gv.swipe(x3, y3, x4, y4)
        time.sleep(1)
        gv.pop_menu_click('paste')
        ss.tap(x2 + width * 1.5, y2 - 10)
        gv.pop_menu_click('cut')
        ss.tap(x2 + width * 2.5, y2 - 10)
        gv.pop_menu_click('paste')
        ss.tap(x2 + width * 1.5, y2 - 10)
        gv.pop_menu_click('hide')
        ss.tap(x2 + width * 1.5, y2 - 10)
        x3, y3 = gv.find_pic_position('hide')
        x4, y4 = gv.find_pic_position('copy')
        gv.swipe(x3, y3, x4, y4)
        time.sleep(1)
        gv.pop_menu_click('hide_cancel')
        ss.tap(x2 + width * 1.5, y2 - 10)
        x, y = gv.find_pic_position('column_right')
        gv.drag_coordinate(x, y, x + width, y)
        gv.drag_coordinate(x, y2 - 10, x + width, y2 - 10)

    @unittest.skip('skip test_pop_menu_text_ss')
    def test_pop_menu_cell_text(self):
        logging.info('==========test_pop_menu_cell_text==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file(type)
        gv = GeneralView(self.driver)
        ss = SSView(self.driver)
        time.sleep(1)

        x, y, width, height = ss.cell_location()  # 新建默认B8
        cv.tap(x + width * 0.5, y - height * 5.5)  # 点击B2
        ss.cell_edit()  # 进入编辑
        for i in range(15):
            self.driver.press_keycode(random.randint(29, 54))
        # time.sleep(1)
        gv.drag_coordinate(x + 200, y - height * 5.5, x + 50, y - height * 5.5)
        gv.pop_menu_click('copy')
        gv.tap(x + width * 0.5, y - height * 5.5)
        gv.pop_menu_click('paste')
        gv.drag_coordinate(x + 200, y - height * 5.5, x + 50, y - height * 5.5)
        gv.pop_menu_click('cut')
        gv.tap(x + width * 0.5, y - height * 5.5)
        gv.pop_menu_click('paste')

        gv.tap(x + width * 0.5, y - height * 5.5)
        gv.pop_menu_click('newline')

        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        gv.tap(x + width * 0.5, y - height * 5.5)
        gv.pop_menu_click('fill_data')
        x1, y1 = gv.find_pic_position('fill_down')
        gv.drag_coordinate(x1, y1, x1, y1 + height * 2)

        gv.tap(x + width * 0.5, y - height * 5.5)
        time.sleep(1)
        x2, y2 = gv.find_pic_position('fill_data')
        gv.swipe(x2, y2, x2 - width * 2, y2)
        gv.pop_menu_click('clear_content')

    @unittest.skip('skip test_cell_inser_delete_fit')
    def test_cell_insert_delete_fit(self):  # 插入删除行宽列高清除
        logging.info('==========test_cell_inser_delete_fit==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)  # 双击进入编辑
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        for i in range(20):
            self.driver.press_keycode(45)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        gv = GeneralView(self.driver)
        gv.font_style(type, '删除线')

        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="单元格填充"]'
        ele4 = '//*[@text="数字格式"]'
        ele5 = '//*[@text="插入单元格"]'
        ele6 = '//*[@text="删除单元格"]'
        ele7 = '//*[@text="设置行高列宽"]'
        ss.swipe_ele(ele2, ele1)
        ss.swipe_ele(ele3, ele1)
        ss.swipe_ele(ele4, ele1)
        ss.cell_insert('右移')
        ss.cell_insert('下移')
        ss.cell_insert('插入整行')
        ss.cell_insert('插入整列')
        ss.cell_delete('删除整列')
        ss.cell_delete('删除整行')
        ss.cell_delete('上移')
        ss.cell_delete('左移')
        ss.swipe_ele(ele5, ele1)
        ss.cell_set_size(5, 5)
        ss.group_button_click('编辑')
        ss.cell_clear('清除格式')
        gv.undo_option()
        ss.cell_clear('清除内容')
        gv.undo_option()
        ss.cell_clear('清除所有')
        gv.undo_option()
        ss.swipe_ele(ele6, ele7)
        ss.cell_fit_height()
        ss.cell_fit_width()
        time.sleep(3)

    @unittest.skip('skip test_sheet_operation')
    def test_sheet_operation(self):  # sheet相关功能
        logging.info('==========test_sheet_operation==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        ss = SSView(self.driver)
        ss.show_sheet()
        ss.hide_sheet()
        ss.show_sheet()
        ss.add_sheet()
        ss.rename_sheet(0, 'test')
        self.assertTrue(ss.check_rename_sheet(0, 'test'))

    @unittest.skip('skip test_sheet_operation1')
    def test_sheet_operation1(self):  # sheet相关功能
        logging.info('==========test_sheet_operation1==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        ss = SSView(self.driver)
        ss.show_sheet()
        ss.operate_sheet(0, 'insert')
        ss.operate_sheet(0, 'copy')
        ss.operate_sheet(0, 'remove')
        ss.operate_sheet(0, 'hide')
        ss.unhide_sheet(0, 0)

    @unittest.skip('skip test_drag_sheet')
    def test_drag_sheet(self):  # sheet拖动
        logging.info('==========test_drag_sheet==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        ss = SSView(self.driver)
        ss.show_sheet()
        ss.add_sheet()
        ss.add_sheet()
        ele1 = ss.get_element('//*[@resource-id="com.yozo.office.en:id/ll_ss_sheet_item"and @index="0"]')
        ele2 = ss.get_element('//*[@resource-id="com.yozo.office.en:id/ll_ss_sheet_item"and @index="2"]')
        # ele1 = ss.find_element(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/ll_ss_sheet_item"and @index="0"]')
        # ele2 = ss.find_element(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/ll_ss_sheet_item"and @index="2"]')
        ss.drag_element(ele1, ele2)

    @unittest.skip('skip test_ss_chart_pop')
    def test_ss_chart_pop(self):  # 图表相关操作
        logging.info('==========test_ss_chart_pop==========')
        cv = CreateView(self.driver)
        type = 'ss'
        cv.create_file(type)
        ss = SSView(self.driver)
        gv = GeneralView(self.driver)
        time.sleep(2)
        x, y, width, height = ss.object_position('drag_point1', 'drag_point2')
        ss.tap(x, y)
        time.sleep(2)
        ss.pop_menu_click('edit')
        self.driver.press_keycode(12)
        ss.tap(x, y + height)
        time.sleep(1)

        ss.tap(x, y + height)
        time.sleep(2)
        ss.pop_menu_click('edit')
        self.driver.press_keycode(15)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
        # ss.tap(x, y)
        x, y = ss.find_pic_position('drag_point1')
        ss.swipe(x, y, x, y - height)
        time.sleep(1)
        ss.group_button_click('插入')
        gv.insert_chart_insert('柱形图', 2)

        x, y, width, height = ss.object_position('chart_all1', 'chart_all4')
        ss.tap(x, y)
        time.sleep(2)
        ss.pop_menu_click('cut')
        ss.tap(x, y)
        time.sleep(2)
        ss.tap(x, y)
        ss.pop_menu_click('paste')
        ss.tap(x, y)
        time.sleep(2)
        ss.pop_menu_click('copy')
        ss.tap(x, y)
        time.sleep(2)
        ss.pop_menu_click('paste')
        ss.swipe(x, y, x - 100, y + 100)
        x, y = ss.find_pic_position('chart_all1')
        ss.swipe(x, y, x - 100, y - 100)

    @unittest.skip('skip test_table_style')
    def test_table_style(self):  # 表格样式
        logging.info('==========test_table_style==========')
        cv = CreateView(self.driver)
        cv.create_file('ss')
        time.sleep(1)
        cv.tap(110 + 263 * 1.5, 295 + 55 * 1.5)
        cv.drag_coordinate(110 + 263 * 2, 295 + 55 * 2, 110 + 263 * 3, 295 + 55 * 4)
        ss = SSView(self.driver)
        ss.group_button_click('编辑')
        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="单元格填充"]'
        ele4 = '//*[@text="数字格式"]'
        ele5 = '//*[@text="插入单元格"]'
        ss.swipe_ele(ele2, ele1)
        ss.swipe_ele(ele3, ele1)
        ss.swipe_ele(ele4, ele1)
        ss.swipe_ele(ele5, ele1)
        ss.table_style()