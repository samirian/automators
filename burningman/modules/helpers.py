import time
import random
import string


def wait_for_element_visibility(driver, xpath: str, timeout=-1):
    if timeout == -1:
        while True:
            try:
                driver.find_element_by_xpath(xpath)
                return
            except:
                time.sleep(1)
    else:
        for i in range(timeout):
            try:
                driver.find_element_by_xpath(xpath)
                return
            except:
                time.sleep(1)
    raise Exception('timedout')

                
def send_keys_slow(element, keys: str):
	import random
	for key in keys:
		element.send_keys(key)
		time.sleep(random.uniform(0.1, 0.25))


def delay(start=2, end=3):
    time.sleep(random.randint(start, end))


def generate_random_string(number_of_letters: int):
    letters = ''
    for _ in range(number_of_letters):
        letters += random.choice(string.ascii_letters)
    return letters


def generate_random_number(number_of_digits: int):
    start_number = pow(10, number_of_digits - 1)
    end_number = start_number * 10 - 1
    return random.randint(start_number, end_number)
