#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging
import random
import time
import os

from ddt import ddt, data
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from businessView.createView import CreateView
from businessView.generalView import GeneralView
from businessView.openView import OpenView
from businessView.pgView import PGView
from common.myunit import StartEnd
from common.common_data import *


@ddt
class TestPg(StartEnd):
    file_type = 'pg'

    # @unittest.skip('skip test_ppt_format')
    def test_ppt_format(self):
        logging.info('==========test_ppt_format==========')
        cv = CreateView(self.driver)
        cv.create_file('pg')
        pg = PGView(self.driver)
        pg.group_button_click(' Edit ')
        for i in FORMAT:
            pg.edit_format(i)
        time.sleep(3)

    # @unittest.skip('skip test_ppt_template')
    def test_ppt_template(self):
        logging.info('==========test_ppt_template==========')
        cv = CreateView(self.driver)
        cv.create_file('pg')
        pg = PGView(self.driver)
        pg.group_button_click(' Edit ')
        for i in range(11):
            pg.edit_template(i)
        time.sleep(3)

    # @unittest.skip('skip test_ppt_add_scroll_comment')
    def test_ppt_add_scroll_comment(self):  # ppt缩略图滚屏备注
        logging.info('==========test_ppt_add_scroll_comment==========')
        ov = OpenView(self.driver)
        ov.open_random_file('ppt')
        pg = PGView(self.driver)
        pg.switch_write_read()
        pg.add_new()
        pg.add_comment(5, 'test2')
        pg.add_new()
        pg.check_comment(5)
        pg.edit_comment('TEST')
        pg.add_new()
        pg.check_comment(5)
        pg.delete_comment()
        time.sleep(1)

    # @unittest.skip('skip test_ppt_play_to_first')
    @data(*['current', 'first'])
    def test_ppt_play_to_first(self, play_type):
        logging.info('==========test_ppt_play_to_first==========')
        cv = CreateView(self.driver)
        cv.create_file('pg')
        pg = PGView(self.driver)
        pg.add_new()
        pg.add_new()

        logging.info('==========play to the first page==========')
        pg = PGView(self.driver)
        pg.group_button_click(' Play ')
        pg.play_mode(play_type)
        if play_type == 'first':
            index = 1
        else:
            index = 3
        pg.play_to_first(index)

        logging.info('==========validate toast==========')
        try:
            toast = self.driver.find_element(By.XPATH, '//*[@text="It has been the first slide."]')
        except NoSuchElementException:
            self.assertTrue(False, '未出现弹窗')
        else:
            self.assertEqual(toast.text, 'It has been the first slide.', '验证弹窗信息为已是简报首页')

    # @unittest.skip('skip test_ppt_play_to_last')
    @data(*['current', 'first'])
    def test_ppt_play_to_last(self, play_type):
        logging.info('==========test_ppt_play_to_last==========')
        cv = CreateView(self.driver)
        cv.create_file('pg')
        pg = PGView(self.driver)
        pg.add_new()
        pg.add_new()

        logging.info('==========play to the last page==========')
        pg = PGView(self.driver)
        pg.group_button_click(' Play ')
        pg.play_mode(play_type)
        if play_type == 'first':
            index = 1
        else:
            index = 3
        pg.play_to_last(index, 3)

        logging.info('==========validate toast==========')
        try:
            toast = self.driver.find_element(By.XPATH, '//*[@text="It has been the last slide."]')
        except NoSuchElementException:
            self.assertTrue(False, '未出现弹窗')
        else:
            self.assertEqual(toast.text, 'It has been the last slide.', '验证弹窗信息为已是简报尾页')

    # @unittest.skip('skip test_ppt_play')
    def test_ppt_play(self):  # ppt Play 
        logging.info('==========test_ppt_play==========')
        ov = OpenView(self.driver)
        ov.open_file('欢迎使用永中Office.pptx')
        pg = PGView(self.driver)
        pg.group_button_click(' Play ')
        pg.play_mode('first')
        x, y = pg.get_size()

        time.sleep(1)
        pg.tap(y * 0.75, x * 0.5)
        time.sleep(1)
        pg.tap(y * 0.75, x * 0.5)
        pg.quit_play()
        pg.play_mode('current')
        time.sleep(1)
        pg.tap(y * 0.75, x * 0.5)
        time.sleep(1)
        pg.tap(y * 0.75, x * 0.5)
        pg.quit_play()
        pg.swipeRight()
        pg.swipeRight()
        pg.swipeRight()
        pg.play_mode('autoplay')
        time.sleep(2)
        pg.pause_resume_play()
        time.sleep(1)
        pg.pause_resume_play()
        time.sleep(20)

    # @unittest.skip('skip test_ppt_autoplay_to_last')
    def test_ppt_autoplay_to_last(self):
        logging.info('==========test_ppt_autoplay_to_last==========')
        cv = CreateView(self.driver)
        cv.create_file('pg')
        pg = PGView(self.driver)
        pg.add_new()
        pg.add_new()

        logging.info('==========autoplay to the last page==========')
        pg = PGView(self.driver)
        pg.group_button_click(' Play ')
        pg.play_mode('autoplay')

        logging.info('==========validate toast==========')
        try:
            WebDriverWait(self.driver, 120).until(
                ec.visibility_of_element_located((By.XPATH, '//*[@text="It has been the last slide."]')))
        except TimeoutException:
            self.assertTrue(False, '等待自动 Play 两分钟，未找到弹窗')
        else:
            toast = self.driver.find_element(By.XPATH, '//*[@text="It has been the last slide."]')
            self.assertEqual(toast.text, 'It has been the last slide.', '验证弹窗信息为已是简报尾页')

    # @unittest.skip('skip test_ppt_play_switch')
    @data(*SWITCH_LIST)
    def test_ppt_play_switch(self, switch):  # 幻灯片切换
        logging.info('==========test_ppt_play_switch==========')
        ov = OpenView(self.driver)
        ov.open_random_file('ppt')
        pg = PGView(self.driver)
        pg.switch_write_read()

        pg.group_button_click(' Switch ')
        pg.switch_mode(switch, 'all')
        pg.group_button_click(' Play ')
        pg.play_mode()
        logging.info('==========validate toast==========')
        try:
            WebDriverWait(self.driver, 1200).until(
                ec.visibility_of_element_located((By.XPATH, '//*[@text="It has been the last slide."]')))
        except TimeoutException:
            self.assertTrue(False, '等待自动 Play 二十分钟，未找到弹窗')
        else:
            toast = self.driver.find_element(By.XPATH, '//*[@text="It has been the last slide."]')
            self.assertEqual(toast.text, 'It has been the last slide.', '验证弹窗信息为已是简报尾页')

    # @unittest.skip('skip test_shape_text_attr_pg')
    def test_shape_text_attr_pg(self):  # 自选图形文本属性，仅WP和PG
        logging.info('==========test_shape_text_attr_pg==========')
        cv = CreateView(self.driver)
        cv.create_file(self.file_type)
        gv = GeneralView(self.driver)
        gv.group_button_click(' Insert ')
        gv.insert_shape(self.file_type, 1)
        gv.group_button_click(' Edit ')
        gv.font_name(self.file_type, 'AndroidClock')
        gv.font_size(15)
        gv.font_style(self.file_type, '倾斜')
        gv.font_color(self.file_type, 6, 29)
        gv.swipe_ele('//*[@text=" Font Color "]', '//*[@text=" Edit "]')
        gv.fold_expand()
        time.sleep(1)
        x, y = gv.find_pic_position('drag_all')
        gv.tap(x, y)  # 进入 Edit 
        gv.pop_menu_click('editText')
        for i in range(20):
            self.driver.press_keycode(random.randint(29, 54))
        time.sleep(1)
        gv.group_button_click(' Edit ')
        gv.bullets_numbers('pg', 6, 10)
        gv.text_align(self.file_type, '分散对齐')
        gv.text_align(self.file_type, '右对齐')
        gv.text_line_space(self.file_type, 1.5)
        gv.text_line_space(self.file_type, 3)
        gv.text_indent(self.file_type, '右缩进')
        gv.text_indent(self.file_type, '右缩进')
        gv.text_indent(self.file_type, '左缩进')
        time.sleep(3)

    # @unittest.skip('skip test_ppt_add_scroll_comment')
    def test_ppt_add_scroll_comment(self):  # ppt缩略图滚屏备注
        logging.info('==========test_ppt_add_scroll_comment==========')
        ov = OpenView(self.driver)
        ov.open_random_file('ppt')
        pg = PGView(self.driver)
        pg.switch_write_read()
        pg.add_new()
        pg.add_comment(5, 'test2')
        pg.add_new()
        pg.check_comment(5)
        pg.edit_comment('TEST')
        pg.add_new()
        pg.check_comment(5)
        pg.delete_comment()
        time.sleep(1)

    # @unittest.skip('skip test_ppt_slide')
    def test_ppt_slide(self):  # 幻灯片复制、剪切、粘贴
        logging.info('==========test_ppt_slide==========')
        cv = CreateView(self.driver)
        cv.create_file(self.file_type)
        gv = GeneralView(self.driver)

        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[1]').click()
        time.sleep(1)
        gv.pop_menu_click('copy')
        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[1]').click()
        time.sleep(1)
        gv.pop_menu_click('paste')

        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[2]').click()
        time.sleep(1)
        gv.pop_menu_click('cut')
        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[1]').click()
        time.sleep(1)
        gv.pop_menu_click('paste')

        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[2]').click()
        time.sleep(1)
        gv.pop_menu_click('create')
        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[3]').click()
        time.sleep(1)
        gv.pop_menu_click('delete')

        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[2]').click()
        time.sleep(1)
        x1, y1 = gv.find_pic_position('copy')
        x2, y2 = gv.find_pic_position('delete')
        gv.swipe(x2, y2, x1, y1)
        gv.pop_menu_click('hide')
        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[2]').click()
        time.sleep(1)
        gv.pop_menu_click('hide_cancel')
        self.driver.find_element(By.XPATH, '//android.widget.HorizontalScrollView'
                                           '/android.widget.LinearLayout/android.view.View[2]').click()
        time.sleep(1)
        gv.pop_menu_click('comment')

        time.sleep(3)

    # @unittest.skip('skip test_ppt_insert_new')
    def test_ppt_insert_new(self):
        logging.info('==========test_ppt_insert_new==========')
        cv =CreateView(self.driver)
        cv.create_file('pg')

        logging.info('==========insert new ppt==========')
        pv = PGView(self.driver)
        pv.insert_new_ppt()
        gv = GeneralView(self.driver)
        gv.fold_expand()

        logging.info('==========validate insert success==========')
        thumbnails_list = self.driver.find_elements(By.CLASS_NAME, 'android.view.View')
        thumbnails_list[0].click()
        pv.screenshot_edit_ppt(SEREEN_SHOTS + 'new_first.png')
        thumbnails_list[1].click()
        pv.screenshot_edit_ppt(SEREEN_SHOTS + 'new_second.png')

        result1 = gv.compare_pic('first.png', 'new_first.png')
        result2 = gv.compare_pic('new_second.png', 'new_ppt.png')

        self.assertEqual(result1, 0.0)
        self.assertEqual(result2, 0.0)

        logging.info('==========delete pngs==========')
        os.remove(SEREEN_SHOTS + 'first.png')
        os.remove(SEREEN_SHOTS + 'new_first.png')
        os.remove(SEREEN_SHOTS + 'new_second.png')