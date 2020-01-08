#!/user/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import logging
import logging.config
from appium import webdriver
from common.common_data import *
from airtest.core.api import auto_setup

logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


def get_desired_caps():
    """
    读取desired caps并返回
    :return: desired caps
    """
    with open(CAPS_YAML, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        print(data)
    return data


def appium_desired():
    data = get_desired_caps()
    desired_caps = data['desired_caps']
    # airtest 输入法禁用 此输入法禁用后，无法使用poco().set_text()
    # yosemite = '?ime_method=None'
    auto_setup(__file__, devices=["Android:///%s?ime_method=ADBIME" % data['desired_caps']['udid']])
    logging.info('start app...')
    driver = webdriver.Remote('http://%s:%s/wd/hub' % (data['ip'], data['port']), desired_caps)
    driver.implicitly_wait(3)
    return driver
