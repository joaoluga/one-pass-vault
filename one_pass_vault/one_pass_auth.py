from .command_builder.one_pass_command_builder import OnePassCommandBuilder
import os
import configparser
from datetime import datetime
import logging


class OnePassAuth(OnePassCommandBuilder):

    __USER = os.environ["USER"]
    __OP_DIR = f'/home/{__USER}/.op'
    __SESSION_TOKEN_FILEPATH = f'/home/{__USER}/.one-pass-vault/session_token'
    __CONFIG = configparser.ConfigParser()
    __CONFIG_DIR = f'/home/{__USER}/.one-pass-vault'
    __CONFIG_FILE = 'config'
    __CONFIG_FILEPATH = os.path.join(__CONFIG_DIR, __CONFIG_FILE)
    __NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, profile):
        self.__profile = profile

        if os.path.exists(self.__CONFIG_FILEPATH):
            self.__config_attributes_setter()
        else:
            self.__create_conf_file()
            self.__profile_register_flow()

        if not self.__is_session_token_still_valid():
            self.__generate_session_token()
        else:
            self.__spawn_current_session_token()
        self.__set_execution_date()

    def __config_attributes_setter(self):
        try:
            self.__CONFIG.read(self.__CONFIG_FILEPATH)
            target_profile = self.__CONFIG[f'profile {self.__profile}']
            self.__sign_in_address = target_profile['sign_in_address']
            self.__sign_in_email = target_profile['sign_in_email']
            self.__last_execution_date = target_profile['last_execution_date']
        except KeyError:
            self.__profile_register_flow()

    def __create_conf_file(self):
        if not os.path.exists(self.__CONFIG_DIR):
            logging.info('Creating config file already exists')
            os.mkdir(self.__CONFIG_DIR)
        else:
            logging.info('config file already exists')

    def __register_profile_in_conf_file(self):
        logging.info(f'Registering new profile: {self.__profile}')
        with open(self.__CONFIG_FILEPATH, 'w') as conf_file:
            self.__CONFIG[f'profile {self.__profile}'] = {
                'sign_in_address': self.__sign_in_address,
                'sign_in_email': self.__sign_in_email,
                'last_execution_date': self.__last_execution_date
            }
            self.__CONFIG.write(conf_file)

    def __profile_register_flow(self):
        account_type = input('Is your account personal (y/n): ')
        if account_type == 'y':
            self.__sign_in_address = 'my'
        else:
            self.__sign_in_address = input('Inform your sign-in address: ')
        self.__sign_in_email = input('Inform your sign-in email: ')
        self.__last_execution_date = self.__NOW
        self.__register_profile_in_conf_file()

    def __register_device(self):
        return self.run_op_command(
            f'signin {self.__sign_in_address} {self.__sign_in_email} --raw',
            json_output=False)

    def __login_with_registered_profile(self):
        return self.run_op_command(f'signin {self.__sign_in_address} --raw',
                                   json_output=False)

    def __generate_session_token(self):
        if os.path.exists(self.__OP_DIR):
            session_token = self.__login_with_registered_profile()
        else:
            session_token = self.__register_device()
        os.environ['ONE_PASS_VAULT_SESSION_TOKEN'] = session_token

        with open(self.__SESSION_TOKEN_FILEPATH, 'w') as session_token_file:
            session_token_file.truncate(0)
            session_token_file.write(session_token)

    def __is_session_token_still_valid(self):
        conf_date = datetime.strptime(self.__last_execution_date, '%Y-%m-%d %H:%M:%S')
        current_date = datetime.strptime(self.__NOW, '%Y-%m-%d %H:%M:%S')
        minutes = round((current_date - conf_date).total_seconds()/60, 0)
        if minutes <= 10:
            return True
        else:
            return False

    def __spawn_current_session_token(self):
        session_token = open(self.__SESSION_TOKEN_FILEPATH).read()
        os.environ['ONE_PASS_VAULT_SESSION_TOKEN'] = session_token

    def __set_execution_date(self):
        with open(self.__CONFIG_FILEPATH, 'w') as conf_file:
            target_profile = self.__CONFIG[f'profile {self.__profile}']
            target_profile['last_execution_date'] = self.__NOW
            self.__CONFIG.write(conf_file)
