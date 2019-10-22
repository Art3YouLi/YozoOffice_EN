import logging
import time

from common.common_func import NoSuchElementException, Common
from selenium.webdriver.common.by import By


class LoginView(Common):

    def login_from_my(self,username, password):
        logging.info('==========login_from_my==========')
        self.find_element(By.ID, 'com.yozo.office.en:id/ll_myinfo_unlogin').click()
        self.login_action(username, password)

    def login_action(self, username, password):  # 登录操作
        logging.info('==========login_action==========')
        # self.driver.find_element(By.ID,'com.yozo.office.en:id/ll_myinfo_unlogin').click()
        logging.info('username is:%s' % username)
        self.find_element(By.ID, 'com.yozo.office.en:id/et_account').set_text(username)  # 输入手机号

        logging.info('password is:%s' % password)
        self.find_element(By.ID, 'com.yozo.office.en:id/et_pwd').set_text(password)  # 输入密码

        logging.info('click loginBtn')
        self.find_element(By.ID, 'com.yozo.office.en:id/btn_login').click()  # 点击登录按钮
        logging.info('login finished!')

    def check_login_status(self):
        logging.info('==========check_login_status==========')
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH, '//*[@text="退出登录"]')
        except NoSuchElementException:
            logging.error('login fail')
            self.getScreenShot('login fail')
            return False
        else:
            logging.info('login success!')
            return True

    def logout_action(self): #退出登录
        logging.info('==========logout_action==========')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/ll_myinfo_sure').click()
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/btn_sure').click()
        logging.info('logout finished!')
        self.driver.find_element(By.ID, 'com.yozo.office.en:id/iv_add_back').click()
        time.sleep(1)


