#!/user/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import unittest
from common.deserid_caps import *


def start_server():
    """
    启动appium服务
    :return: None
    """
    logging.info('start appium')
    caps = get_desired_caps()
    port, bp, udid = caps['port'], caps['bp'], caps['desired_caps']['udid']
    cmd = os.popen('netstat -ano | findstr "%s" ' % port)
    msg = cmd.read()
    if "LISTENING" in msg:
        print("appium服务已经启动：%s" % msg)
    else:
        print("appium服务启动：%s" % msg)
        os.system("start /b appium -a 127.0.0.1 --session-override -p %s -bp %s -U %s" % (port, bp, udid))
        time.sleep(5)


def stop_server():
    """
    结束appium服务
    :return: None
    """
    os.system("start /b taskkill /F /t /IM node.exe")


class StartEnd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.info('=====setUpClass=====')
        start_server()

    @classmethod
    def tearDownClass(cls):
        logging.info('=====tearDownClass=====')
        stop_server()

    def setUp(self):
        logging.info('=====setUp====')
        # os.system('adb shell pm clear com.tencent.mobileqq')
        # os.system('adb shell pm clear com.tencent.mm')
        # os.system('adb shell pm clear com.vivo.email')
        # os.system('adb shell pm clear com.alibaba.android.rimet')
        os.system('adb shell am force-stop com.tencent.mobileqq')
        os.system('adb shell am force-stop com.tencent.mm')
        os.system('adb shell am force-stop com.vivo.email')
        os.system('adb shell am force-stop com.alibaba.android.rimet')
        self.driver = appium_desired()

    def tearDown(self):
        logging.info('====tearDown====')
        self.driver.close_app()

