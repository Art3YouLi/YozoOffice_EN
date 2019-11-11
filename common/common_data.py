#!/user/bin/env python3
# -*- coding: utf-8 -*-

SHARE_LIST = ['wp_wx', 'wp_qq', 'wp_ding', 'wp_mail', 'ss_wx', 'ss_qq', 'ss_ding',
              'ss_mail', 'pg_wx', 'pg_qq', 'pg_ding', 'pg_mail']
WPS = ['wp', 'ss', 'pg']
PS = ['ss', 'pg']
WP = ['wp', 'pg']
WS = ['wp', 'ss']
TYPE_LIST = ['all', 'wp', 'ss', 'pg', 'pdf']
SEARCH_DICT = {'wp': 'docx', 'ss': 'xlsx', 'pg': 'pptx'}
FOLDER_LIST = ['Moblie Phones', 'My Documents', 'Download', 'QQ', 'Wechat']
INDEX_SHARE_LIST = ['qq', 'wechat', 'email', 'more']

# SS
AUTO_SUM = [' AutoSum ', ' Average ', ' Count ', ' Max ', ' Min ']
DATE_FILTER = ['等于', '不等于', '在以下日期之后', '在以下日期之后或与之相同', '在以下日期之前',
               '在以下日期之钱或与之相同', '开始于', '非开始于', '结束于', '非结束于', '包含', '不包含']
NUM_FILTER = ['等于','不等于','大于','大于等于','小于','小于等于','开始于','非开始于','结束于','非结束于','包含','不包含']
TEXT_FILTER = ['等于','不等于','大于','大于等于','小于','小于等于','开始于','非开始于','结束于','非结束于','包含','不包含']

# PG
FORMAT = [' Title and Subtitle ', ' Title ', ' Title and Text ', ' Title and Two Column Text ',
          ' Title and Vertical Text ', ' Vertical Title and Text ', ' Blank ', ' Title and Picture ',
          ' Title, Text and Picture ', ' Title, Picture and Text ', ' Title, Picture and Vertical Text ',
          ' Title, Vertical Text and Picture ']
SWITCH_LIST = [' None ', ' Fade ', ' Fade Through Black ', ' Cut ', ' Cut Through Black ', ' Dissolve ',
               ' Wipe from Bottom ', ' Wipe from Left ', ' Wipe from Right ', ' Wipe from Top ',
               ' Wheel ', ' Pull from Bottom ', ' Pull from Left ', ' Pull from Right ', ' Pull from Top ',
               ' Pull from Bottom-Left ', ' Pull from Top-Left ', ' Pull from Buttom-Right ', ' Pull from Top-Right ',
               ' Box Shrink ', ' Box Expand ', ' 1 Spoke ', ' 2 Spokes ', ' 3 Spokes ', ' 4 Spokes ', ' 8 Spokes ',
               ' Vertical In ', ' Vertical Out ', ' Horizontal In ', ' Horizontal Out ', ' Expand from Bottom-Left ',
               ' Expand from Top-Left ', ' Expand from Bottom-Right ', ' Expand from Top-Right ', ' Circle ',
               ' Diamond ', ' Plus ', ' Flash ', ' Push from Bottom ', ' Push from Left ', ' Push from Right ',
               ' Push from Top ', ' Insert From Bottom ', ' Insert From Left ', ' Insert From Right ',
               ' Insert From Top ', ' Insert From Bottom-Left ', ' Insert From Top-Left ', ' Insert From Bottom-Right ',
               ' Insert From Top-Right ', ' Horizontal Blinds ', ' Vertical Blinds ', ' Horizontal Checkerboard ',
               ' Vertical Checkerboard ', ' Horizontal Comb ', ' Vertical Comb ', ' Horizontal Bars ',
               ' Vertical Bars ', ' Random ']

# File path
CSV_FILE = '../data/account.csv'
CASE_DIR = '../test_case'
REPORT_DIR = '../reports'
CON_LOG = '../config/logs.conf'
CAPS_YAML = '../config/yozo_office_caps.yaml'
SEREEN_SHOTS = '../screenshots/'

# Test case
CASE_FILES = ['test_homepage.py', 'test_common.py', 'test_wp.py', 'test_ss.py', 'test_pg.py']

