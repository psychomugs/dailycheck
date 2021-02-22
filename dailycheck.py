import selenium
from selenium import webdriver as wd
from webdriver_manager.chrome import ChromeDriverManager
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--netid', type=str, default='')
parser.add_argument('-p', '--password', type=str, default='')
parser.add_argument('--headless', action='store_true', default=False)
args = vars(parser.parse_args())

op = wd.ChromeOptions()
if args['headless']:
    op.add_argument('headless')
d = wd.Chrome(
    executable_path=ChromeDriverManager().install(),
    options=op
)

d.get('https://dailycheck.cornell.edu/saml_login_user?redirect=%2Fdaily-checkin')

# login with netID and password
d.find_elements_by_id('netid')[0].send_keys(args['netid'])
d.find_elements_by_id('password')[0].send_keys(args['password'])
d.find_elements_by_class_name('input-submit')[0].click()
time.sleep(1)

try:
    # proceed to form
    c = d.find_elements_by_id('continue')[0]
    c.click()

    # click on all NO radio buttons
    radios = [
        'covidsymptoms',
        'contactsymptoms',
        'exposure',
        'positivetestever'
    ]
    for radio in radios:
        d.find_elements_by_id(radio+'-no')[0].click()

    # submit twice
    for _ in range(2):
        d.find_elements_by_id('submit')[0].click()
        time.sleep(1)
except:
    print("Could not find form...")

try:
    status = d.find_elements_by_xpath('/html/body/div[2]/main/div/article/div[2]/div/div/div/h2')[0]
    status_msg = status.get_attribute('innerHTML')
    status_msg = status_msg[:status_msg.find('<')]+status_msg[status_msg.find('>')+1:]
    print("Status message: ", status_msg)
except:
    print("Error logging in and completing form, no status message found")

d.close()