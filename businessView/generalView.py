#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from businessView.loginView import LoginView
from common.common_func import Common
from common.tool import get_project_path


class GeneralView(Common):

    def insert_pic(self):  # 插入图片，基于vivoX9手机,选取图片只能点选坐标
        logging.info('=========insert_pic==========')
        self.driver.find_element(By.XPATH, '//*[@text="图片"]').click()
        self.driver.find_element(By.XPATH, '//android.widget.ListView/android.widget.RelativeLayout[1]').click()
        self.tap(145, 369)
        self.driver.find_element(By.XPATH, '//*[@text="确定"]').click()

    def sort_files(self, way='type', order='down'):  # 排序
        logging.info('=========sort_files==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_shot').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/rl_sort_%s' % way).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_sort_%s' % order).click()
        time.sleep(1)

    def identify_file_index(self):  # 识别云文档中首个文件，递归有问题
        logging.info('=========identify_file_index==========')
        eles = self.driver.find_elements(By.XPATH, '//android.support.v7.widget.RecyclerView'
                                                   '/android.widget.RelativeLayout')
        suffix_list = ['docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'pdf']
        index = 0
        for i, e in enumerate(eles):  # 尚有缺陷，将将用
            name = e.find_element(By.ID, 'com.yozo.office.en:id/tv_title').text
            if '.' in name:
                suffix = name[name.rindex('.') + 1:]
                if suffix in suffix_list:
                    index = i
                    break
        if index == 0:
            self.swipe_ele1(eles[-1], eles[0])
            time.sleep(1)
            self.identify_file_index()
        else:
            return index

    def download_file(self):  # 下载文件
        logging.info('=========download_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="下载"]').click()
        time.sleep(2)
        return self.get_toast_message('文件下载成功')

    def select_all(self, select='all', del_list=[]):  # 全选、多选
        logging.info('=========select_all==========')
        self.driver.find_element(By.XPATH, '//*[@text="Select All"]').click()
        name_list = []
        if select == 'all':
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_file_checked_tab_all').click()
        else:
            eles = self.driver.find_elements(By.XPATH, '//android.support.v7.widget.RecyclerView'
                                                       '/android.widget.RelativeLayout')
            for i in del_list:
                name = eles[i - 1].find_element(By.ID, 'com.yozo.office.en:id/tv_title').text
                name_list.append(name)
                eles[i - 1].click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_check_bottom_del').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_true').click()
        return name_list

    def delete_last_file(self):  # "最近"删除文件
        logging.info('=========delete_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="Delete"]').click()
        return self.get_toast_message('This action simply removes the file from the recent list')

    def delete_file(self):  # 删除文件
        logging.info('=========delete_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="Delete"]').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_true').click()

    def rename_file(self, newName):  # 重命名文件
        logging.info('=========rename_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="Rename"]').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/et_newfoldername').set_text(newName)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_true').click()
        return self.get_toast_message('Operation success')

    def move_file(self):  # 移动文件
        logging.info('=========move_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="Move"]').click()
        self.driver.find_elements(By.ID, 'com.yozo.office.en:id/file_item')[0].click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_move_true').click()
        return self.get_toast_message('Success to move')

    def copy_file(self):  # 复制文件
        logging.info('=========copy_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="Copy"]').click()
        time.sleep(1)
        self.driver.find_elements(By.ID, 'com.yozo.office.en:id/file_item')[0].click()
        self.driver.find_elements(By.ID, 'com.yozo.office.en:id/file_item')[1].click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_move_true').click()
        return self.get_toast_message('Operation success')

    def upload_file(self):  # 上传文件
        logging.info('=========upload_file==========')
        self.driver.find_element(By.XPATH, '//*[@text="Upload"]').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_upload_onedrive').click()
        time.sleep(1)
        self.driver.find_element(By.ID, 'com.microsoft.skydrive:id/menu_action').click()
        return self.get_toast_message('Request completed successfully')

    def share_file_index(self, way):  # 主页分享
        logging.info('=========file_more_info==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_%s_share' % way).click()
        if way == 'more':
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@text="OneDrive"]').click()

    def check_mark_satr(self, file):
        logging.info('=========check_mark_satr==========')
        # ele = '//*[@text="%s"]/following-sibling::android.widget.ImageView' % file
        ele = '//*[@text="%s"]/../android.widget.ImageView' % file
        # ele = '//*[@text="%s"]/parent::android.widget.LinearLayout/android.widget.ImageView' % file
        return self.get_element_result(ele)

    def mark_star(self):
        logging.info('=========file_more_info==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_filework_pop_star').click()
        file_name = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filename').text
        file_type = self.driver.find_element(By.ID, 'com.yozo.office.en:id/tv_filetype').text
        file = file_name + '.' + file_type
        self.driver.keyevent(4)
        return file

    def file_more_info(self, index):  # 查看指定文件信息
        logging.info('=========file_more_info==========')
        ele = self.driver.find_element(By.CLASS_NAME, 'android.support.v7.widget.RecyclerView')
        eles = ele.find_elements(By.ID, 'com.yozo.office.en:id/file_item')
        if index < 1:
            eles[0].find_element(By.ID, 'com.yozo.office.en:id/lay_more').click()
        elif index > len(eles):
            eles[-1].find_element(By.ID, 'com.yozo.office.en:id/lay_more').click()
        else:
            eles[index - 1].find_element(By.ID, 'com.yozo.office.en:id/lay_more').click()

    def check_select_file_type(self, type):
        logging.info('==========check_select_file_type==========')
        suffix_dict = {'all': ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf'], 'wp': ['doc', 'docx'],
                       'ss': ['xls', 'xlsx'], 'pg': ['ppt', 'pptx'], 'pdf': ['pdf']}
        eles = self.driver.find_elements(By.ID, 'com.yozo.office.en:id/tv_title')
        eles_str = list(map(lambda x: x.text, eles))
        eles_suffix = list(set(map(lambda x: x[x.rindex('.') + 1:].lower(), eles_str)))
        print(eles_suffix)
        if [False for i in eles_suffix if i not in suffix_dict[type]]:
            return False
        else:
            return True

    def select_file_type(self, type):  # 文档类型
        logging.info('==========select_file_type==========')
        logging.info('select %s files', type)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_filetype_%s' % type).click()
        time.sleep(3)

    def open_local_folder(self, folder):  # 打开本地文档
        logging.info('==========open_local_folder==========')
        self.driver.find_element(By.XPATH, '//*[@text="%s"]' % folder).click()

    def check_open_folder(self, folder):
        logging.info('==========check_open_folder==========')
        folder_dict = {'手机': '浏览目录 > 手机', '我的文档': ' > Documents', 'Download': ' > Download',
                       'QQ': ' > QQfile_recv', '微信': ' > Download'}
        path = self.driver.find_elements(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/name_layout"]'
                                                   '/android.widget.TextView')[-1].text
        if path == folder_dict[folder]:
            return True
        else:
            return False

    def search_action(self, keyword):
        logging.info('==========search_action==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/im_title_bar_menu_search').click()
        logging.info('input keyword %s' % keyword)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/et_search').send_keys(keyword)
        logging.info('searching...')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_search_search').click()
        time.sleep(3)
        return self.get_element_result('//android.widget.TextView[@text="%s"]' % keyword)

    def check_search_action(self, keyword):
        logging.info('==========check_search_action==========')
        name = keyword[:keyword.rindex('.') + 1]
        suffix = keyword[keyword.rindex('.') + 1:]
        key = name + suffix
        return self.get_element_result('//android.widget.TextView[@text="%s"]' % key)

    def jump_to_index(self, type='last'):  # 5个主页界面
        """
        index = ['last', 'alldoc', 'cloud', 'star', 'my']  # office的五个页面组件尾缀
        :param type:
        :return:
        """
        logging.info('===========jump_to_%s==========' % type)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_bottommenu_%s' % type).click()

    def pop_menu_click(self, option):  # 点击pop
        logging.info('==========pop_menu_click==========')
        time.sleep(1)
        x, y = self.find_pic_position(option)
        self.tap(x, y)

    def find_pic_position(self, option):  # 查找图片的中心坐标
        logging.info('==========find_pic_position==========')
        self.getScreenShot4Compare('source')
        src_path = get_project_path() + '\\screenshots\\source.png'  # （当前页面）
        obj_path = get_project_path() + '\\clickPicture_CN\\%s.png' % option  # （需要点击的地方）
        # obj_path = get_project_path() + '\\clickPicture_EN\\%s.png' % option  # （需要点击的地方）
        x, y = self.find_image_cv(obj_path, src_path)
        return x, y
        # self.tap(x,y)

    def change_row_column(self):  # 切换行列
        logging.info('==========change_row_column==========')
        ele1 = '//*[@text="图表类型"]'
        ele2 = '//*[@text="图表元素"]'
        self.swipe_ele(ele2, ele1)
        self.driver.find_element(By.XPATH, '//*[@text="切换行列"]').click()

    def chart_element_XY(self, xy='x', title='', label=1, grid=0, sub_grid=0, axis=1, line=0, sub_line=0):
        logging.info('==========chart_element_XY==========')
        self.driver.find_element(By.XPATH, '//*[@text="%s轴"]' % str.upper(xy)).click()
        title_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_axis_title_check"]' \
                       '/android.widget.Switch'
        if title != '':
            if self.get_element(title_switch).text != '开启':
                self.find_element(By.XPATH, title_switch).click()
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_axis_title').click()
            time.sleep(1)
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_title').set_text(title)
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_full_screen_base_dialog_id_ok').click()
            self.fold_expand()

        if label != 1:
            label_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_label"]' \
                           '/android.widget.Switch' % (xy)
            if self.get_element(label_switch).text == '开启':
                self.driver.find_element(By.ID,
                                         'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_label'
                                         % (xy)).click()

        if grid != 0:
            grid_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_grid"]' \
                          '/android.widget.Switch' % (xy)
            if self.get_element(grid_switch).text == '关闭':
                self.driver.find_element(By.ID,
                                         'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_grid'
                                         % (xy)).click()

        sub_grid_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_subgrid"]' \
                          '/android.widget.Switch' % (xy)
        if sub_grid != 0:
            if self.get_element(sub_grid_switch).text == '关闭':
                self.driver.find_element(By.ID,
                                         'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_subgrid'
                                         % (xy)).click()
        self.swipe_ele(sub_grid_switch, title_switch)
        time.sleep(1)
        if axis != 0:
            line_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_line"]' \
                          '/android.widget.Switch' % (xy)
            if self.get_element(line_switch).text == '关闭':
                self.driver.find_element(By.ID,
                                         'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_line' % (
                                             xy)).click()
            if line != 0:
                line_checked = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_majortick"]' \
                               '/android.widget.CheckBox' % (xy)
                if self.get_element(line_checked).get_attribute('checked') == 'false':
                    self.driver.find_element(By.ID,
                                             'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_majortick' % (
                                                 xy)).click()
            if sub_line != 0:
                sub_line_checked = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_minortick"]' \
                                   '/android.widget.CheckBox' % (xy)
                if self.get_element(sub_line_checked).get_attribute('checked') == 'false':
                    self.driver.find_element(By.ID,
                                             'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_%saxis_minortick'
                                             % (xy)).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def chart_element(self, types, title='', index=1, display=0, label=0):  # 图表元素
        logging.info('==========chart_element==========')
        self.driver.find_element(By.XPATH, '//*[@text="图表元素"]').click()
        if title != '':
            title_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_title_check"]' \
                           '/android.widget.Switch' % types
            if self.get_element(title_switch).text != '开启':
                self.find_element(By.XPATH, title_switch).click()
            locate_ele = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_title_location_list"]' \
                         '/android.widget.FrameLayout[%s]' % (types, index)
            self.find_element(By.XPATH, locate_ele).click()
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_title' % types).click()
            time.sleep(1)
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_ss_option_id_chart_elem_title').set_text(title)
            self.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_full_screen_base_dialog_id_ok').click()
            self.fold_expand()

        if display != 0:
            display_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_legend_check"]' \
                             '/android.widget.Switch' % types
            if self.get_element(display_switch).text != '开启':
                self.find_element(By.ID,
                                  'com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_legend_check' % types).click()
            # align_list = {'底部': '1', '顶部': '2', '靠左': '3', '靠右': '4', '右上角': '5'}
            self.find_element(By.XPATH,
                              '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_legend_list"]'
                              '/android.widget.FrameLayout[%s]' % (types, display)).click()
        ele1 = '//*[@text="显示图表标题"]'
        ele2 = '//*[@text="显示图例"]'
        self.swipe_ele(ele2, ele1)
        if label != 0:
            label_switch = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_label_check"]' \
                           '/android.widget.Switch' % types
            if self.get_element(label_switch).text != '开启':
                self.find_element(By.ID,
                                  'com.yozo.office.en:id/yozo_ui_%s_option_id_chart_elem_label_check' % types).click()

    def chart_color(self, index):  # 图表颜色
        logging.info('==========chart_color==========')
        ele1 = '//*[@text="数据源"]'
        ele2 = '//*[@text="图表类型"]'
        self.swipe_ele(ele2, ele1)
        self.driver.find_element(By.XPATH, '//*[@text="更改颜色"]').click()
        eles_name = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout'
        eles = self.driver.find_elements(By.XPATH, eles_name)
        if index > len(eles):
            eles[-1].click()
        else:
            eles[index - 1].click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def chart_template(self):  # 图表样式
        logging.info('==========chart_template==========')
        self.driver.find_element(By.XPATH, '//*[@text="图表样式"]').click()
        eles_name = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout'
        time.sleep(1)
        eles = self.driver.find_elements(By.XPATH, eles_name)
        target_ele = eles_name + '[%s]' % random.randint(1, len(eles))
        self.driver.find_element(By.XPATH, target_ele).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def insert_chart_chart(self, chart, index):  # 插入图表，从图表选项进入
        logging.info('==========insert_chart_chart==========')
        self.driver.find_element(By.XPATH, '//*[@text="图表类型"]').click()
        self.insert_chart(chart, index)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def insert_chart_insert(self, chart, index=1):  # 插入图表,从插入选项进入
        logging.info('==========insert_chart_insert==========')
        self.driver.find_element(By.XPATH, '//*[@text="图表"]').click()
        self.insert_chart(chart, index)

    def insert_chart(self, chart, index):  # 插入图表,从图表选项进入
        logging.info('==========insert_chart==========')
        chart_list = ['柱形图', '条形图', '折线图', '饼图', '散点图', '面积图', '圆环图', '雷达图', '气泡图', '圆柱图',
                      '圆锥图', '棱锥图']
        ranges = '//android.support.v4.view.ViewPager/android.widget.ScrollView/android.widget.LinearLayout' \
                 '/android.widget.RelativeLayout'
        target = '//*[@text="%s"]' % chart
        self.swipe_search2(target, ranges)
        self.driver.find_element(By.XPATH, target).click()
        ele_name = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout'
        eles = self.driver.find_elements(By.XPATH, ele_name)
        if index > len(eles):
            eles[-1].click()
        else:
            eles[index - 1].click()

    def shape_content_align(self, type, horizontal='左对齐', vertical='上对齐'):
        logging.info('==========cell_align: %s_%s==========' % (horizontal, vertical))
        align_dict = {'左对齐': '1', '水平居中': '2', '右对齐': '3', '上对齐': '4', '垂直居中': '5', '下对齐': '6'}
        style_index1 = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_text_align"]' \
                       '/android.widget.FrameLayout[%s]' % (type, align_dict[horizontal])
        style_index2 = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_text_align"]' \
                       '/android.widget.FrameLayout[%s]' % (type, align_dict[vertical])
        self.driver.find_element(By.XPATH, style_index1).click()
        self.driver.find_element(By.XPATH, style_index2).click()

    def shape_insert(self, type, index=0, s_index=0):  # 插入自选图形
        logging.info('======shape_insert======')
        self.driver.find_element(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_insert"]'
                                           '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index >= 6:
            eleA = '//*[@text="最近使用"]'
            eleB = '//*[@text="基本形状"]'
            if self.get_element_result(eleA):
                self.swipe_ele(eleB, eleA)
            eles = self.driver.find_elements(By.XPATH,
                                             '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_more_shape'
                                             '_main_container"]/android.widget.FrameLayout')
            if len(eles) < s_index:
                time.sleep(0.5)
                self.swipe_ele1(eles[-1], eles[0])
                time.sleep(0.5)
                eles = self.driver.find_elements(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_more'
                                                           '_shape_main_container"]/android.widget.FrameLayout')
                eles[s_index - 19].click()
            else:
                eles[s_index - 1].click()
            time.sleep(1)
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def text_wrap(self, wrap='浮于文字上方'):  # 文字环绕
        logging.info('======text_wrap======')
        wrap_list = ['浮于文字上方', '衬于文字下方', '嵌入型', '四周型', '紧密型']
        self.driver.find_element(By.XPATH, '//*[@text="文字环绕"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="%s"]' % wrap).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def shape_layer(self, lay='置于顶层'):  # 图形叠放次序
        logging.info('======shape_layer======')
        lay_dict = {'上移一层': '1', '置于顶层': '2', '下移一层': '3', '置于底层': '4'}
        self.driver.find_element(By.XPATH, '//*[@text="叠放次序"]').click()
        self.driver.find_element(By.XPATH, '//*[@text="%s"]' % lay).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def pic_effect_type(self, type, index=1, shadow=8):
        logging.info('======pic_effect_type======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_picture_effect"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index >= 6:
            self.driver.find_element(By.XPATH,
                                     '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_object_effect_shadow"]'
                                     '/android.widget.FrameLayout[%s]' % shadow).click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def shape_effect_type(self, type, index=1, shadow=8, three_d=8):  # 边框效果
        logging.info('======shape_effect_type======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_effect_type"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index >= 6:
            self.driver.find_element(By.XPATH,
                                     '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_object_effect_shadow"]'
                                     '/android.widget.FrameLayout[%s]' % shadow).click()
            if self.get_element_result('//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_object_effect_3d"]'):
                self.driver.find_element(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_object_effect_3d"]'
                                         '/android.widget.FrameLayout[%s]' % three_d).click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def pic_border_width(self, type, index=1, size=1):  # 边框粗细size=1-30
        logging.info('======pic_border_width======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_picture_border_width"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index >= 6:
            for i in range(60):
                font_ele = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_number_picker_recycler_view"]' \
                           '/android.widget.TextView[@index="1"]'
                font = int((self.get_element(font_ele).text)[:-2])
                if size != font:
                    if size < font:
                        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_left').click()
                    else:
                        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_right').click()
                else:
                    self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()
                    break

    def shape_border_width(self, type, index=1, size=1):  # 边框粗细size=1-30
        logging.info('======shape_border_width======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_border_width"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index >= 6:
            for i in range(60):
                font_ele = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_number_picker_recycler_view"]' \
                           '/android.widget.TextView[@index="1"]'
                font = int((self.get_element(font_ele).text)[:-2])
                if size != font:
                    if size < font:
                        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_left').click()
                    else:
                        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_right').click()
                else:
                    self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()
                    break

    def pic_border_type(self, type, index=1, s_index=1):  # 边框格式
        logging.info('======pic_border_type======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_picture_border_type"]'
                                 '/android.widget.FrameLayout[%s]' % (
                                     type, index)).click()
        if index >= 6:
            eles = self.driver.find_elements(By.XPATH,
                                             '//*[@resource-id="com.yozo.office.en:id/yozo_ui_shape_border_type"]'
                                             '/android.widget.FrameLayout')
            eles[s_index - 1].click()

    def shape_border_type(self, type, index=1, s_index=1):  # 边框格式
        logging.info('======shape_boeder_type======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_border_type"]'
                                 '/android.widget.FrameLayout[%s]' % (
                                     type, index)).click()
        if index >= 6:
            eles = self.driver.find_elements(By.XPATH,
                                             '//*[@resource-id="com.yozo.office.en:id/yozo_ui_shape_border_type"]'
                                             '/android.widget.FrameLayout')
            eles[s_index - 1].click()
            time.sleep(0.5)
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def pic_border_color(self, type, index=1, s_index=0):  # 边框颜色
        logging.info('======shape_border_color======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_picture_broad"]'
                                 '/android.widget.FrameLayout[%s]' % (
                                     type, index)).click()
        if index >= 6:
            eles = self.driver.find_elements(By.XPATH,
                                             '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_color_all"]'
                                             '/android.widget.FrameLayout')
            eles[s_index - 1].click()
            time.sleep(0.5)
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def shape_border_color(self, type, index=1, s_index=0):  # 边框颜色
        logging.info('======shape_border_color======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_border_color"]'
                                 '/android.widget.FrameLayout[%s]' % (
                                     type, index)).click()
        if index >= 6:
            eles = self.driver.find_elements(By.XPATH,
                                             '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_color_all"]'
                                             '/android.widget.FrameLayout')
            eles[s_index - 1].click()
            time.sleep(0.5)
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def shape_fill_color_transparency(self, transparency=0):  # 0-100
        logging.info('======shape_fill_color_transparency======')
        eles = self.driver.find_elements(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_color_all"]'
                                         '/android.widget.FrameLayout')
        self.swipe_ele1(eles[-1], eles[0])
        seekbar = self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_group_seekbar').rect
        x, y, width, height = int(seekbar['x']), int(seekbar['y']), int(seekbar['width']), int(seekbar['height'])
        for i in range(x, x + width, 5):
            display = self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_group_seekbar_display').text
            display_num = int(display[:-1])
            if transparency == display_num:
                break
            else:
                self.tap(i, y)
                time.sleep(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def shape_fill_color(self, type, index, s_index=36):
        logging.info('======shape_fill_color======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_fill_color"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index == 6:
            eles = self.driver.find_elements(By.XPATH,
                                             '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_color_all"]'
                                             '/android.widget.FrameLayout')
            if len(eles) < 42 and len(eles) > 0:
                self.swipe_ele1(eles[0], eles[-1])
            eles[s_index - 1].click()
            time.sleep(0.5)
            # self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def pic_option(self, type, index, width=3.81, height=3.81, position='drag_pic3', x=0, y=0):  # 图片旋转等操作
        logging.info('======pic_option======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_picture_edit"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index == 5:
            width_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/shape_width')
            width_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(width))
            height_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/shape_height')
            height_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(height))
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_full_screen_base_dialog_id_ok').click()
            self.fold_expand()
        if index == 6:
            x1, y1 = self.find_pic_position(position)
            self.drag_coordinate(x1, y1, x1 + x, y1 + y)

    def shape_option(self, type, index, width=3.81, height=3.81, top=0.13, bottom=0.13, left=0.25,
                     right=0.25):  # 旋转、镜像、剪切
        logging.info('======shape_option======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_shape_quick_function"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index == 5:
            width_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/shape_width')
            width_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(width))
            height_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/shape_height')
            height_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(height))
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_full_screen_base_dialog_id_ok').click()
            self.fold_expand()
        if index == 6:
            top_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/margin_top')
            top_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(top))
            bottom_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/margin_bottom')
            bottom_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(bottom))
            left_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/margin_left')
            left_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(left))
            eleA = '//*[@text="左边距(单位:厘米)"]'
            eleB = '//*[@text="上边距(单位:厘米)"]'
            self.swipe_ele(eleA, eleB)
            right_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/margin_right')
            right_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(right))
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_full_screen_base_dialog_id_ok').click()
            self.fold_expand()

    def shape_option_5(self, width=5, height=5):
        width_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/shape_width')
        width_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(width))
        height_ele = self.driver.find_element(By.ID, 'com.yozo.office.en:id/shape_height')
        height_ele.find_element(By.ID, 'com.yozo.office.en:id/margin_value').set_text(str(height))
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_full_screen_base_dialog_id_ok').click()

    def pen_size(self, type, index):  # 签批字粗细 1-6
        logging.info('======pen_size======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_sign_pen_size"]'
                                 '/android.widget.FrameLayout[%s]' % (type, index)).click()

    def pen_color(self, type, index=41):  # 签批颜色 1-42
        logging.info('======pen_color======')
        self.driver.find_element(By.XPATH,
                                 '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_sign_pen_color"]'
                                 '/android.widget.FrameLayout[6]' % type).click()
        self.driver.find_element(By.XPATH, '//android.support.v7.widget.RecyclerView'
                                           '/android.widget.FrameLayout[%s]' % index).click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def pen_type(self, type, pen='钢笔'):  # 钢笔、荧光笔、擦除
        logging.info('======pen_type======')
        pen_list = ['钢笔', '荧光笔', '擦除']
        index = pen_list.index(pen) + 1
        self.driver.find_element(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_sign_pen_type"]'
                                           '/android.widget.FrameLayout[%s]' % (type, index)).click()

    def use_finger(self, type):  # 是否使用手指
        logging.info('======use_finger======')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_%s_option_id_sign_use_finger' % type).click()

    def insert_shape(self, type, index=1, s_index=0):  # 通用插入
        logging.info('======insert_shape======')
        self.driver.find_element(By.XPATH, '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_insert_shape"]'
                                           '/android.widget.FrameLayout[%s]' % (type, index)).click()
        if index >= 6:
            eleA = '//*[@text="最近使用"]'
            eleB = '//*[@text="基本形状"]'
            if self.get_element_result(eleA):
                self.swipe_ele(eleB, eleA)

            ele_id = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_option_id_more_shape_main_container"]' \
                     '/android.widget.FrameLayout'
            eles = self.driver.find_elements(By.XPATH, ele_id)
            if len(eles) < s_index:
                time.sleep(0.5)
                self.swipe_ele1(eles[-1], eles[0])
                time.sleep(0.5)
                eles = self.driver.find_elements(By.XPATH, ele_id)
                eles[s_index - 19].click()
            else:
                eles[s_index - 1].click()

    def text_indent(self, type, indent='左缩进'):  # 缩进
        logging.info('==========text_indent==========')
        if type == 'pg':
            if indent == '左缩进':
                self.driver.find_element(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_pg_option_id_edit_para_indent"]'
                                         '/android.widget.FrameLayout[1]').click()
            else:
                self.driver.find_element(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_pg_option_id_edit_para_indent"]'
                                         '/android.widget.FrameLayout[2]').click()
        else:
            if indent == '左缩进':
                self.driver.find_element(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_para_indent"]'
                                         '/android.widget.FrameLayout[1]' % type).click()
            else:
                self.driver.find_element(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_para_indent"]'
                                         '/android.widget.FrameLayout[2]' % type).click()

    def text_line_space(self, type, space):  # 行距
        logging.info('==========text_line_space==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_%s_option_id_para_line_space' % type).click()
        space_dict = {1: 'single', 1.5: 'singles', 2: 'double'}
        if space in space_dict:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/linespace_%s' % space_dict[space]).click()
        else:
            for i in range(50):
                space_ele = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_number_picker_recycler_view"]' \
                            '/android.widget.TextView[@index="1"]'
                space_now = float(self.get_element(space_ele).text)
                if space != space_now:
                    if space < space_now:
                        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_left').click()
                    else:
                        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_right').click()
                else:
                    break
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def text_align(self, type, align):  # 文本位置
        logging.info('==========text_align==========')
        align_dict = {'左对齐': '1', '居中': '2', '右对齐': '3', '两端对齐': '4', '分散对齐': '5'}
        if type == 'pg':
            align_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_pg_option_id_edit_para_hor_align"]' \
                          '/android.widget.FrameLayout[%s]' % (align_dict[align])
        else:
            align_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_para_hor_align"]' \
                          '/android.widget.FrameLayout[%s]' % (type, align_dict[align])
        self.driver.find_element(By.XPATH, align_index).click()

    def bullets_numbers(self, type, index, s_index=0):  # 项目符号、项目编码s_index=1-15
        logging.info('==========bullets_numbers==========')
        if type == 'pg':
            num_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_pg_option_id_edit_item_bullets_numbers"]' \
                        '/android.widget.FrameLayout[%s]' % index
        else:
            num_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_item_bullets_numbers"]' \
                        '/android.widget.FrameLayout[%s]' % (type, index)
        self.driver.find_element(By.XPATH, num_index).click()
        if index >= 6:
            if s_index <= 7 and s_index > 0:
                self.driver.find_elements(By.XPATH,
                                          '//*[@resource-id="com.yozo.office.en:id/yozo_ui_wp_option_id_item_bullets"]'
                                          '/android.widget.FrameLayout[%s]' % (s_index)).click()
            elif s_index > 7 and s_index < 16:
                self.driver.find_element(By.XPATH,
                                         '//*[@resource-id="com.yozo.office.en:id/yozo_ui_wp_option_id_item_numbers"]'
                                         '/android.widget.FrameLayout[%s]' % (s_index - 7)).click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def high_light_color(self, type, index=1, s_index=0):  # 高亮颜色
        logging.info('==========high_light_color==========')
        color_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_highlight_color"]' \
                      '/android.widget.FrameLayout[%s]' % (type, index)
        self.driver.find_element(By.XPATH, color_index).click()
        if index >= 6:
            self.driver.find_element(By.XPATH, '//android.support.v7.widget.RecyclerView'
                                               '/android.widget.FrameLayout[%s]' % s_index).click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def font_color(self, type, index=1, s_index=41):  # 字体颜色
        logging.info('==========font_color==========')
        if type == 'pg':
            color_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_pg_option_id_edit_font_color"]' \
                          '/android.widget.FrameLayout[%s]' % index
        else:
            color_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_font_color"]' \
                          '/android.widget.FrameLayout[%s]' % (type, index)
        self.driver.find_element(By.XPATH, color_index).click()
        if index >= 6:
            self.driver.find_element(By.XPATH, '//android.support.v7.widget.RecyclerView'
                                               '/android.widget.FrameLayout[%s]' % s_index).click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def font_style(self, type, style):  # 加粗，倾斜，划掉，下划线
        logging.info('==========font_style==========')
        style_dict = {'加粗': '0', '倾斜': '1', '删除线': '2', '下划线': '3'}
        if type == 'pg':
            style_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_pg_option_id_edit_font_style"]' \
                          '/android.widget.FrameLayout[@index="%s"]' % style_dict[style]
        else:
            style_index = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_%s_option_id_font_style"]' \
                          '/android.widget.FrameLayout[@index="%s"]' % (type, style_dict[style])
        self.driver.find_element(By.XPATH, style_index).click()

    def font_name(self, type, name='Noto Color Emoji'):  # 字体类型选择，目前只取系统自带选项的第一个
        logging.info('==========font_name==========')
        if type == 'pg':
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_pg_option_id_edit_font_name').click()
        else:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_%s_option_id_font_name' % type).click()
        time.sleep(1)
        ele1 = '//*[@text="系统"]'
        ele2 = '//*[@text="最近"]'
        ele3 = '//*[@text="字体"]'
        self.swipe_ele(ele2, ele3)
        self.swipe_ele(ele1, ele3)
        range = '//*[@resource-id="com.yozo.office.en:id/system_font_names"]/android.widget.RelativeLayout'
        name_ele = '//*[@text="%s"]' % name
        self.swipe_search2(name_ele, range)
        self.driver.find_element(By.XPATH, '//*[@text="%s"]' % name).click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_back_button').click()

    def font_size(self, size):  # 字体大小
        logging.info('==========font_size: %s==========' % size)
        font_ele = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_number_picker_recycler_view"]' \
                   '/android.widget.TextView[@index="1"]'
        font = int(self.get_element(font_ele).text)
        if size != font:
            if size < font:
                self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_left').click()
            else:
                self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_number_picker_arrow_right').click()
            self.font_size(size)

    def fold_expand(self):
        logging.info('==========fold_expand==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_option_expand_button').click()

    def search_content(self, type, content):  # 查找内容
        logging.info('==========search_content==========')
        setting_btn = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_iv_find_replace_switch"]'
        if self.get_element_result(setting_btn):
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_iv_find_replace_switch').click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/rb_find').click()
        else:
            if type == 'wp':
                self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_wp_option_id_find_replace').click()
            elif type == 'ss':
                self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_ss_option_id_ll_find').click()
            else:
                self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_quick_option_id_pg_find').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_et_find_content').set_text(content)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_iv_icon_search').click()

    def replace_content(self, replace, num='one'):
        logging.info('==========replace==========')
        if not self.get_element_result('//*[@resource-id="com.yozo.office.en:id/yozo_ui_iv_replace_one"]'):
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_iv_find_replace_switch').click()
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/rb_replace').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_et_replace_content').set_text(replace)
        if num == 'one':
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_iv_replace_one').click()
        else:
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_tv_replace_all').click()

    def share_file(self, type, way):  # 分享way=['wx','qq','ding','mail']
        logging.info('==========share_file==========')
        self.group_button_click('文件')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_%s_option_id_share_by_%s' % (type, way)).click()

    def export_pdf(self, file_name, save_path):  # 导出pdf
        logging.info('==========export_pdf==========')
        self.group_button_click('文件')
        self.driver.find_element(By.XPATH, '//*[@text="输出为PDF"]').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_folder').click()
        logging.info('choose save path %s' % save_path)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_%s' % save_path).click()

        if self.get_toast_message('您尚未登录，请登录'):
            login = LoginView(self.driver)
            login.login_action('13915575564', 'zhang199412')
            self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_%s' % save_path).click()

        logging.info('file named %s' % file_name)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_file_name').set_text(file_name)

        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_file_type').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_select_save_path_save_btn').click()  # save

    def check_export_pdf(self):
        logging.info('==========check_export_pdf==========')
        time.sleep(1)
        return self.get_toast_message('导出成功')

    def switch_write_read(self):  # 阅读模式与编辑模式切换
        logging.info('==========switch_write_read==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_mode').click()

    def check_write_read(self):
        logging.info('==========check_write_read==========')
        undo = '//*[@resource-id="com.yozo.office.en:id/yozo_ui_toolbar_button_undo"]'
        if self.get_element_result(undo):
            logging.info('edit mode')
            return False
        else:
            logging.info('read mode')
            return True

    def screen_rotate(self, rotate):  # 旋转屏幕
        logging.info('==========screen_rotate==========')
        # allowed_values = ['LANDSCAPE', 'PORTRAIT']
        self.driver.orientation = rotate

    def check_rotate(self):
        logging.info('==========check_rotate==========')
        f_width = self.driver.get_window_size()['width']
        print(f_width)
        self.screen_rotate('LANDSCAPE')
        s_width = self.driver.get_window_size()['height']
        print(s_width)
        if f_width == s_width:
            return True
        else:
            return False

    def undo_option(self):  # 撤销
        logging.info('==========undo_option==========')
        time.sleep(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_undo').click()
        time.sleep(1)

    def redo_option(self):  # 重做
        logging.info('==========redo_option==========')
        time.sleep(1)
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/yozo_ui_toolbar_button_redo').click()
        time.sleep(1)

    def file_info(self):
        """
        打开文档信息
        :param file_type: 文档类型：'wp', 'ss', 'pg'
        :return:
        """
        logging.info('==========file_info==========')
        self.group_button_click('文件')
        try:
            self.driver.find_element(By.XPATH, '//*[@text="文档信息"]')
        except NoSuchElementException:
            ele_save = self.driver.find_element(By.XPATH, '//*[@text="保存"]')
            ele_share = self.driver.find_element(By.XPATH, '//*[@text="分享"]')
            Common(self).swipe_ele1(ele_share, ele_save)

        self.driver.find_element(By.XPATH, '//*[@text="文档信息"]').click()

    def wait_loading(self, timeout=180):
        """
        等待加载控件消失,默认等待3分钟，超时则抛出异常
        :param timeout: 等待时间
        :return:
        """
        logging.info('==========wait_loading==========')
        try:
            WebDriverWait(self.driver, timeout).until_not(
                ec.visibility_of_element_located((By.CLASS_NAME, 'android.widget.ProgressBar')))
        except TimeoutException:
            logging.error('等待超时，抛出异常')


if __name__ == '__main__':
    list1 = ['dfs', 'ddfdf', 'gbg', 'ryy']
    for e, i in enumerate(list1):
        print(e, i)
    # str = '123'
    # str1 = str[:-1]
    # print(str1)
