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
SWITCH_LIST = ['无切换', '平滑淡出', '从全黑淡出', '切出', '从全黑切出', '溶解', '向下擦除', '向左擦除', '向右擦除',
               '向上擦除', '扇形展开', '从下抽出', '从左抽出', '从右抽出', '从上抽出', '从左下抽出', '从左上抽出',
               '从右下抽出', '从右上抽出', '盒状收缩', '盒状展开', '1根轮辐', '2根轮辐', '3根轮辐', '4根轮辐', '8根轮辐',
               '上下收缩', '上下展开', '左右收缩', '左右展开', '左下展开', '左上展开', '右下展开', '右上展开', '圆形',
               '菱形', '加号', '新闻快报', '向下推出', '向左推出', '向右推出', '向上推出', '向下插入', '向左插入',
               '向右插入', '向上插入', '向左下插入', '向左上插入', '向右下插入', '向右上插入', '水平百叶窗',
               '垂直百叶窗', '横向棋盘式', '纵向棋盘式', '水平梳理', '垂直梳理', '水平线条', '垂直线条', '随机']
FOLDER_LIST = ['手机', '我的文档', 'Download', 'QQ', '微信']
INDEX_SHARE_LIST = ['qq', 'wechat', 'email', 'more']
AUTO_SUM = ['求和', '平均值', '计数', '最大值', '最小值']
CASE_FILES = ['test_homepage.py', 'test_common.py', 'test_wp.py', 'test_ss.py', 'test_pg.py']

# File path
CSV_FILE = '../data/account.csv'
CASE_DIR = '../test_case'
REPORT_DIR = '../reports'
CON_LOG = '../config/logs.conf'
CAPS_YAML = '../config/yozo_office_caps.yaml'

