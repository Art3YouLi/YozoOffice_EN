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

class TestWp(StartEnd):
    def template_object(self, filename):
        pro_path = ST.PROJECT_ROOT
        clickpic_path = os.path.join(pro_path, 'clickPicture_CN')
        t = Template(os.path.join(clickpic_path, filename), resolution=(1080, 1920), rgb=True, threshold=0.5)
        return t

    @unittest.skip('skip test_wp_read_self_adaption')
    def test_wp_read_self_adaption(self):  # wp阅读自适应
        logging.info('==========test_wp_read_self_adaption==========')
        ov = OpenView(self.driver)
        ov.open_file('欢迎使用永中Office.docx')
        wp = WPView(self.driver)
        wp.read_self_adaption()
        time.sleep(1)
        self.assertFalse(wp.get_element_result('//*[@resource-id="com.yozo.office:id/yozo_ui_toolbar_button_close"]'),
                         'read self adaption set fail!')

    @unittest.skip('skip test_wp_pop_menu_text')
    def test_wp_pop_menu_text(self):
        logging.info('==========test_pop_menu_text_wp==========')
        cv = CreateView(self.driver)
        type = 'wp'
        cv.create_file(type)
        gv = GeneralView(self.driver)

        time.sleep(1)
        gv.tap(700, 700)
        for i in range(100):
            self.driver.press_keycode(random.randint(29, 54))
        gv.drag_coordinate(300, 540, 300, 200)
        gv.pop_menu_click('copy')
        gv.tap(700, 700)
        time.sleep(1)
        gv.long_press(700, 700)
        gv.pop_menu_click('paste')
        gv.drag_coordinate(300, 540, 300, 200)
        gv.pop_menu_click('cut')
        gv.tap(700, 700)
        time.sleep(1)
        gv.long_press(700, 700)
        gv.pop_menu_click('paste')

        time.sleep(3)

    @unittest.skip('skip test_wp_shape_text_attr')
    def test_wp_shape_text_attr(self):  # 自选图形文本属性，仅WP和PG
        logging.info('==========test_wp_shape_text_attr==========')
        type = 'wp'
        cv = CreateView(self.driver)
        cv.create_file(type)
        gv = GeneralView(self.driver)
        gv.group_button_click('插入')
        gv.insert_shape(type, 1)
        gv.tap(680, 750)
        gv.pop_menu_click('editText')
        time.sleep(1)
        gv.group_button_click('编辑')
        gv.font_name(type, 'AndroidClock')
        gv.font_size(15)
        gv.font_style(type, '倾斜')
        gv.font_color(type, 6, 29)
        gv.swipe_ele('//*[@text="字体颜色"]', '//*[@text="编辑"]')
        time.sleep(1)
        for i in range(20):
            self.driver.press_keycode(random.randint(29, 54))
        time.sleep(1)
        gv.swipe_ele('//*[@text="高亮颜色"]', '//*[@text="编辑"]')
        gv.drag_coordinate(680, 750, 680, 600)
        gv.high_light_color(type, 6, random.randint(1, 15))
        gv.bullets_numbers(type, 6, 10)
        gv.text_align(type, '分散对齐')
        gv.text_align(type, '右对齐')
        gv.text_line_space(type, 1.5)
        gv.text_line_space(type, 3)
        gv.text_indent(type, '右缩进')
        gv.text_indent(type, '右缩进')
        gv.text_indent(type, '左缩进')
        time.sleep(3)

    @unittest.skip('skip test_wp_pop_menu_text')
    def test_wp_pop_menu_text(self):
        logging.info('==========test_pop_menu_text_wp==========')
        cv = CreateView(self.driver)
        type = 'wp'
        cv.create_file(type)
        gv = GeneralView(self.driver)

        time.sleep(1)
        gv.tap(700, 700)
        for i in range(100):
            self.driver.press_keycode(random.randint(29, 54))
        gv.drag_coordinate(300, 540, 300, 200)
        gv.pop_menu_click('copy')
        gv.tap(700, 700)
        time.sleep(1)
        gv.long_press(700, 700)
        gv.pop_menu_click('paste')
        gv.drag_coordinate(300, 540, 300, 200)
        gv.pop_menu_click('cut')
        gv.tap(700, 700)
        time.sleep(1)
        gv.long_press(700, 700)
        gv.pop_menu_click('paste')

        time.sleep(3)

    @unittest.skip('skip test_wp_bookmark')
    def test_wp_bookmark(self):
        logging.info('==========test_wp_bookmark==========')
        ov = OpenView(self.driver)
        ov.open_file('欢迎使用永中Office.docx')
        wp = WPView(self.driver)
        wp.group_button_click('查看')
        wp.add_bookmark('test')
        self.assertTrue(wp.check_add_bookmark(), '书签插入失败！')
        wp.swipeUp()
        wp.swipeUp()
        wp.group_button_click('查看')
        wp.list_bookmark('test')

    @unittest.skip('skip test_wp_jump')
    def test_wp_jump(self):  # 跳转页
        logging.info('==========test_wp_bookmark==========')
        ov = OpenView(self.driver)
        ov.open_file('欢迎使用永中Office.docx')
        wp = WPView(self.driver)
        wp.group_button_click('查看')
        wp.page_jump(7)
        time.sleep(2)

    @unittest.skip('skip test_wp_font_attr')
    def test_wp_font_attr(self):
        logging.info('==========test_wp_font_attr===========')
        cv = CreateView(self.driver)
        type = 'wp'
        cv.create_file(type)
        time.sleep(1)
        wp = WPView(self.driver)
        wp.group_button_click('编辑')
        wp.font_size(16)
        # wp.font_name(type)
        wp.font_style(type, '倾斜')
        wp.font_color(type, 3)
        ele1 = '//*[@text="编辑"]'
        ele2 = '//*[@text="字体颜色"]'
        ele3 = '//*[@text="高亮颜色"]'
        ele4 = '//*[@text="分栏"]'
        wp.swipe_ele(ele2, ele1)
        time.sleep(1)
        wp.tap(450, 450)
        for i in range(100):
            self.driver.press_keycode(random.randint(29, 54))
        wp.group_button_click('编辑')
        wp.drag_coordinate(450, 500, 200, 500)
        wp.high_light_color(type, 3)
        wp.bullets_numbers(type, 6, 14)
        wp.text_align(type, '右对齐')
        wp.swipe_ele(ele3, ele1)
        wp.text_line_space(type, 2.5)
        wp.text_indent(type, '右缩进')
        wp.swipe_ele(ele4, ele1)
        wp.text_columns(4)
        wp.text_columns(3)
        wp.text_columns(2)
        time.sleep(3)

    @unittest.skip('skip test_wp_insert_testbox')
    def test_wp_insert_testbox(self):
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.get_element('//*[@resource-id="com.yozo.office:id/yozo_ui_%s_option_id_insert_shape"]'
                       '/android.widget.FrameLayout[1]' % type).click()
        time.sleep(1)

    @unittest.skip('skip test_wp_table_attr_1_type')
    def test_wp_table_attr_1_type(self):
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.insert_example_table()
        wp = WPView(self.driver)
        wp.table_type_list()

    @unittest.skip('skip test_wp_insert_watermark')
    def test_wp_insert_watermark(self):
        logging.info('==========test_wp_insert_watermark==========')
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.insert_watermark('YOZO')
        time.sleep(1)
        wp.group_button_click('插入')
        wp.insert_watermark('yozo', delete='delete')
        time.sleep(3)

    @unittest.skip('skip test_wp_insert_watermark')
    def test_wp_insert_watermark(self):
        logging.info('==========test_wp_insert_watermark==========')
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.insert_watermark('YOZO')
        time.sleep(1)
        wp.group_button_click('插入')
        wp.insert_watermark('yozo', delete='delete')
        time.sleep(3)

    @unittest.skip('skip test_wp_check_approve')
    def test_wp_check_approve(self):  # 修订
        logging.info('==========test_wp_check_approve==========')
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('审阅')
        wp.change_name('super_root')
        wp.group_button_click('审阅')
        wp.revision_on_off('开启')
        wp.tap(450, 550)
        for i in range(20):
            self.driver.press_keycode(random.randint(29, 54))
        wp.group_button_click('审阅')
        wp.revision_accept_not('yes')
        wp.tap(450, 550)
        for i in range(20):
            self.driver.press_keycode(random.randint(29, 54))
        wp.group_button_click('审阅')
        wp.revision_accept_not()
        wp.group_button_click('审阅')
        wp.revision_on_off('关闭')
        time.sleep(3)

    @unittest.skip('skip test_wp_shape_fixed_rotate')
    def test_wp_shape_fixed_rotate(self):  # 形状四种固定旋转角度
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.get_element('//*[@resource-id="com.yozo.office:id/yozo_ui_%s_option_id_insert_shape"]'
                       '/android.widget.FrameLayout[3]' % type).click()
        wp = WPView(self.driver)
        for i in range(1, 5):
            wp.get_element('//*[@resource-id="com.yozo.office:id/yozo_ui_%s_option_id_shape_quick_function"]'
                           '/android.widget.FrameLayout[%s]' % (type1, i)).click()
            # print(i)

    @unittest.skip('skip test_wp_pop_menu_shape_all')
    def test_wp_pop_menu_shape_all(self, type1='wp'):
        cv = CreateView(self.driver)
        cv.create_file(type1)
        wp = WPView(self.driver)
        time.sleep(1)
        wp.pinch()
        wp.group_button_click('插入')
        wp.insert_shape(type1, index=3)
        wp.fold_expand()
        touch(self.template_object('rotate_free.png'))
        touch(self.template_object('editText.png'))  # 编辑文字
        touch(self.template_object('rotate_free.png'))
        touch(self.template_object('copy.png'))  # 复制
        touch(self.template_object('rotate_free.png'))
        touch(self.template_object('cut.png'))  # 剪切
        touch(self.template_object('point.png'))
        touch(self.template_object('paste.png'))  # 粘贴
        touch(self.template_object('rotate_free.png'))
        swipe(self.template_object('editText.png'), self.template_object('copy.png'))
        touch(self.template_object('rotate_90.png'))
        touch(self.template_object('rotate_free.png'))
        touch(self.template_object('delete.png'))  # 删除

        time.sleep(10)

    @unittest.skip('skip test_wp_shape_text_attr')
    def test_wp_shape_text_attr(self):  # 自选图形文本属性，仅WP和PG
        logging.info('==========test_wp_shape_text_attr==========')
        type = 'wp'
        cv = CreateView(self.driver)
        cv.create_file(type)
        gv = GeneralView(self.driver)
        gv.group_button_click('插入')
        gv.insert_shape(type, 1)
        gv.tap(680, 750)
        gv.pop_menu_click('editText')
        time.sleep(1)
        gv.group_button_click('编辑')
        gv.font_name(type, 'AndroidClock')
        gv.font_size(15)
        gv.font_style(type, '倾斜')
        gv.font_color(type, 6, 29)
        gv.swipe_ele('//*[@text="字体颜色"]', '//*[@text="编辑"]')
        time.sleep(1)
        for i in range(20):
            self.driver.press_keycode(random.randint(29, 54))
        time.sleep(1)
        gv.swipe_ele('//*[@text="高亮颜色"]', '//*[@text="编辑"]')
        gv.drag_coordinate(680, 750, 680, 600)
        gv.high_light_color(type, 6, random.randint(1, 15))
        gv.bullets_numbers(type, 6, 10)
        gv.text_align(type, '分散对齐')
        gv.text_align(type, '右对齐')
        gv.text_line_space(type, 1.5)
        gv.text_line_space(type, 3)
        gv.text_indent(type, '右缩进')
        gv.text_indent(type, '右缩进')
        gv.text_indent(type, '左缩进')
        time.sleep(3)

    @unittest.skip('skip test_wp_pic_fixed_rotate')
    def test_wp_pic_fixed_rotate(self, type1):  # 图片四种固定旋转角度
        cv = CreateView(self.driver)
        cv.create_file(type1)
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.insert_pic()
        wp = WPView(self.driver)
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1
        for i in range(1, 5):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()

    @unittest.skip('skip test_wp_pic_width_to_height')
    def test_wp_pic_width_to_height(self):
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.insert_pic()
        wp = WPView(self.driver)
        if type1 == 'wp':
            s = wp.swipe_option('up')
            while not wp.exist('//*[@text="文字环绕"]'):
                wp.swipe(s[0], s[1], s[2], s[3])
            wp.text_wrap('四周型')
            ele1 = '//*[@resource-id="com.yozo.office:id/yozo_ui_wp_option_id_picture_broad"]'
            ele2 = '//*[@text="叠放次序"]'
            wp.swipe_ele(ele1, ele2)
        cc = "com.yozo.office:id/yozo_ui_wp_option_id_picture_edit"
        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        # 属性调整大小
        wp.shape_option_5()
        # 手势拖拉大小控制点
        x, y = loop_find(self.template_object('drag_pic.png'))
        wp.swipe(x, y, 500, 1000)
        time.sleep(10)

    @unittest.skip('skip test_wp_pic_shadow')
    def test_wp_pic_shadow(self, type1='wp'):
        # type1 = 'wp'
        self.insert_pic_rect(type1)
        wp = WPView(self.driver)
        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_quick_function"
        # else:
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1

        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        # 属性调整大小
        wp.shape_option_5()
        if not wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()
        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_effect_type"
        # else:
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_effect" % type1
        for i in range(1, 7):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()

        cc = 'com.yozo.office:id/yozo_ui_option_id_object_effect_shadow'
        for i in range(1, 6):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()
        time.sleep(10)

    def test_wp_pic_outline_color(self, type1='wp'):
        # type1 = 'wp'
        self.insert_pic_rect(type1)
        wp = WPView(self.driver)
        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_quick_function"
        # else:
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1
        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        # 属性调整大小
        wp.shape_option_5()
        if not wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()

        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_border_color"
        # elif type1 == 'wp':
        cc = "com.yozo.office:id/yozo_ui_wp_option_id_picture_broad"
        # elif type1 == 'ss':
        #     cc = "com.yozo.office:id/yozo_ui_ss_option_id_picture_broad_color"
        s = wp.swipe_option('up')
        while not wp.exist('//*[@resource-id="%s"]' % cc):
            wp.swipe(s[0], s[1], s[2], s[3])
        for i in range(1, 7):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()
        cc = 'com.yozo.office:id/yozo_ui_option_id_color_all'
        list(map(lambda i: wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[%s]' % (cc, i)).click(), range(1, 43)))
        # for i in range(1, 43):
        #     wp.get_element(
        #         '//*[@resource-id="%s"]'
        #         '/android.widget.FrameLayout[%s]' % (cc, i)).click()

    def test_wp_pic_outline_border_type(self, type1='wp'):
        # type1 = 'wp'
        self.insert_pic_rect(type1)
        wp = WPView(self.driver)
        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_quick_function"
        # else:
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1
        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        # 属性调整大小
        wp.shape_option_5()
        if not wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()

        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_border_type"
        # elif type1 == 'wp':
        cc = "com.yozo.office:id/yozo_ui_wp_option_id_picture_border_type"
        # elif type1 == 'ss':
        #     cc = "com.yozo.office:id/yozo_ui_ss_option_id_picture_border_type"
        s = wp.swipe_option('up')
        while not wp.exist('//*[@resource-id="%s"]' % cc):
            wp.swipe(s[0], s[1], s[2], s[3])
        for i in range(1, 7):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()
        cc = 'com.yozo.office:id/yozo_ui_shape_border_type'
        for i in range(1, 8):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()

    def test_wp_pic_outline_border_px(self, type1='wp'):
        # type1 = 'wp'
        self.insert_pic_rect(type1)
        wp = WPView(self.driver)
        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_quick_function"
        # else:
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1
        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        # 属性调整大小
        wp.shape_option_5()
        if not wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()

        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_border_width"
        # elif type1 == 'wp':
        cc = "com.yozo.office:id/yozo_ui_wp_option_id_picture_border_width"
        # elif type1 == 'ss':
        #     cc = "com.yozo.office:id/yozo_ui_ss_option_id_picture_border_width"
        s = wp.swipe_option('up')
        while not wp.exist('//*[@resource-id="%s"]' % cc):
            wp.swipe(s[0], s[1], s[2], s[3])
        for i in range(1, 7):
            wp.get_element(
                '//*[@resource-id="%s"]'
                '/android.widget.FrameLayout[%s]' % (cc, i)).click()
        # cc = 'com.yozo.office:id/yozo_ui_option_id_objec_border_width_select'
        for i in range(30):
            wp.get_element(
                '//*[@resource-id="com.yozo.office:id/yozo_ui_number_picker_arrow_right"]').click()

    def test_wp_pic_text_round(self):
        # 仅wp存在文字环绕功能
        self.insert_pic_rect('wp')
        wp = WPView(self.driver)
        s = wp.swipe_option('up')
        while not wp.exist('//*[@text="文字环绕"]'):
            wp.swipe(s[0], s[1], s[2], s[3])
        wp.text_wrap('四周型')
        wp.text_wrap('嵌入型')
        wp.text_wrap('紧密型')
        wp.text_wrap('衬于文字下方')
        wp.text_wrap()

    def test_wp_pic_order(self, type1='wp'):
        # type1 = 'wp'
        self.insert_pic_rect(type1)
        wp = WPView(self.driver)
        if type1 == 'wp':
            s = wp.swipe_option('up')
            while not wp.exist('//*[@text="文字环绕"]'):
                wp.swipe(s[0], s[1], s[2], s[3])
            wp.text_wrap('四周型')

        # if type1 == 'pg':
        #     cc = "com.yozo.office:id/yozo_ui_pg_option_id_picture_quick_function"
        # else:
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1
        if type1 == 'wp':
            s = wp.swipe_option('down')
            while not wp.exist('//*[@resource-id="%s"]' % cc):
                wp.swipe(s[0], s[1], s[2], s[3])
        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        # 属性调整大小
        wp.shape_option_5()
        if wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()
        # if type1 == 'pg':
        #     pic_png = 'rotate_free.png'
        # else:
        pic_png = 'drag_pic.png'
        touch(self.template_object(pic_png))
        touch(self.template_object('copy.png'))
        touch(self.template_object(pic_png))
        touch(self.template_object('paste.png'))
        touch(self.template_object(pic_png))
        touch(self.template_object('paste.png'))
        if not wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()
        ele1 = '//*[@text="图片"]'
        ele2 = '//*[@text="轮廓"]'
        wp.swipe_ele(ele2, ele1)
        wp.shape_layer('置于底层')
        wp.shape_layer('上移一层')
        wp.shape_layer('置于顶层')
        wp.shape_layer('下移一层')
        if type1 == 'wp':
            wp.shape_layer('衬于文字下方')
            wp.shape_layer('浮于文字上方')

    def wp_insert_table(self):
        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        wp.group_button_click('插入')
        wp.insert_example_table()

    def test_wp_insert_table(self):
        self.wp_insert_table()

    def test_wp_table_attr_2_fill_color(self):
        self.wp_insert_table()
        wp = WPView(self.driver)
        wp.fill_color()

    def test_wp_table_attr_3_border_line(self):
        self.wp_insert_table()
        wp = WPView(self.driver)
        wp.border_line()

    def test_wp_table_attr_4_insert_row_col(self):
        self.wp_insert_table()
        wp = WPView(self.driver)
        s = wp.swipe_option('up')
        while not wp.exist('//*[@text="插入行或者列"]'):
            wp.swipe(s[0], s[1], s[2], s[3])
        wp.insert_row_col(direction='up')
        wp.insert_row_col(direction='down')
        wp.insert_row_col(direction='left')
        wp.insert_row_col(direction='light')

    def test_wp_table_attr_5_delete_table(self):
        self.wp_insert_table()
        wp = WPView(self.driver)
        s = wp.swipe_option('up')
        while not wp.exist('//*[@text="删除行或者列"]'):
            wp.swipe(s[0], s[1], s[2], s[3])
        wp.delete_table_row_col_all(del0='row')
        wp.delete_table_row_col_all(del0='col')
        wp.delete_table_row_col_all(del0='all')

    def test_wp_shape_text_round(self):
        # 仅wp存在文字环绕功能
        self.insert_shape_rect('wp')
        wp = WPView(self.driver)
        s = wp.swipe_option('up')
        while not wp.exist('//*[@text="文字环绕"]'):
            wp.swipe(s[0], s[1], s[2], s[3])
        wp.text_wrap('四周型')
        wp.text_wrap('嵌入型')
        wp.text_wrap('紧密型')
        wp.text_wrap('衬于文字下方')
        wp.text_wrap()

    def test_wp_pop_menu_pic_all(self, type1='wp'):
        self.inserttest_wp_insert_testbox_pic_rect(type1)
        wp = WPView(self.driver)
        s = wp.swipe_option('up')
        while not wp.exist('//*[@text="文字环绕"]'):
            wp.swipe(s[0], s[1], s[2], s[3])
        wp.text_wrap('四周型')

        # 属性调整大小
        cc = "com.yozo.office:id/yozo_ui_%s_option_id_picture_edit" % type1
        s = wp.swipe_option('down')
        while not wp.exist('//*[@resource-id="%s"]' % cc):
            wp.swipe(s[0], s[1], s[2], s[3])
        wp.get_element(
            '//*[@resource-id="%s"]'
            '/android.widget.FrameLayout[5]' % cc).click()
        wp.shape_option_5()
        if wp.exist('//*[@resource-id="com.yozo.office:id/yozo_ui_option_content_container"]'):
            wp.fold_expand()

        touch(self.template_object('chart_all1.png'))
        touch(self.template_object('copy.png'))  # 复制
        touch(self.template_object('chart_all1.png'))
        touch(self.template_object('cut.png'))  # 剪切
        touch(self.template_object('point.png'))
        touch(self.template_object('paste.png'))  # 粘贴
        touch(self.template_object('rotate_free.png'))
        swipe(self.template_object('editText.png'), self.template_object('copy.png'))
        touch(self.template_object('rotate_90.png'))
        touch(self.template_object('rotate_free.png'))
        touch(self.template_object('save_to_album.png'))  # 存至相册
        touch(self.template_object('rotate_free.png'))
        touch(self.template_object('edit_pic.png'))  # 裁剪
        touch(self.template_object('delete.png'))  # 删除

    def test_wp_insert_chart_list(self):

        cv = CreateView(self.driver)
        cv.create_file('wp')
        wp = WPView(self.driver)
        chart_type = ['柱形图', '条形图', '折线图', '饼图', '散点图', '面积图', '圆环图', '雷达图', '气泡图', '圆柱图', '圆锥图', '棱锥图']
        for i in chart_type:
            wp.group_button_click('插入')
            s = wp.swipe_option('up')
            while not wp.exist('//*[@text="图表"]'):
                wp.swipe(s[0], s[1], s[2], s[3])
            wp.get_element('//*[@text="图表"]').click()
            while not wp.exist('//*[@text="%s"]' % i):
                wp.swipe(s[0], s[1], s[2], s[3])
            wp.get_element('//*[@text="%s"]' % i).click()
            wp.chart_list('%s' % i)


