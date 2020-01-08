#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging
import random
import time
import unittest

from ddt import ddt, data
from selenium.webdriver.common.by import By

from common.myunit import StartEnd
from businessView.generalView import GeneralView
from businessView.openView import OpenView
from businessView.createView import CreateView
from businessView.pgView import PGView
from businessView.ssView import SSView
from common.common_data import *


@ddt
class TestCommon(StartEnd):
    @unittest.skip('skip test_undo_redo')
    @data(*WPS)
    def test_undo_redo(self, file_type):  # 撤销、重做
        logging.info('==========test_undo_redo==========')
        cv = CreateView(self.driver)
        gv = GeneralView(self.driver)
        cv.create_file(file_type)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_undo')  # 判断页面是否已切过来

        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type, 1)
        gv.fold_expand()

        gv.undo_option()
        time.sleep(1)
        gv.redo_option()
        time.sleep(1)
        gv.undo_option()
        time.sleep(1)

        logging.info('capture before undo')
        gv.getScreenShot4Compare('before_undo')

        gv.redo_option()
        time.sleep(1)

        logging.info('capture before redo')
        gv.getScreenShot4Compare('before_redo')

        gv.undo_option()
        if file_type == 'ss':
            gv.fold_expand()
            gv.fold_expand()
        time.sleep(1)
        logging.info('capture after undo')
        gv.getScreenShot4Compare('after_undo')

        gv.redo_option()
        time.sleep(1)
        logging.info('capture after redo')
        gv.getScreenShot4Compare('after_redo')

        result1 = gv.compare_pic('before_undo.png', 'after_undo.png')
        result2 = gv.compare_pic('before_redo.png', 'after_redo.png')

        self.assertLess(result1, 100, 'undo fail!')
        self.assertLess(result2, 100, 'redo fail!')

    @unittest.skip('skip test_create_file')
    @data(*WPS)
    def test_create_file(self, file_type):  # 新建文档
        logging.info('==========test_create_file==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/fb_show_menu_main').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/fb_show_menu_%s' % file_type).click()
        create_dict = {'wp': 'New blank.doc', 'ss': 'New blank.xls', 'pg': 'New blank.ppt'}
        self.driver.find_elements(By.ID, 'com.yozo.office.en:id/iv_gv_image')[0].click()
        file_name = self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_title_text_view').text
        self.assertTrue(file_name == create_dict[file_type])
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_close').click()

    @unittest.skip('skip test_rotate')
    @data(*WPS)
    def test_rotate(self, file_type):
        logging.info('==========test_rotate==========')
        suffix = SEARCH_DICT[file_type]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)
        gv = GeneralView(self.driver)
        # gv.screen_rotate('landscape')
        self.assertTrue(gv.check_rotate())
        gv.screen_rotate('portrait')

    @unittest.skip('skip test_search_replace')
    @data(*WPS)
    def test_search_replace(self, file_type):  # 查找替换
        logging.info('==========test_search_replace==========')
        cv = CreateView(self.driver)
        gv = GeneralView(self.driver)
        cv.create_file(file_type)
        if file_type == 'ss':
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_edit_container').click()
        elif file_type == 'pg':
            pg = PGView(self.driver)
            x, y = pg.get_size()
            pg.tap(x * 0.5, y * 0.4)
            pg.tap(x * 0.5, y * 0.4)
        elif file_type == 'wp':
            gv.tap(700, 700)
        self.driver.press_keycode(53)
        self.driver.press_keycode(43)
        self.driver.press_keycode(54)
        self.driver.press_keycode(43)
        if file_type in WS:
            if file_type == 'ss':
                self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()
            gv.group_button_click(' View ')
        gv.search_content(file_type, 'yozo')
        gv.replace_content('YOZO')
        time.sleep(3)
        gv.replace_content('yozo', 'all')

    @unittest.skip('skip test_read_mode')
    @data(*WPS)
    def test_read_mode(self, file_type):  # 阅读模式
        logging.info('==========test_read_mode==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        gv.switch_write_read()
        self.assertTrue(gv.check_write_read())

    @unittest.skip('skip test_close_file')
    @data(*WPS)
    def test_close_file(self, file_type):
        """
        关闭功能（X）
        :param file_type: 文档类型：'wp', 'ss', 'pg'
        :return: None
        """
        logging.info('==========test_close_file==========')
        ov = OpenView(self.driver)
        ov.open_random_file(SEARCH_DICT[file_type])
        ov.close_file()
        self.assertTrue(ov.check_close_file())

    @unittest.skip('skip test_save_existFile')
    @data(*WPS)
    def test_zz_save_existFile(self, file_type):  # 已有文件改动保存
        logging.info('==========test_save_existFile==========')
        suffix = SEARCH_DICT[file_type]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)
        cv = CreateView(self.driver)
        gv = GeneralView(self.driver)
        gv.switch_write_read()
        gv.group_button_click(' Signature ')
        gv.pen_type(file_type, '荧光笔')
        self.driver.swipe(300, 400, 800, 500)
        cv.save_file()
        self.assertTrue(cv.check_save_file())

    @unittest.skip('skip test_save_newFile')
    @data(*WPS)
    def test_zz_save_newFile(self, file_type):  # 新建脚本保存
        logging.info('==========test_save_newFile==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        file_name = 'save_new' + cv.getTime('%Y%m%d%H%M%S')
        cv.save_new_file(file_name, 'local', item=2)
        self.assertTrue(cv.check_save_file())

    @unittest.skip('skip test_export_pdf')
    @data(*WP)
    def test_export_pdf(self, file_type):  # 导出pdf
        logging.info('==========test_export_pdf==========')
        suffix = SEARCH_DICT[file_type]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)

        gv = GeneralView(self.driver)
        file_name = 'export_pdf ' + gv.getTime('%Y-%m-%d %H_%M_%S')
        gv.export_pdf(file_name, 'local')

        self.assertTrue(gv.check_export_pdf())

    #@unittest.skip('skip test_share_newFile')
    @data(*SHARE_LIST)
    def test_share_newFile(self, share_info):
        """
        新建文档分享
        :param share_info: 分享相关信息，'wp_wx', 'wp_qq', 'wp_ding', 'wp_mail'..
        :return: None
        """
        logging.info('==========test_share_newFile==========')
        file_type = share_info.split('_')[0]
        share_type = share_info.split('_')[1]

        logging.info('==========create and save new File==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        cv.save_new_file('%s%s分享' % (file_type, share_type), 'local')
        time.sleep(1)
        cv.cover_file(True)
        self.assertTrue(cv.get_toast_message('Saved to local'))

        logging.info('==========share new File==========')
        gv = GeneralView(self.driver)
        gv.share_file(file_type, share_type)

    #@unittest.skip('skip test_share_file')
    @data(*SHARE_LIST)
    def test_share_file(self, way):  # 分享文件
        logging.info('==========test_share_file==========')
        index = way.index('_')
        suffix = SEARCH_DICT[way[0:index]]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)

        gv = GeneralView(self.driver)
        gv.share_file(way[0:index], way[index + 1:])

    #@unittest.skip('skip test_share_editFile')
    @data(*SHARE_LIST)
    def test_share_editFile(self, share_info):
        """
        编辑文档分享
        :param share_info: 分享相关信息，'wp_wx', 'wp_qq', 'wp_ding', 'wp_mail'..
        :return: None
        """
        logging.info('==========test_share_newFile==========')
        file_type = share_info.split('_')[0]
        share_type = share_info.split('_')[1]

        logging.info('==========edit and save File==========')
        ov = OpenView(self.driver)
        ov.open_random_file(SEARCH_DICT[file_type])

        gv = GeneralView(self.driver)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_mode').click()
        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type, 1)

        cv = CreateView(self.driver)
        cv.save_file()
        self.assertTrue(cv.get_toast_message('Saved to local'))

        logging.info('==========share new File==========')
        gv = GeneralView(self.driver)
        gv.share_file(file_type, share_type)

    @unittest.skip('skip test_file_info')
    @data(*WPS)
    def test_file_info(self, file_type):
        """
        文档信息
        :param file_type: 文档类型：'wp', 'ss', 'pg'
        :return: None
        """
        logging.info('==========test_share_newFile==========')
        ov = OpenView(self.driver)
        ov.open_random_file(SEARCH_DICT[file_type])

        logging.info('==========show file info==========')
        gv = GeneralView(self.driver)
        gv.wait_loading()
        gv.file_info()

    logging.info('==========test auto shapes==========')
    @unittest.skip('skip test_pop_menu_shape')
    @data(*WPS)
    def test_pop_menu_shape(self, file_type='wp'):
        logging.info('==========test_pop_menu_shape==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type)
        time.sleep(1)
        if file_type == 'pg':
            gv.tap(550, 450)
            gv.pop_menu_click('editText')
        else:
            gv.tap(700, 700, 2)
            gv.tap(700, 700, 3)

        for i in range(50):
            self.driver.press_keycode(random.randint(29, 54))

        if file_type == 'pg':
            gv.drag_coordinate(550, 830, 500, 800)
            gv.pop_menu_click('copy')
            gv.tap(550, 830)
            time.sleep(1)
            gv.long_press(550, 830)
            gv.pop_menu_click('paste')
            gv.drag_coordinate(550, 830, 500, 800)
            gv.pop_menu_click('cut')
            gv.tap(550, 830)
            time.sleep(1)
            gv.long_press(550, 830)
            gv.pop_menu_click('paste')
            gv.drag_coordinate(550, 830, 500, 800)
            gv.pop_menu_click('delete')
        else:
            gv.drag_coordinate(700, 700, 550, 550)
            gv.pop_menu_click('copy')
            gv.tap(700, 700)
            time.sleep(1)
            gv.long_press(700, 700)
            gv.pop_menu_click('paste')
            gv.drag_coordinate(700, 700, 550, 550)
            gv.pop_menu_click('cut')
            gv.tap(700, 700)
            time.sleep(1)
            gv.long_press(700, 700)
            gv.pop_menu_click('paste')
            gv.drag_coordinate(700, 700, 550, 550)
            gv.pop_menu_click('delete')

    @unittest.skip('skip test_shape_attr')
    @data(*WPS)
    def test_shape_attr(self, file_type):
        logging.info('==========test_shape_attr==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type, 6, 30)
        gv.shape_insert(file_type, 6, 31)
        gv.shape_insert(file_type, 6, 32)
        gv.shape_insert(file_type, 6, 33)
        ele1 = '//*[@text=" Shape "]'
        ele2 = '//*[@text=" Outline "]'
        ele3 = '//*[@text=" Effect "]'
        if file_type == 'pg':
            ele0 = '//*[@text=" Insert "]'
            gv.swipe_ele(ele0, ele1)
        gv.swipe_ele(ele2, ele1)
        gv.swipe_ele(ele3, ele1)
        gv.shape_layer(' Send Backward ')
        gv.shape_layer(' Send to Back ')
        gv.shape_layer(' Bring Forward ')
        gv.shape_layer(' Bring to Front ')

    @unittest.skip('skip test_pop_menu_shape1')
    @data(*WPS)
    def test_pop_menu_shape1(self, file_type):
        logging.info('==========test_pop_menu_shape1_ws==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)

        if file_type == 'pg':
            pg = PGView(self.driver)
            gv.group_button_click(' Edit ')
            pg.edit_format('空白')

        time.sleep(1)
        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type)

        gv.fold_expand()
        x1, y1 = gv.find_pic_position('drag_all')
        gv.drag_coordinate(x1, y1, x1 - 100, y1)

        x1, y1 = gv.find_pic_position('drag_all')
        gv.drag_coordinate(x1, y1, x1 + 100, y1)

        x1, y1 = gv.find_pic_position('drag_all')
        gv.drag_coordinate(x1, y1, x1 - 50, y1 - 50)

        x2, y2 = gv.find_pic_position('drag_all1')
        gv.drag_coordinate(x2, y2, x2, y2 - 100)

        x2, y2 = gv.find_pic_position('drag_all1')
        gv.drag_coordinate(x2, y2, x2, y2 + 100)

        x2, y2 = gv.find_pic_position('drag_all1')
        gv.drag_coordinate(x2, y2, x2 - 50, y2 - 50)

        x, y = gv.find_pic_position('rotate_free')
        gv.drag_coordinate(x, y, x + 50, y + 50)

    @unittest.skip('skip test_shape_attr1')
    @data(*WPS)
    def test_shape_attr1(self, file_type):  # 文本框字符属性
        logging.info('==========test_shape_attr1==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        x1, y1 = 0, 0
        if file_type == 'ss':
            ss = SSView(self.driver)
            x1, y1, w, h = ss.cell_location()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/formulabar_ok').click()

        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type)
        time.sleep(1)
        x, y = gv.find_pic_position('drag_all')
        gv.tap(x, y)  # 进入编辑
        gv.pop_menu_click('editText')

        if file_type == 'ss':
            gv.fold_expand()
            gv.fold_expand()
            x, y = gv.find_pic_position('drag_all')
            gv.tap(x, y)  # 进入编辑
            gv.pop_menu_click('editText')

        for i in range(50):
            self.driver.press_keycode(random.randint(7, 16))

        if file_type == 'pg':
            gv.tap(250, 250)
            gv.tap(550, 850)
        elif file_type == 'ss':
            gv.tap(x1, y1)
            gv.tap(x, y)
        else:
            gv.tap(250, 450)
            time.sleep(1)
            gv.fold_expand()
            gv.tap(x, y)
            time.sleep(1)
        gv.fold_expand()

        gv.shape_option(file_type, 5, width=5, height=5)
        gv.shape_option(file_type, 6, top=0.5, bottom=0.5, left=0.5, right=0.5)
        ele1 = '//*[@text=" Shape "]'
        ele2 = '//*[@text=" Outline "]'
        ele3 = '//*[@text=" Effect "]'
        if file_type == 'pg':
            ele0 = '//*[@text=" Insert "]'
            gv.swipe_ele(ele0, ele1)
        gv.swipe_ele(ele2, ele1)
        gv.swipe_ele(ele3, ele1)
        gv.shape_content_align(file_type, '右对齐', '下对齐')
        gv.shape_content_align(file_type)
        gv.shape_content_align(file_type, '水平居中', '垂直居中')
        time.sleep(3)

    @unittest.skip('skip test_shape_attr2')
    @data(*WPS)
    def test_shape_attr2(self, file_type):
        logging.info('==========test_shape_attr2==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type, 6, 10)
        gv.shape_option(file_type, 2)
        gv.shape_fill_color(file_type, 6, 24)
        gv.shape_fill_color_transparency(5)
        ele1 = '//*[@text=" Shape "]'
        ele2 = '//*[@text=" Outline "]'
        if file_type == 'pg':
            ele0 = '//*[@text=" Insert "]'
            gv.swipe_ele(ele0, ele1)
        gv.swipe_ele(ele2, ele1)
        gv.shape_border_color(file_type, 6, 5)
        gv.shape_border_type(file_type, 6, 3)
        gv.shape_border_width(file_type, 6, 5)
        gv.shape_effect_type(file_type, 6, 4, 5)
        time.sleep(1)

    @unittest.skip('skip test_insert_shape')
    @data(*WPS)
    def test_insert_shape(self, file_type):
        logging.info('==========test_insert_shape==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)

        gv = GeneralView(self.driver)
        ss = SSView(self.driver)
        # ss.insert_chart()
        gv.group_button_click(' Insert ')
        gv.insert_shape(file_type)
        for i in range(5):
            gv.shape_insert(file_type, 6, random.randint(1, 42))
        time.sleep(3)

    @unittest.skip('skip test_expand_fold')
    @data(*WPS)
    def test_expand_fold(self, file_type):  # 编辑栏收起展开
        logging.info('==========test_expand_fold==========')
        suffix = SEARCH_DICT[file_type]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)
        gv = GeneralView(self.driver)
        gv.switch_write_read()
        gv.fold_expand()
        gv.fold_expand()

    logging.info('==========test signature==========')

    @unittest.skip('skip test_signature')
    @data(*WPS)
    def test_signature(self, file_type):  # 签批
        logging.info('==========test_signature==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        gv.group_button_click(' Signature ')
        gv.use_finger(file_type)
        gv.use_finger(file_type)
        gv.pen_type(file_type, '钢笔')
        gv.pen_color(file_type, 15)
        gv.pen_size(file_type, 3)
        gv.swipe(300, 400, 800, 400, 500)
        gv.pen_type(file_type, '荧光笔')
        gv.pen_color(file_type, 30)
        gv.pen_size(file_type, 6)
        gv.swipe(300, 600, 800, 600, 500)
        gv.pen_type(file_type, '擦除')
        gv.swipe(200, 400, 900, 400, 500)
        gv.swipe(200, 600, 900, 600, 500)
        time.sleep(3)

    logging.info('==========unknow==========')
    @unittest.skip('skip test_insert_pic1')
    def test_insert_pic1(self, file_type='ss'):
        logging.info('==========test_insert_pic==========')
        suffix = SEARCH_DICT[file_type]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)
        gv = GeneralView(self.driver)
        gv.switch_write_read()
        gv.group_button_click(' Insert ')

        gv.insert_pic()
        gv.pic_option(file_type, 5, 4, 4)
        ele1 = '//*[@text=" Picture "]'
        ele2 = '//*[@text=" Outline "]'
        # ele3 = '//*[@text="文字环绕"]'
        # ele4 = '//*[@text="叠放次序"]'
        gv.swipe_ele(ele2, ele1)
        if file_type == 'wp':
            gv.text_wrap(' Square ')
            gv.text_wrap(' In Line with Text ')
            gv.text_wrap(' Tight ')
            gv.text_wrap(' Behind Text ')
            gv.text_wrap(' In Front of Text ')

        x, y = gv.find_pic_position('drag_pic')
        gv.tap(x, y)
        gv.pop_menu_click('cut')
        if file_type == 'wp':
            gv.long_press(x, y)
        else:
            gv.tap(x + 100, y)
            gv.tap(x + 100, y)
        gv.pop_menu_click('paste')

        x, y = gv.find_pic_position('drag_pic')
        gv.tap(x, y)
        x, y = gv.find_pic_position('rotate_90')
        gv.swipe(x, y, x - 50, y)

        gv.pop_menu_click('save_to_album')

        gv.pop_menu_click('delete')

    @unittest.skip('skip test_insert_pic')
    def test_insert_pic(self, file_type='ss'):
        logging.info('==========test_insert_pic==========')
        cv = CreateView(self.driver)
        gv = GeneralView(self.driver)
        cv.create_file(file_type)
        cv.group_button_click(' Insert ')

        gv.insert_pic()
        gv.pic_option(file_type, 5, 4, 4)
        gv.pic_option(file_type, 1)
        ele1 = '//*[@text=" Picture "]'
        ele2 = '//*[@text=" Outline "]'
        # ele3 = '//*[@text="文字环绕"]'
        # ele4 = '//*[@text="叠放次序"]'
        gv.swipe_ele(ele2, ele1)
        if file_type == 'wp':
            gv.text_wrap()

        x, y = gv.find_pic_position('rotate_free')
        gv.swipe(x, y, x + 100, y + 100)

        x, y = gv.find_pic_position('drag_all')
        gv.tap(x, y)
        gv.pop_menu_click('copy')
        gv.tap(x, y)
        gv.pop_menu_click('paste')
        gv.tap(x, y)
        gv.pop_menu_click('paste')
        gv.shape_layer(' Send Backward ')
        gv.shape_layer(' Send to Back ')
        gv.shape_layer(' Bring Forward ')
        gv.shape_layer(' Bring to Front ')

    @unittest.skip('skip test_insert_chart1')
    @data(*PS)
    def test_insert_chart1(self, file_type):
        logging.info('==========test_insert_chart1==========')
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        ss = SSView(self.driver)

        time.sleep(1)
        if file_type == 'ss':
            x, y, width, height = ss.cell_location()
            for i in range(3):
                cv.tap(x + width * 0.5, y + height * (i + 0.5))
                ss.cell_edit()  # 双击进入编辑
                self.driver.press_keycode(random.randint(7, 16))
            gv.drag_coordinate(x, y + height * 2, x, y)

        gv.group_button_click(' Insert ')
        if file_type == 'pg':
            ele1 = '//*[@text=" Slide "]'
            ele2 = '//*[@text=" Picture "]'
            gv.swipe_ele(ele2, ele1)
        gv.insert_chart_insert(' Column Chart ', random.randint(1, 9))
        gv.chart_color(random.randint(1, 8))
        gv.chart_element(file_type, '大标题', 1, 1, 1)
        gv.chart_element_XY('x', 'x', 0, 1, 1, 1, 1, 1)
        gv.chart_element_XY('y', 'y', 0, 1, 1, 0, 1, 0)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()
        gv.change_row_column()
        time.sleep(3)

    @unittest.skip('skip test_insert_chart')
    @data(*PS)
    def test_insert_chart(self, file_type):  # Insert 图表，仅ss，pg
        logging.info('==========test_insert_chart==========')
        chart_list = [' Column Chart ', ' Bar Chart ', ' Line Chart ', ' Pie Chart ', ' Scatter Chart ', ' Area Chart ',
                      ' Doughnut Chart ', ' Radar Chart ', ' Bubble Chart ', ' Cylind Chart ', ' Cone Chart ',
                      ' Pyramid Chart ']
        cv = CreateView(self.driver)
        cv.create_file(file_type)
        gv = GeneralView(self.driver)
        ss = SSView(self.driver)

        time.sleep(1)
        if file_type == 'ss':
            x, y, width, height = ss.cell_location()
            for i in range(3):
                cv.tap(x + width * 0.5, y + height * (i + 0.5))
                ss.cell_edit()  # 双击进入编辑
                self.driver.press_keycode(random.randint(7, 16))
            gv.drag_coordinate(x, y + height * 2, x, y)

        for i in range(3):
            gv.group_button_click(' Insert ')
            if file_type == 'pg' and i == 0:
                ele1 = '//*[@text=" Slide "]'
                ele2 = '//*[@text=" Picture "]'
                gv.swipe_ele(ele2, ele1)
            gv.insert_chart_insert(chart_list[i], random.randint(1, 9))
            gv.chart_template()
        ele1 = '//*[@text=" Chart "]'
        ele2 = '//*[@text=" Chart Type "]'
        gv.swipe_ele(ele2, ele1)
        gv.shape_layer(' Send Backward ')
        gv.shape_layer(' Send to Back ')
        gv.shape_layer(' Bring Forward ')
        gv.shape_layer(' Bring to Front ')

        time.sleep(3)

    @unittest.skip('skip test_scroll_screen')
    @data(*WPS)
    def test_scroll_screen(self, file_type):  # 滚屏
        logging.info('==========test_scroll_screen==========')
        suffix = SEARCH_DICT[file_type]
        ov = OpenView(self.driver)
        ov.open_random_file(suffix)
        if file_type == 'pg':
            time.sleep(3)
            ov.swipeLeft()
            ov.swipeLeft()
            ov.swipeRight()
        elif file_type == 'ss':
            time.sleep(3)
            ov.swipeLeft()
            ov.swipeLeft()
            ov.swipeRight()
            ov.swipeUp()
            ov.swipeUp()
            ov.swipeDown()
        else:
            time.sleep(3)
            ov.swipeUp()
            ov.swipeUp()
            ov.swipeDown()
        time.sleep(3)


