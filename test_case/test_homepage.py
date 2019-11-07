#!/user/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time

from ddt import ddt, data
from selenium.webdriver.common.by import By
from common.myunit import StartEnd
from common.common_data import *
from businessView.generalView import GeneralView
from businessView.openView import OpenView
from businessView.createView import CreateView


@ddt
class TestHomePage(StartEnd):

    def create_new_file(self, save_path='local', file_path='None'):
        """
        生成新文档
        :param save_path: local or OneDrive
        :param file_path: detail path ,edg: 'Download>emaila'
        :return: file name
        """
        gv = GeneralView(self.driver)
        ov = OpenView(self.driver)
        cv = CreateView(self.driver)
        cv.create_file('wp')
        file_name = gv.getTime('%Y%m%d%H%M%S')
        cv.save_new_file(file_name, save_path, file_path)
        ov.close_file()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_add_back').click()
        return file_name + '.doc'

    logging.info('==========Recent==========')

    # @unittest.skip('skip test_show_open_file')
    def test_show_open_file(self):  # “最近”中显示已打开的文件
        logging.info('==========test_show_open_file==========')
        gv = GeneralView(self.driver)
        file_name = self.ov.open_random_file('doc')
        self.ov.close_file()
        time.sleep(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_search_back').click()
        gv.jump_to_index('last')
        file_ele = '//*[@text="%s"]' % file_name
        self.assertTrue(self.ov.get_element_result(file_ele))

    # @unittest.skip('skip test_last_scroll')
    def test_last_scroll(self):  # 测试“最近”中的滑屏
        logging.info('==========test_last_scroll==========')
        gv = GeneralView(self.driver)
        self.ov.open_several_files()
        gv.jump_to_index('last')
        first_name = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')[0].text
        gv.swipeUp()
        second_name = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')[0].text
        self.assertTrue(first_name != second_name)

    # @unittest.skip('skip test_last_file_info')
    def test_last_file_info(self):  # File Info显示
        logging.info('==========test_last_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_last_mark_star')
    def test_last_mark_star(self):  # 最近中的标星操作
        logging.info('==========test_last_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.file_more_info(1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_share_from_index')
    @data(*INDEX_SHARE_LIST)
    def test_last_share(self, way):  # “最近”中的分享
        logging.info('==========test_last_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_last_share_back')
    def test_last_share_back(self):  # “最近”中的分享的返回键
        logging.info('==========test_last_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_last_upload_file')
    def test_last_upload_file(self):  # “最近”上传文件
        logging.info('==========test_last_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        check = gv.upload_file()
        self.assertTrue(check, 'upload fail')

    # @unittest.skip('skip test_last_delete_file')
    def test_last_delete_file(self):  # “最近”删除文件
        logging.info('==========test_last_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        self.assertTrue(gv.delete_last_file())

    # @unittest.skip('skip test_last_select_all')
    def test_last_select_all(self):  # “最近”全选操作
        logging.info('==========test_last_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.file_more_info(1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_last_select_all1')
    def test_last_select_all1(self):  # “最近”全选操作
        logging.info('==========test_last_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.select_file_type('all')
        gv.sort_files('name', 'up')
        gv.file_more_info(1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.search_action(i))
            self.driver.keyevent(4)

    logging.info('==========Open-all/wp/pg/ss/pdf==========')
    
    # @unittest.skip('skip test_alldoc_show_file')
    def test_alldoc_show_file(self):  # 点击文件类型
        logging.info('==========test_alldoc_show_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        for i in TYPE_LIST:
            gv.select_file_type(i)
            self.assertTrue(gv.check_select_file_type(i), 'filter fail')
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_user').click()
            time.sleep(1)

    # @unittest.skip('skip test_alldoc_type_back')
    def test_alldoc_type_back(self):  # “打开”文档类型中的返回键
        logging.info('==========test_alldoc_type_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('pdf')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_user').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/fb_show_menu_main"]'))

    # @unittest.skip('skip test_alldoc_sort_file')
    def test_alldoc_sort_file(self):  # “打开”文档按条件排序
        logging.info('==========test_alldoc_sort_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        way_list = ['type', 'name', 'size', 'time']
        order_list = ['up', 'down']
        for i in way_list:
            for j in order_list:
                gv.sort_files(i, j)

    # @unittest.skip('skip test_alldoc_search_file')
    def test_alldoc_search_file(self):  # 搜索功能
        logging.info('==========test_alldoc_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        filename = self.create_new_file()
        result = gv.search_action(filename)
        self.assertTrue(result)

    # @unittest.skip('skip test_alldoc_file_info')
    def test_alldoc_file_info(self):  # File Info显示
        logging.info('==========test_alldoc_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        filename = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filename').text.strip()
        self.assertTrue(filename != '-')
        suffix = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetype').text.strip()
        self.assertTrue(suffix != '-')
        size = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filesize').text.strip()
        self.assertTrue(size != '-')
        chang_time = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetime').text.strip()
        self.assertTrue(chang_time != '-')
        path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text.strip()
        self.assertTrue(path != '-')

    # @unittest.skip('skip test_alldoc_mark_star')
    def test_alldoc_mark_star(self):
        logging.info('==========test_alldoc_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.file_more_info(1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_alldoc_share')
    @data(*INDEX_SHARE_LIST)
    def test_alldoc_share(self, way):
        logging.info('==========test_alldoc_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_alldoc_share_back')
    def test_alldoc_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_alldoc_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_alldoc_upload_file')
    def test_alldoc_upload_file(self):  # 上传文件
        logging.info('==========test_alldoc_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        check = gv.upload_file()
        self.assertTrue(check, 'upload fail')

    # @unittest.skip('skip test_alldoc_copy_file')
    def test_alldoc_copy_file(self):  # “打开”复制文件
        logging.info('==========test_alldoc_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_alldoc_move_file')
    def test_alldoc_move_file(self):  # “打开”移动文件
        logging.info('==========test_alldoc_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_alldoc_rename_file')
    def test_alldoc_rename_file(self):
        logging.info('==========test_alldoc_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_alldoc_delete_file')
    def test_alldoc_delete_file(self):
        logging.info('==========test_alldoc_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.sort_files('name', 'up')
        gv.file_more_info(1)
        suffix = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetype').text.strip()
        filename = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filename').text.strip()
        name = filename + '.' + suffix
        gv.delete_file()
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name), 'delete fail')

    # @unittest.skip('skip test_alldoc_scroll')
    def test_alldoc_scroll(self):  # 测试“最近”中的滑屏
        logging.info('==========test_alldoc_scroll==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        first_name = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')[0].text
        gv.swipeUp()
        second_name = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')[0].text
        self.assertTrue(first_name != second_name)

    # @unittest.skip('skip test_alldoc_select_all')
    def test_alldoc_select_all(self):  # “所有”全选操作
        logging.info('==========test_alldoc_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_alldoc_select_all1')
    def test_alldoc_select_all1(self):
        logging.info('==========test_alldoc_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.sort_files('name', 'up')
        gv.file_more_info(1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.search_action(i))
            self.driver.keyevent(4)

    # @unittest.skip('skip test_local_folder')
    @data(*FOLDER_LIST)
    def test_local_folder(self, folder):  # 测试本地文档打开
        logging.info('==========test_local_folder==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder(folder)
        self.assertTrue(gv.check_open_folder(folder), 'open fail')

    logging.info('==========Open-mobile==========')

    # @unittest.skip('skip test_mobile_copy_file')
    def test_mobile_copy_file(self):
        logging.info('==========test_mobile_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_mobile_delete_file')
    def test_mobile_delete_file(self):
        logging.info('==========test_mobile_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        self.driver.find_elements(By.ID, 'com.yozo.office.en:id/file_item')[0].click()
        gv.file_more_info(1)
        file_path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text
        index_e = file_path.rindex('/') + 1
        name = file_path[index_e:]
        gv.delete_file()
        # self.driver.keyevent(4)
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name))

    # @unittest.skip('skip test_mobile_file_info')
    def test_mobile_file_info(self):  # File Info显示
        logging.info('==========test_mobile_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file()
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_mobile_mark_star')
    def test_mobile_mark_star(self):
        logging.info('==========test_mobile_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_mobile_move_file')
    def test_mobile_move_file(self):  # “打开”移动文件
        logging.info('==========test_mobile_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_mobile_rename_file')
    def test_mobile_rename_file(self):
        logging.info('==========test_mobile_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file()
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_mobile_search_file')
    def test_mobile_search_file(self):  # 搜索功能
        logging.info('==========test_mobile_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        file_name = self.create_new_file()
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        result = gv.search_action(file_name)
        self.assertTrue(result)

    # @unittest.skip('skip test_mobile_select_all')
    def test_mobile_select_all(self):  # “最近”全选操作
        logging.info('==========test_mobile_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_mobile_select_all1')
    def test_mobile_select_all1(self):
        logging.info('==========test_mobile_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.get_element_result('//*[@text="%s"]' % i))

    # @unittest.skip('skip test_mobile_share')
    @data(*INDEX_SHARE_LIST)
    def test_mobile_share(self, way):
        logging.info('==========test_mobile_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_mobile_share_back')
    def test_mobile_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_mobile_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_mobile_sort_file')
    def test_mobile_sort_file(self):  # “打开”文档按条件排序
        logging.info('==========test_mobile_sort_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        way_list = ['type', 'name', 'size', 'time']
        order_list = ['up', 'down']
        for i in way_list:
            for j in order_list:
                gv.sort_files(i, j)

    # @unittest.skip('skip test_mobile_upload_file')
    def test_mobile_upload_file(self):  # 上传文件
        logging.info('==========test_mobile_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Mobile Phones')
        self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        if check is None:
            gv.jump_to_index('alldoc')
            gv.open_local_folder('Mobile Phones')
            self.assertTrue(gv.check_open_folder('Mobile Phones'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        self.assertTrue(check, 'upload fail')
        self.driver.keyevent(4)
        gv.jump_to_index('my')

    logging.info('==========Open-my file==========')

    # @unittest.skip('skip test_myfile_copy_file')
    def test_myfile_copy_file(self):
        logging.info('==========test_myfile_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_myfile_delete_file')
    def test_myfile_delete_file(self):
        logging.info('==========test_myfile_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file_path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text
        index_e = file_path.rindex('/') + 1
        name = file_path[index_e:]
        gv.delete_file()
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name))

    # @unittest.skip('skip test_myfile_file_info')
    def test_myfile_file_info(self):  # File Info显示
        logging.info('==========test_myfile_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_myfile_mark_star')
    def test_myfile_mark_star(self):
        logging.info('==========test_myfile_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_myfile_move_file')
    def test_myfile_move_file(self):  # “打开”移动文件
        logging.info('==========test_myfile_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_myfile_rename_file')
    def test_myfile_rename_file(self):
        logging.info('==========test_myfile_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_myfile_search_file')
    def test_myfile_search_file(self):  # 搜索功能
        logging.info('==========test_myfile_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        file_name = self.create_new_file()
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        result = gv.search_action(file_name)
        self.assertTrue(result)

    # @unittest.skip('skip test_myfile_select_all')
    def test_myfile_select_all(self):  # “最近”全选操作
        logging.info('==========test_myfile_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_myfile_select_all1')
    def test_myfile_select_all1(self):
        logging.info('==========test_myfile_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.get_element_result('//*[@text="%s"]' % i))

    # @unittest.skip('skip test_myfile_share')
    @data(*INDEX_SHARE_LIST)
    def test_myfile_share(self, way):
        logging.info('==========test_myfile_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_myfile_share_back')
    def test_myfile_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_myfile_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_myfile_sort_file')
    def test_myfile_sort_file(self):  # “打开”文档按条件排序
        logging.info('==========test_myfile_sort_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        way_list = ['type', 'name', 'size', 'time']
        order_list = ['up', 'down']
        for i in way_list:
            for j in order_list:
                gv.sort_files(i, j)

    # @unittest.skip('skip test_myfile_upload_file')
    def test_myfile_upload_file(self):  # 上传文件
        logging.info('==========test_myfile_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('My Documents')
        self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        if check is None:
            gv.jump_to_index('alldoc')
            gv.open_local_folder('My Documents')
            self.assertTrue(gv.check_open_folder('My Documents'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        self.assertTrue(check, 'upload fail')
        self.driver.keyevent(4)
        gv.jump_to_index('my')

    logging.info('==========Open-download==========')

    # @unittest.skip('skip test_Download_copy_file')
    def test_download_copy_file(self):
        logging.info('==========test_Download_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file()
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_Download_delete_file')
    def test_download_delete_file(self):
        logging.info('==========test_Download_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file_path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text
        index_e = file_path.rindex('/') + 1
        name = file_path[index_e:]
        gv.delete_file()
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name))

    # @unittest.skip('skip test_Download_file_info')
    def test_download_file_info(self):  # File Info显示
        logging.info('==========test_Download_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file()
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_Download_mark_star')
    def test_download_mark_star(self):
        logging.info('==========test_Download_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_Download_move_file')
    def test_download_move_file(self):  # “打开”移动文件
        logging.info('==========test_Download_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_Download_rename_file')
    def test_download_rename_file(self):
        logging.info('==========test_Download_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file()
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_Download_search_file')
    def test_download_search_file(self):  # 搜索功能
        logging.info('==========test_Download_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        file_name = self.create_new_file()
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        result = gv.search_action(file_name)
        self.assertTrue(result)

    # @unittest.skip('skip test_Download_select_all')
    def test_download_select_all(self):  # “最近”全选操作
        logging.info('==========test_Download_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_Download_select_all1')
    def test_download_select_all1(self):
        logging.info('==========test_Download_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.get_element_result('//*[@text="%s"]' % i))

    # @unittest.skip('skip test_Download_share')
    @data(*INDEX_SHARE_LIST)
    def test_download_share(self, way):
        logging.info('==========test_Download_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='Download')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_Download_share_back')
    def test_download_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_Download_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_Download_sort_file')
    def test_download_sort_file(self):  # “打开”文档按条件排序
        logging.info('==========test_Download_sort_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        way_list = ['type', 'name', 'size', 'time']
        order_list = ['up', 'down']
        for i in way_list:
            for j in order_list:
                gv.sort_files(i, j)

    # @unittest.skip('skip test_Download_upload_file')
    def test_download_upload_file(self):  # 上传文件
        logging.info('==========test_Download_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('Download')
        self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        if check is None:
            gv.jump_to_index('alldoc')
            gv.open_local_folder('Download')
            self.assertTrue(gv.check_open_folder('Download'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        self.assertTrue(check, 'upload fail')
        self.driver.keyevent(4)
        gv.jump_to_index('my')

    logging.info('==========Open-QQ==========')

    # @unittest.skip('skip test_QQ_copy_file')
    def test_qq_copy_file(self):
        logging.info('==========test_QQ_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>QQfile_recv')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_QQ_delete_file')
    def test_qq_delete_file(self):
        logging.info('==========test_QQ_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file_path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text
        index_e = file_path.rindex('/') + 1
        name = file_path[index_e:]
        gv.delete_file()
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name))

    # @unittest.skip('skip test_QQ_file_info')
    def test_qq_file_info(self):  # File Info显示
        logging.info('==========test_QQ_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>QQfile_recv')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_QQ_mark_star')
    def test_qq_mark_star(self):
        logging.info('==========test_QQ_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_QQ_move_file')
    def test_qq_move_file(self):  # “打开”移动文件
        logging.info('==========test_QQ_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>QQfile_recv')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_QQ_rename_file')
    def test_qq_rename_file(self):
        logging.info('==========test_QQ_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>QQfile_recv')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_QQ_search_file')
    def test_qq_search_file(self):  # 搜索功能
        logging.info('==========test_QQ_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        file_name = self.create_new_file(file_path='tencent>QQfile_recv')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        result = gv.search_action(file_name)
        self.assertTrue(result)

    # @unittest.skip('skip test_QQ_select_all')
    def test_qq_select_all(self):  # “最近”全选操作
        logging.info('==========test_QQ_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_QQ_select_all1')
    def test_qq_select_all1(self):
        logging.info('==========test_QQ_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.get_element_result('//*[@text="%s"]' % i))

    # @unittest.skip('skip test_QQ_share')
    @data(*INDEX_SHARE_LIST)
    def test_qq_share(self, way):
        logging.info('==========test_QQ_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_QQ_share_back')
    def test_qq_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_QQ_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_QQ_sort_file')
    def test_qq_sort_file(self):  # “打开”文档按条件排序
        logging.info('==========test_QQ_sort_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        way_list = ['type', 'name', 'size', 'time']
        order_list = ['up', 'down']
        for i in way_list:
            for j in order_list:
                gv.sort_files(i, j)

    # @unittest.skip('skip test_QQ_upload_file')
    def test_qq_upload_file(self):  # 上传文件
        logging.info('==========test_QQ_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder('QQ')
        self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        if check is None:
            gv.jump_to_index('alldoc')
            gv.open_local_folder('QQ')
            self.assertTrue(gv.check_open_folder('QQ'), 'open fail')
            gv.swipe_to_end()
            gv.file_more_info(-1)
            check = gv.upload_file()
        self.assertTrue(check, 'upload fail')
        self.driver.keyevent(4)
        gv.jump_to_index('my')

    logging.info('==========Open-Wechat==========')

    # @unittest.skip('skip test_wechat_copy_file')
    def test_wechat_copy_file(self):
        logging.info('==========test_wechat_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>MicroMsg>Download')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_wechat_delete_file')
    def test_wechat_delete_file(self):
        logging.info('==========test_wechat_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file_path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text
        index_e = file_path.rindex('/') + 1
        name = file_path[index_e:]
        gv.delete_file()
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name))

    # @unittest.skip('skip test_wechat_file_info')
    def test_wechat_file_info(self):  # File Info显示
        logging.info('==========test_wechat_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>MicroMsg>Download')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_wechat_mark_star')
    def test_wechat_mark_star(self):
        logging.info('==========test_wechat_mark_star==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        gv.swipe_to_end()
        gv.file_more_info(-1)
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_wechat_move_file')
    def test_wechat_move_file(self):  # “打开”移动文件
        logging.info('==========test_wechat_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_wechat_rename_file')
    def test_wechat_rename_file(self):
        logging.info('==========test_wechat_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>MicroMsg>Download')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_wechat_search_file')
    def test_wechat_search_file(self):  # 搜索功能
        logging.info('==========test_wechat_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        file_name = self.create_new_file(file_path='tencent>MicroMsg>Download')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        result = gv.search_action(file_name)
        self.assertTrue(result)

    # @unittest.skip('skip test_wechat_select_all')
    def test_wechat_select_all(self):  # “最近”全选操作
        logging.info('==========test_wechat_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_wechat_select_all1')
    def test_wechat_select_all1(self):
        logging.info('==========test_wechat_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.get_element_result('//*[@text="%s"]' % i))

    # @unittest.skip('skip test_wechat_share')
    @data(*INDEX_SHARE_LIST)
    def test_wechat_share(self, way):
        logging.info('==========test_wechat_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        self.create_new_file(file_path='tencent>MicroMsg>Download')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_wechat_share_back')
    def test_wechat_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_wechat_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))

    # @unittest.skip('skip test_wechat_sort_file')
    def test_wechat_sort_file(self):  # “打开”文档按条件排序
        logging.info('==========test_wechat_sort_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        way_list = ['type', 'name', 'size', 'time']
        order_list = ['up', 'down']
        for i in way_list:
            for j in order_list:
                gv.sort_files(i, j)

    # @unittest.skip('skip test_wechat_upload_file')
    def test_wechat_upload_file(self):  # 上传文件
        logging.info('==========test_wechat_upload_file==========')
        gv = GeneralView(self.driver)
        l = LoginView(self.driver)
        gv.jump_to_index('alldoc')
        gv.open_local_folder("Wechat")
        self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
        gv.swipe_to_end()
        gv.file_more_info(-1)
        check = gv.upload_file()
        if check is None:
            gv.jump_to_index('alldoc')
            gv.open_local_folder("Wechat")
            self.assertTrue(gv.check_open_folder("Wechat"), 'open fail')
            gv.swipe_to_end()
            gv.file_more_info(-1)
            check = gv.upload_file()
        self.assertTrue(check, 'upload fail')
        self.driver.keyevent(4)
        gv.jump_to_index('my')
        l.logout_action()

    logging.info('==========Favourite==========')

    # @unittest.skip('skip test_star_show_no_file')
    def test_star_show_no_file(self):
        logging.info('==========test_star_show_no_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('star')
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/iv_view"]'))

    # @unittest.skip('skip test_star_copy_file')
    def test_star_copy_file(self):  # “打开”复制文件
        logging.info('==========test_star_copy_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        gv.mark_star()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_user').click()
        gv.jump_to_index('star')
        gv.file_more_info(1)
        check = gv.copy_file()
        self.assertTrue(check, 'copy fail')

    # @unittest.skip('skip test_star_delete_file')
    def test_star_delete_file(self):
        logging.info('==========test_star_delete_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.sort_files('name', 'up')
        gv.file_more_info(2)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        self.driver.keyevent(4)
        gv.jump_to_index('star')
        gv.file_more_info(2)
        suffix = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetype').text.strip()
        filename = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filename').text.strip()
        name = filename + '.' + suffix
        gv.delete_file()
        self.assertFalse(gv.get_element_result('//*[@text="%s"]' % name), 'delete fail')

    # @unittest.skip('skip test_star_file_info')
    def test_star_file_info(self):  # File Info显示
        logging.info('==========test_star_file_info==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        self.driver.keyevent(4)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        filename = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filename').text.strip()
        self.assertTrue(filename != '-')
        suffix = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetype').text.strip()
        self.assertTrue(suffix != '-')
        size = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filesize').text.strip()
        self.assertTrue(size != '-')
        chang_time = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetime').text.strip()
        self.assertTrue(chang_time != '-')
        path = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_fileloc').text.strip()
        self.assertTrue(path != '-')
        file = gv.mark_star()
        self.assertFalse(gv.check_mark_satr(file))

    # @unittest.skip('skip test_star_move_file')
    def test_star_move_file(self):  # “打开”移动文件
        logging.info('==========test_star_move_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(3)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        self.driver.keyevent(4)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        check = gv.move_file()
        self.assertTrue(check, 'move fail')

    # @unittest.skip('skip test_star_rename_file')
    def test_star_rename_file(self):
        logging.info('==========test_star_rename_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        gv.file_more_info(1)
        file = gv.mark_star()
        self.assertTrue(gv.check_mark_satr(file))
        self.driver.keyevent(4)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        newName = 'rename' + gv.getTime('%Y%m%d%H%M%S')
        check = gv.rename_file(newName)
        self.assertTrue(check, 'rename fail')

    # @unittest.skip('skip test_star_search_file')
    def test_star_search_file(self):  # 搜索功能
        logging.info('==========test_star_search_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('star')
        file_name = self.create_new_file()
        result = gv.search_action(file_name)
        self.assertTrue(result)

    # @unittest.skip('skip test_star_select_all')
    def test_star_select_all(self):  # “最近”全选操作
        logging.info('==========test_star_select_all==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.select_file_type('all')
        eles = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/file_item')
        i = 1
        while i <= len(eles):
            gv.file_more_info(i)
            file = gv.mark_star()
            self.assertTrue(gv.check_mark_satr(file))
            i += 1
        self.driver.keyevent(4)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        self.assertTrue(gv.get_element_result('//*[@text="Deselect All"]'))
        num = int(self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_num').text)
        self.assertTrue(num != 0)
        self.driver.find_element(By.XPATH, '//*[@text="Cancel"]').click()
        self.assertTrue(gv.get_element_result('//*[@resource-id="com.yozo.office.en:id/lay_more"]'))

    # @unittest.skip('skip test_star_select_all1')
    def test_star_select_all1(self):
        logging.info('==========test_star_select_all1==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('alldoc')
        gv.jump_to_index('star')
        gv.file_more_info(1)
        name_list = gv.select_all('multi')
        for i in name_list:
            self.assertFalse(gv.search_action(i))
            self.driver.keyevent(4)

    # @unittest.skip('skip test_star_share')
    @data(*INDEX_SHARE_LIST)
    def test_star_share(self, way):
        logging.info('==========test_star_share==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        gv.share_file_index(way)

    # @unittest.skip('skip test_star_share_back')
    def test_star_share_back(self):  # “打开”中的分享的返回键
        logging.info('==========test_star_share_back==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_more_share').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="File Info"]'))
    
    # @unittest.skip('skip test_star_upload_file')
    def test_star_upload_file(self):  # 上传文件
        logging.info('==========test_star_upload_file==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('star')
        gv.file_more_info(1)
        check = gv.upload_file()
        if check is None:
            gv.jump_to_index('alldoc')
            gv.select_file_type('all')
            gv.file_more_info(1)
            gv.mark_star()
            self.driver.keyevent(4)
            gv.jump_to_index('star')
            gv.file_more_info(1)
            check = gv.upload_file()
        self.assertTrue(check, 'upload fail')
        self.driver.keyevent(4)
        gv.jump_to_index('my')

    logging.info('==========Me==========')
    
    # @unittest.skip('skip test_my1_about_yozo')
    def test_me_about_yozo(self):
        logging.info('==========test_my1_about_yozo==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('my')
        self.driver.find_element(By.XPATH, '//*[@text="About Yozo"]').click()
        version_no = self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_version').text
        self.assertTrue(version_no != '-')
        web_addr = self.driver.find_element(By.ID, 'com.yozo.office.en:id/_phone_web').text
        self.assertTrue(web_addr == 'www.yozosoft.com')
        mail_addr = self.driver.find_element(By.ID, 'com.yozo.office.en:id/_phone_email').text
        self.assertTrue(mail_addr == 'mobile@yozosoft.com')
        phone = self.driver.find_element(By.ID, 'com.yozo.office.en:id/_phone_phone').text
        self.assertTrue(phone == '400-050-5206')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_back').click()
        self.assertTrue(gv.get_element_result('//*[@text="About Yozo"]'))
    
    # @unittest.skip('skip test_rotate_index')
    def test_rotate_index(self):
        logging.info('==========test_rotate_index==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        gv.screen_rotate('landscape')
        gv.screen_rotate('portrait')
        gv.jump_to_index('alldoc')
        gv.screen_rotate('landscape')
        gv.screen_rotate('portrait')
        gv.jump_to_index('star')
        gv.screen_rotate('landscape')
        gv.screen_rotate('portrait')
        gv.jump_to_index('my')
        gv.screen_rotate('landscape')
        gv.screen_rotate('portrait')
    
    # @unittest.skip('skip test_search_icon_show')
    def test_search_icon_show(self):  # 搜索键显示
        logging.info('==========test_search_icon_show==========')
        gv = GeneralView(self.driver)
        gv.jump_to_index('last')
        ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search')
        self.assertTrue(ele != None)
        gv.jump_to_index('alldoc')
        ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search')
        self.assertTrue(ele != None)
        gv.jump_to_index('star')
        ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search')
        self.assertTrue(ele != None)
