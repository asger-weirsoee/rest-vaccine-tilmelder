from email.mime.text import MIMEText
from pathlib import Path
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep
import json
import smtplib, ssl

from mail import get_message, send_mail, get_adm_message

root = Path(__file__).parent
with open(root.joinpath('config.json'), 'r+') as f:
    config = json.load(f)


class RestVacBot:
    name_text = None
    age_text = None
    phone_text = None

    def __init__(self, name, age, phone):
        self.name_text = name
        self.age_text = age
        self.phone_text = phone
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=options)

    def go_to_page(self):
        self.driver.get('https://rn.dk/sundhed/patient-i-region-nordjylland/coronavirus/covid-vaccination/restvacciner')
        sleep(5)
        accept_cookies = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[4]/div[2]/div/button')
        accept_cookies.click()
        sleep(1)
        drop_down_click = self.driver.find_element_by_xpath(
            '/html/body/form/div[4]/div[1]/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[4]/div/div/div/ul/li[3]/h3/a')
        drop_down_click.click()
        sleep(1)
        navigate_to_page = self.driver.find_element_by_xpath(
            '/html/body/form/div[4]/div[1]/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[4]/div/div/div/ul/li[3]/div/div/div/div/div/div/div/div/div/p[4]/a')
        navigate_to_page.click()

    def fill_out_form(self):
        already_vaccinated = self.driver.find_element_by_xpath(
            '/html/body/div/form/div[1]/div[2]/table/tbody/tr[2]/td/div/span[2]/label')
        already_vaccinated.click()
        name = self.driver.find_element_by_xpath('//*[@id="t337561910"]')
        name.send_keys(self.name_text)
        age = self.driver.find_element_by_xpath('//*[@id="n337561915"]')
        age.send_keys(self.age_text)
        phone_number = self.driver.find_element_by_xpath('//*[@id="t337561922"]')
        phone_number.send_keys(self.phone_text)
        vaccination_place = self.driver.find_element_by_xpath(
            '/html/body/div/form/div[1]/div[6]/table/tbody/tr[2]/td/div/span[2]/label')
        vaccination_place.click()
        sleep(1)
        next_button = self.driver.find_element_by_xpath('/html/body/div/form/div[2]/div[3]/input')
        next_button.click()
        sleep(5)
        close_button = self.driver.find_element_by_xpath('/html/body/div/form/div[2]/div[3]/input')
        close_button.click()

    def close(self):
        self.driver.quit()


def send_mail_to_config(recepient, content, errors):
    text_type = 'plain'
    txt = get_message(config['author']['name'], content, errors)
    msg = MIMEText(txt, text_type, 'utf-8')
    msg['Subject'] = f'{"!!!FEJL!!!!" if errors else "SUCCESS"}: anmodning om restvaccine'
    msg['From'] = config['email']['username']
    msg['To'] = recepient
    send_mail(config['email']['username'], config['email']['password'], msg)


def send_admin_mail(all_errors: dict):
    text_type = 'plain'
    txt = get_adm_message(config['author']['name'], all_errors)
    msg = MIMEText(txt, text_type, 'utf-8')
    msg['Subject'] = f'Admin message'
    msg['From'] = config['email']['username']
    msg['To'] = config['author']['email']
    send_mail(config['email']['username'], config['email']['password'], msg)


def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    if exc is not None:
        f = sys.exc_info()[-1].tb_frame.f_back
        stack = traceback.extract_stack(f)
    else:
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr


def main():
    all_errors = dict()

    for file in root.glob('subs/*'):
        if file.name.endswith('.json'):
            with open(file, 'r+') as f:
                obj = json.load(f)
                errors = []
                if not obj['name']:
                    errors.append('no name')
                if not obj['age']:
                    errors.append('no age')
                if not obj['phone']:
                    errors.append('no phone')

                if not errors:
                    with Display() as display:
                        try:

                            runner = RestVacBot(obj['name'], obj['age'], obj['phone'])
                            runner.go_to_page()
                            sleep(5)
                            runner.fill_out_form()
                            runner.close()
                            sleep(3)
                        except Exception as e:
                            errors.append(full_stack())

                all_errors[f.name] = errors
                send_mail_to_config(obj['email'], obj, errors)
    send_admin_mail(all_errors)


if __name__ == '__main__':
    main()
