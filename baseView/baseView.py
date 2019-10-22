#!/user/bin/env python3
# -*- coding: utf-8 -*-


class BaseView(object):
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *loc):
        # WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element(*loc))
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        # WebDriverWait(self.driver, 20).until(lambda driver: driver.find_elements(*loc))
        return self.driver.find_elements(*loc)

    def get_window_size(self):
        return self.driver.get_window_size()

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        return self.driver.swipe(start_x, start_y, end_x, end_y, duration)