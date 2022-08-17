import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nordvpn_switcher import rotate_VPN, initialize_VPN, terminate_VPN


data = pd.read_csv(r'C:\Users\sagar b j\OneDrive\Documents\tertium_office_doc\Logestics_Companies\yellowpages_out\USA\logistic_Kentucky_out.csv',
                    header=0, encoding='unicode_escape')
companies = data['cname'].tolist()
Name1 = data['NAME 1'].tolist()


# companies = companies[98:]
# Name1 = Name1[98:]
print('Companies')
print(companies)
print(len(companies))
print('owner name')
print(Name1)
print(len(Name1))

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("log-level=3")


ser = Service(r'C:\seleniumDrivers\chromedriver.exe')
driver = webdriver.Chrome(service=ser, options=options)
# driver.maximize_window()
driver.implicitly_wait(3)
driver.get(r'https://www.google.com/')


email1 = []
email1_per = []
name1 = []
cnme = []
match_email1 = []
url = []
# count j
j = 1
chk = 0
for cn, nm in zip(range(len(companies)), range(len(Name1))):
    print('-----------------------------')
    print('company name: ',companies[cn])
    while True:
        if chk == 1:
            chk = 0

        try:
            driver.get(r'https://www.google.com/')
            m = driver.find_element(by=By.NAME, value='q')
            m.clear()
            m.send_keys(f'{companies[cn]} in rocketreach Email Format')
            m.send_keys(Keys.ENTER)
            break
        except:
            while True:
                try:
                    print("Rotating Driver")
                    settings = initialize_VPN(area_input=['complete rotation'], skip_settings=1)
                    rotate_VPN(settings)
                    rotate_VPN(settings, google_check=1)
                    chk = 1
                    driver.get(r'https://www.google.com/')
                    break
                except:
                    print("driver error occured")
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("log-level=3")

            ser = Service(r'C:\seleniumDrivers\chromedriver.exe')
            driver = webdriver.Chrome(service=ser, options=options)

    string = Name1[nm].lower()
    print('owner name: ',string)
    print('count: ', j)
    j += 1
    if 'nan' in string or 'the' in string or 'ceo' in string:
        cnme.append(companies[cn])
        name1.append('None')
        email1.append('None')
        email1_per.append('None')
        match_email1.append('None')
        url.append("None")
        print(string)
        continue
    else:
        string = string.replace('.', ' ')
        string = string.split(' ')
        string = string[:-1]
        print(string)
        if len(string) > 1:
            fname = string[0]
            lname = string[1]
        else:
            fname = string

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    srch_res = soup.find('div', {"class":'yuRUbf'}).parent.parent.parent

    lnk = srch_res.find('div', class_="yuRUbf").find('a')['href']
    flnk = lnk.find('rocketreach')

    if flnk != -1:
        try:
            get_rocketreach = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='yuRUbf']//a"))).click()
        except:
            # try:
            #     # captcha click
            #     WebDriverWait(driver, 20).until(
            #         EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
            #     WebDriverWait(driver, 20).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
            #     print('captcha clicked')
            # except:
            #     print()
            try:
                driver.find_element(By.XPATH, '//div[@class="max-width-layout row row-flex no-gutters rr-sec-fold-content"]')
                a = 1 / 0
            except:
                # time.sleep(100)
                print()

        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # captcha = soup.find('iframe', {'title': 'reCAPTCHA'})
        # if captcha:
        #     WebDriverWait(driver, 20).until(
        #         EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
        #     WebDriverWait(driver, 20).until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
        #     print('captcha clicked')
        # else:
        #     print('captcha None')
        #
        # if bool(captcha) == True or bool(captcha) == False:
        try:
            driver.find_element(By.XPATH, '//a[@data-ceid="company_primary-tab_email-format"]')
            time.sleep(2)
            email_format = driver.find_element(By.XPATH, '//a[@data-ceid="company_primary-tab_email-format"]').click()
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            email_format_table = soup.find('table', {'class': "table"})
            email_format_trs = email_format_table.findAll('tr')
            email_format_string = ""
            for no_tr, tr in enumerate(email_format_trs):
                tds = tr.findAll('td')
                if no_tr != 0:

                    for td in tds[:-1]:
                        email_format_string += td.text.strip()
                        email_format_string += ', '
                    email_format_string += tds[-1].text.strip()
                    email_format_string += '; '
            print('emailformat',email_format_string)
            sp1 = email_format_string.split(';')
            print('sp1 is ',sp1)
            sp1 = sp1[:-1]
            try:
                a = sp1[0].split(',')
                formula = a[0]
                domain = a[1]
                temp_form = formula.replace(' ','').replace("'",'').replace('last_initial',lname[0]).replace('first_initial',fname[0]).replace('last',lname).replace("first'_'last", fname+"'_'"+ lname).replace('first', fname).replace("first '.' last", fname+"'.'"+lname).replace("last '.' first", lname+"'.'"+fname)
                print('tempform: ',temp_form)
                f = domain.find('@')
                email = domain[f:]
                finalemail = temp_form + email
                print('finalemail: ',finalemail)

                url_ = driver.current_url
                print('url: ', url_)

                url.append(url_)
                print('url', len(url), url)
                name1.append(a[0])
                print('name1',len(name1),name1)
                email1.append(a[1])
                print('email',len(email1),email1)
                email1_per.append(a[2])
                print('per',len(email1_per),email1_per)
                match_email1.append(finalemail)
                print('match',len(match_email1),match_email1)
                cnme.append(companies[cn])
            except:
                cnme.append(companies[cn])
                name1.append('None')
                print('name',len(name1),name1)
                email1.append('None')
                print('email',len(email1), email1)
                email1_per.append('None')
                print('per',len(email1_per), email1_per)
                match_email1.append('None')
                print('match',len(match_email1),match_email1)
                url.append('None')
                print('url',len(url),url)

        except:
            cnme.append(companies[cn])
            name1.append('None')
            email1.append('None')
            email1_per.append('None')
            match_email1.append('None')
            url.append('None')
    else:
        cnme.append(companies[cn])
        name1.append('None')
        email1.append('None')
        email1_per.append('None')
        match_email1.append('None')
        url.append('None')
    # try:
    #     driver.get(r'https://google.co.in/')
    # except:
    #     while True:
    #         try:
    #             print("Rotating Driver")
    #             settings = initialize_VPN(area_input=['complete rotation'], skip_settings=1)
    #             rotate_VPN(settings)
    #             rotate_VPN(settings, google_check=1)
    #             chk = 1
    #             break
    #         except:
    #             print("driver error occured")
    # print(len(cnme))
    # print(len(name1))
    # print(len(email1))
    # print(len(email1_per))
    # print(len(match_email1))
    # print(len(url))
    #
    # address_dict = {'Company Name': cnme, 'Formula': name1, 'email 1': email1, 'email1 per': email1_per, 'FinalEmail': match_email1, 'Url': url}
    # df = pd.DataFrame(address_dict)
    # df.to_csv(r'sagar_emailrocketreach.csv')


print('-----------------------------')
print('Name1: ',len(name1),name1)
print(len(name1))
print('Email1: ',len(email1),email1)
print(len(email1))
print('Emailper1: ',len(email1_per),email1_per)
print(len(email1_per))
print('final email',match_email1)
print(len(match_email1))
print('url',url)
print(len(url))
print('-----------------------------')


address_dict = {'Company Name': cnme, 'Formula':name1, 'email 1':email1, 'email1 per': email1_per, 'FinalEmail':match_email1, 'Url':url}
df = pd.DataFrame(address_dict)
df.to_csv(r'C:\Users\sagar b j\OneDrive\Documents\tertium_office_doc\Logestics_Companies\rocketreach_email_formula\yellowpages_usa\yellowpages_Kentucky_emailrocketreach.csv')
driver.close()
