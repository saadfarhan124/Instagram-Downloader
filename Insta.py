from tkinter import *
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.common.exceptions import NoSuchElementException
import time
import urllib.request
import unittest
from pathlib import Path
import pickle
from webdriver_manager.chrome import ChromeDriverManager


class Instagram(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://www.instagram.com/')

    def login(self):
        # login = self.driver.find_element_by_class_name("_2hvTZ pexuQ zyHYP").find_element_by_tag_name('a')
        # login.click()
        time.sleep(15)
        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys('INSTA_USERNAME')
        self.driver.find_element_by_xpath('//input[@name="password"]').send_keys('INSTA_PASSWORD')
        self.driver.find_element_by_class_name('L3NKy').click()
        time.sleep(5)
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def test_instagram(self):
        cookies = Path('cookies.pkl')
        if not cookies.is_file():
            self.login()
        else:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        url = 'https://www.instagram.com/p/ByvLb4QnpR1/'
        self.driver.get(url)
        counter = 0
        src = self.driver.find_element_by_class_name('KL4Bh').find_element_by_tag_name('img').get_attribute('src')
        filename = url.split('/')
        filename = filename[len(filename) - 2] + '.jpg'
        urllib.request.urlretrieve(src, 'images/{}'.format(filename))
        if self.find_element():
            while self.find_element():
                self.driver.find_element_by_class_name('_6CZji').click()
        images = self.driver.find_elements_by_class_name('KL4Bh')
        for image in images:
            print(image)
            src = image.find_element_by_tag_name('img').get_attribute('src')
            filename = url.split('/')
            filename = filename[len(filename) - 2] + '{}.jpg'.format(counter)
            counter = counter + 1
            urllib.request.urlretrieve(src, 'images/{}'.format(filename))

    def tearDown(self):
        time.sleep(5)
        self.driver.close()

    def find_element(self):
        try:
            self.driver.find_element_by_class_name('_6CZji')
            return True
        except NoSuchElementException:
            return False

if __name__ == '__main__':
    unittest.main()