import os
import json
import csv
from modules.google_gmail_api import Email_Reader
from modules.constatns import fieldnames
from modules.helpers import *
import time
from modules.burning_man import Burining_Man
import logging


log_file_path = os.path.join(os.path.dirname(__file__), 'file.log')
logger = logging.getLogger('Burning man')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename=os.path.join(log_file_path, mode='a', encoding='utf-8'))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

captcha_solver_api_key = 'your anti-captcha account api_key'
burining_man = Burining_Man(captcha_solver_api_key)
#signing up the emails in the file accounts.csv and creating an output file signed_accounts.csv with the field username filled
input_filepath = os.path.join(os.path.dirname(__file__), 'data', 'accounts.csv')
output_filepath = os.path.join(os.path.dirname(__file__), 'data', 'signed_accounts.csv')

print('Signing up the emails..')
if not os.path.exists(output_filepath):
    output_file = open(output_filepath, 'w', newline='', encoding='utf-8')
    input_file = open(input_filepath)
    csv_writer = csv.DictWriter(output_file, fieldnames)
    csv_writer.writeheader()
    csv_reader = csv.DictReader(input_file)

    for account_details in csv_reader:
        print('Email:', account_details['Email'])
        logger.info('Signing up email: ' + account_details['Email'])
        if account_details['Username'] == '':
            account_details, state = burining_man.signup_account(account_details)
            logger.info('State:\n' + json.dumps(state, indent=4))
        csv_writer.writerow(account_details)
        output_file.flush()
    output_file.close()
    input_file.close()

print('Waiting 30 secs to make sure that the activation emails are recieved.')
time.sleep(30)
print('Setting passwords for the accounts..')
#setting a password for the usernames in in the file signed_accounts.csv and creating an output file verified_accounts.csv with the field password filled
input_filepath = os.path.join(os.path.dirname(__file__), 'data', 'signed_accounts.csv')
output_filepath = os.path.join(os.path.dirname(__file__), 'data', 'verified_accounts.csv')

if not os.path.exists(output_filepath):
    output_file = open(output_filepath, 'w', newline='', encoding='utf-8')
    input_file = open(input_filepath)
    csv_writer = csv.DictWriter(output_file, fieldnames)
    csv_writer.writeheader()
    csv_reader = csv.DictReader(input_file)

    email_reader = Email_Reader()
    email_reader.login()
    
    for account_details in csv_reader:
        username = account_details['Username']
        print(f'Username: {username}')
        if username != '' and account_details['Password'] == '':
            password = burining_man.generate_password()
            activation_link = email_reader.get_activation_url(username)
            print(f'Activation link: {activation_link}')
            if activation_link != '':
                try:
                    burining_man.set_account_password(activation_link, password)
                    account_details['Password'] = password
                except Exception as e:
                    print(e)
                    print('Can not reset password for the specified user.')
            else:
                print('No activation link found.')
        csv_writer.writerow(account_details)
        output_file.flush()
    output_file.close()
    input_file.close()


#copying the final data to the accounts.csv file and deleting the temp files

input_filepath = os.path.join(os.path.dirname(__file__), 'data', 'verified_accounts.csv')
output_filepath = os.path.join(os.path.dirname(__file__), 'data', 'accounts.csv')
output_file = open(output_filepath, 'w', newline='', encoding='utf-8')
input_file = open(input_filepath)
csv_writer = csv.DictWriter(output_file, fieldnames)
csv_writer.writeheader()
csv_reader = csv.DictReader(input_file)
for row in csv_reader:
    csv_writer.writerow(row)
    output_file.flush()
output_file.close()
input_file.close()
os.remove(os.path.join(os.path.dirname(__file__), 'data', 'signed_accounts.csv'))
os.remove(os.path.join(os.path.dirname(__file__), 'data', 'verified_accounts.csv'))
