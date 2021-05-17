import os
import random
import requests
from modules.captcha_solver import Captcha_Solver
from selenium import webdriver
from modules.helpers import *
from copy import deepcopy


class Burining_Man:
    def __init__(self, captcha_solver_api_key: str):
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
        }
        self.__signup_url = "https://profiles.burningman.org/signup"
        self.__site_key = '6Lcu8bEUAAAAAOgsfUZCexoE7gerCoycrmv9w6Ub'
        self.__solver = Captcha_Solver(captcha_solver_api_key)
    
    def signup_account(self, account_details: dict) -> tuple:
        state = {}
        g_response = self.__solver.solve(self.__site_key, self.__signup_url)
        print("Solution recieved!")
        temp_account_details = deepcopy(account_details)
        temp_account_details['Username'] = self.generate_username(account_details['Name'])
        form_data = self.__create_signup_form(temp_account_details, g_response)
        try:
            json_response = requests.post('https://portalapi.burningman.org/api/profile', headers=self.__headers, data=form_data).json()
            if json_response['status']['message'] == 'OK':
                account_details = temp_account_details
                state['status'] = 'ok'
                print('Account created successfully.')
            else:
                state['status'] = json_response['status']['message']
                print('The website returns an error message.')
            state['api_response'] = json_response
        except Exception as e:
            state['status'] = 'non json response'
            print('The website refused the connection.')
        return account_details, state

    def __create_signup_form(self, account_details: dict, g_response: str):
        return {
            'username': account_details['Username'],
            'email': account_details['Email'],
            'fname': account_details['Name'].split(' ')[0],
            'lname': account_details['Name'].split(' ')[1],
            'pname': "",
            'org': "",
            'title': "",
            'work': "",
            'url': "",
            'addr1': account_details['Address'].split(', ')[0],
            'addr2': "",
            'city': account_details['Address'].split(', ')[-2],
            'state': account_details['Address'].split(', ')[-1].split(' ')[0],
            'country': "US",
            'zip': account_details['Address'].split(' ')[-1],
            'phone1': account_details['Phone'],
            'bmyears': [
                str(random.randint(2014,2019))
            ],
            'affs': [],
            'descr': "",
            'recaptcha_response': g_response
        }

    def generate_username(self, name: str):
        return name.replace(' ', '') + str(generate_random_number(5))

    def generate_password(self):
        return generate_random_string(1).lower() + generate_random_string(1).upper() + str(generate_random_number(12))

    def set_account_password(self, activation_link: str, password: str):
        driver = webdriver.Chrome(os.getcwd() +'/chromedrivers/windows_chromedriver')
        driver.set_page_load_timeout(60)
        driver.get(activation_link)
        wait_for_element_visibility(driver, '//div[@id="sign-in-widget"]', 60)
        wait_for_element_visibility(driver, '//span[@data-se="o-form-input-newPassword"]/input[@type="password"]', 30)
        send_keys_slow(driver.find_element_by_xpath('//span[@data-se="o-form-input-newPassword"]/input[@type="password"]'), password)
        delay()
        send_keys_slow(driver.find_element_by_xpath('//span[@data-se="o-form-input-confirmPassword"]/input[@type="password"]'), password)
        delay()
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//input[@type="submit"]'))
        delay(4, 5)
        error_xpath = '//div[contains(@class, "o-form-has-error")]'
        if len(driver.find_elements_by_xpath(error_xpath)) > 0:
            raise Exception('Can not reset password.')
        else:
            wait_for_element_visibility(driver, '//a[@class="item menu-signup"][text()="Log Out"]', 60)
            delay(8, 10)
        self.update_profile(driver)
        driver.close()

    def update_profile(self, driver):
        driver.get('https://profiles.burningman.org/my-profile')
        wait_for_element_visibility(driver, '//input[@id="Never"]')
        delay(1, 2)
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//input[@id="Never"]'))
        delay(1, 2)
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//button[@type="submit"]'))
        wait_for_element_visibility(driver, '//div[contains(@class, "display-success")]')
        delay(5, 6)

    def is_vertification_page_has_error(self):
        pass
