#!/user/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from businessView.generalView import GeneralView


class PGView(GeneralView):
    def edit_format(self, format):  # 版式
        logging.info('==========edit_format==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_option_id_edit_format').click()
        range = '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout'
        format_ele = '//*[@text="%s"]' % format
        self.swipe_search2(format_ele, range)
        self.driver.find_element(By.XPATH, format_ele).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def edit_template(self, template):  # 模板
        logging.info('==========edit_template==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_option_id_edit_templet').click()
        range = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout'
        eles = self.driver.find_elements(By.XPATH, range)
        template_ele = '%s[@index="%s"]' % (range, template)
        if int(template) > 8:
            self.swipe_ele1(eles[-1], eles[0])
        self.driver.find_element(By.XPATH, template_ele).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def add_new(self):  # 新建
        logging.info('==========add_new==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/a0000_pg_add_slide_button_id').click()

    def thumbnail_scroll(self):  # 缩略图滚屏
        logging.info('==========thumbnail_scroll==========')
        eles = self.driver.find_elements(By.XPATH,
                                         '//android.widget.HorizontalScrollView/android.widget.LinearLayout'
                                         '/android.view.View')
        if len(eles) >= 3:
            self.swipe_ele2(eles[2], eles[0])

    def search_slide(self, index):  # 查找幻灯片
        logging.info('==========search_slide==========')
        for i in range(10000):
            if not self.get_element_result('//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.view.View[@index="%s"]' % (int(index) - 1)):
                self.thumbnail_scroll()
            else:
                break
        self.driver.find_element(By.XPATH,
                                 '//android.widget.HorizontalScrollView/android.widget.LinearLayout/android.view.View[@index="%s"]' % (int(index) - 1)).click()

    def add_comment(self, index, comment):  #  Insert 备注
        logging.info('==========add_comment==========')
        time.sleep(2)
        self.search_slide(index)
        if not self.get_element_result('//*[@text=" Remarks "]'):
            self.group_button_click(' Insert ')
        self.driver.find_element(By.XPATH, '//*[@text=" Remarks "]').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_eidt_note_et').set_text(comment)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_eidt_note_ok').click()

    def check_comment(self, index):
        logging.info('==========add_new==========')
        self.search_slide(index)

        if self.get_element_result('//android.widget.Button'):
            self.driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()

    def delete_comment(self):  # 删除备注
        logging.info('==========edit_comment==========')
        self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_note_body_delete_note').click()

    def edit_comment(self, comment):  # 编辑备注
        logging.info('==========edit_comment==========')
        self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_note_body_edit_note').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_eidt_note_et').set_text(comment)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_eidt_note_ok').click()

    def play_mode(self, mode='autoplay'):  # 播放模式 current,first,autoplay
        logging.info('==========play_mode==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_option_id_play_%s' % mode).click()

    def insert_new_ppt(self):
        """
        菜单插入幻灯片
        :return:
        """
        logging.info('==========insert_new_ppt==========')
        if not self.get_element_result('//*[@text=" Slide "]'):
            self.group_button_click(' Insert ')
        self.driver.find_element(By.XPATH, '//*[@text=" Slide "]').click()

    def screenshot_edit_ppt(self, file_name):
        """
        截取当前编辑的ppt图片
        注：工具栏会被收缩
        :param file_name:
        :return:
        """
        logging.info('==========screenshot_current_editPpt==========')
        try:
            self.driver.find_element(By.CLASS_NAME, 'android.support.v4.view.ViewPager')
        except NoSuchElementException:
            pass
        else:
            self.driver.find_element(By.ID,
                                     'com.yozo.office.en:id/yozo_ui_option_expand_button').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/a0000_pg_slide_view_id').screenshot(file_name)

    def play_to_first(self, start_page):
        """
        非自动播放下，点击播放至首页
        :param start_page: 起始播放页，首页为1
        :return: None
        """
        x, y = self.get_size()
        while start_page > 0:
            time.sleep(1)
            self.tap(y * 0.25, x * 0.5)
            start_page -= 1

    def play_to_last(self, start_page, total_pages):
        """
        非自动播放下，点击播放至最后页
        :param start_page: 起始播放页，首页为1
        :param total_pages: ppt总页数
        :return: None
        """
        x, y = self.get_size()
        while total_pages-start_page > -1:
            time.sleep(1)
            self.tap(y * 0.75, x * 0.5)
            start_page += 1

    def quit_play(self):  # 退出播放
        logging.info('==========quit_paly==========')
        self.driver.keyevent(4)

    def pause_resume_play(self):  # 暂停、回复播放
        logging.info('==========pause_resume==========')
        self.tap(880, 540)

    def switch_mode(self, switch, apply='one'):  # 切换
        logging.info('==========switch_mode==========')
        ranges = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout'
        switch_ele = '//*[@text="%s"]' % switch
        self.swipe_search2(switch_ele, ranges)
        self.driver.find_element(By.XPATH, switch_ele).click()
        if not apply == 'one':
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_option_id_transition_apply_all').click()