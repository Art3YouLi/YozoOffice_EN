#!/user/bin/env python3
# -*- coding: utf-8 -*-

import HTMLTestRunner
import os
import unittest
import time
import logging
import sys
from common.common_data import *

path = os.path.dirname(os.getcwd())
sys.path.append(path)

suite = unittest.TestSuite()
for caseFile in CASE_FILES:
    discover = unittest.defaultTestLoader.discover(CASE_DIR, pattern=caseFile, top_level_dir=None)
    for case in discover:
        suite.addTests(case)

now = time.strftime('%Y-%m-%d %H_%M_%S')
report_name = REPORT_DIR + '/' + now + 'Mobile_Office_Report.html'
with open(r'%s' % report_name, 'wb') as f:
    runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='YOZO_Mobile_Office_en_Report',
                                           description='yozo en Android app test reports')
    logging.info('start run test case...')
    runner.run(suite)

