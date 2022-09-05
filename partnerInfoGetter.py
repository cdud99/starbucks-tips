#!/usr/bin/python3

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


def get_info(numbers, question_one, answer_one, question_two, answer_two, password):

    timeoutTime = 30;

    # Initialize Selenium Chrome WebDriver
    driver = get_driver()

    # Go to url for partner info
    driver.get('https://mysite.starbucks.com/Person.aspx')


    print('Login Page')
    WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element_by_id('ContentPlaceHolder1_MFALoginControl1_UserIDView_txtUserid'))
    driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_txtUserid').send_keys(numbers)
    driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_btnSubmit').click()
    

    timeout = datetime.now() + timedelta(seconds = timeoutTime)
    notFound = 0
    while notFound == 0 and datetime.now() < timeout:
        try:
            driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_lblErrMessage')
            notFound = 'Error'
        except Exception:
            print('No error')
        try:
            driver.find_element(By.ID, 'lnkbtnRetailKBA')
            notFound = 'SSO'
        except Exception:
            print('No SSO')
        try:
            driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1')
            notFound = 'Security'
        except Exception:
            print('No security')

    if notFound == 0 and dateTime.now() >= timeout:
        return 1, 'No SSO, Security Question, or Error'

    if notFound == 'Error':
        errorText = str(driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_lblErrMessage').text)
        return 1, errorText

    if notFound == 'SSO':
        WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element(By.ID, 'lnkbtnRetailKBA'))
        driver.find_element(By.ID, 'lnkbtnRetailKBA').click()


    print('Security Question')
    WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1'))
    securityQuestion = str(driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1').text)

    answer = ''
    if(securityQuestion == question_one):
        answer = answer_one
    elif(securityQuestion == question_two):
        answer = answer_two
    else:
        driver.quit()
        raise Exception('Security question not recognized')

    # if question == None or answer == None or password == None:
    #     return 0, securityQuestion

    # if question != securityQuestion:
    #     return 2, None

    driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_tbxKBA1').send_keys(answer)
    driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_btnSubmit').click()

    timeout = datetime.now() + timedelta(seconds = timeoutTime)
    notFound = 0
    while notFound == 0 and datetime.now() < timeout:
        try:
            driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblErrMessage')
            notFound = 'Error'
        except Exception:
            print('No error')
        try:
            driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_PasswordView_tbxPassword')
            notFound = 'Password'
        except Exception:
            print('No password')

    if notFound == 0 and dateTime.now() >= timeout:
        return 1, ['No error or password']

    if notFound == 'Error':
        errorText = str(driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblErrMessage').text)
        securityQuestion = str(driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1').text)
        return 1, [errorText, securityQuestion]

    print('Password Page')

    #Submit
    WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_PasswordView_tbxPassword'))
    driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_PasswordView_tbxPassword').send_keys(password)
    driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_PasswordView_btnSubmit').click()


    # Get partner info
    WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element(By.ID, 'ctl00_ctl40_g_151d28df_c666_4083_8cb8_34a60bc8b6dd_lbUserJobTitle'))
    position = driver.find_element(By.ID, 'ctl00_ctl40_g_151d28df_c666_4083_8cb8_34a60bc8b6dd_lbUserJobTitle').text
    store = driver.find_element(By.ID, 'ctl00_ctl40_g_151d28df_c666_4083_8cb8_34a60bc8b6dd_lbUserDepartment').text
    store = store[store.find(' ') + 1:]

    driver.quit()
    return {
        'position': position,
        'store': store,
    }


def get_sq(numbers):

    questions = []

    driver = get_driver()
    timeoutTime = 30

    while len(questions) < 2:
        driver.get('https://mysite.starbucks.com/Person.aspx')

        WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element_by_id('ContentPlaceHolder1_MFALoginControl1_UserIDView_txtUserid'))
        driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_txtUserid').send_keys(numbers)
        driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_btnSubmit').click()

        timeout = datetime.now() + timedelta(seconds = timeoutTime)
        notFound = 0
        while notFound == 0 and datetime.now() < timeout:
            try:
                driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_lblErrMessage')
                notFound = 'Error'
            except Exception:
                print('No error')
            try:
                driver.find_element(By.ID, 'lnkbtnRetailKBA')
                notFound = 'SSO'
            except Exception:
                print('No SSO')
            try:
                driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1')
                notFound = 'Security'
            except Exception:
                print('No security')

        if notFound == 0 and dateTime.now() >= timeout:
            return 1, 'No SSO, Security Question, or Error'

        if notFound == 'Error':
            errorText = str(driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_UserIDView_lblErrMessage').text)
            return 1, errorText

        if notFound == 'SSO':
            WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element(By.ID, 'lnkbtnRetailKBA'))
            driver.find_element(By.ID, 'lnkbtnRetailKBA').click()


        print('Security Question')
        WebDriverWait(driver, timeoutTime).until(lambda d: d.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1'))
        securityQuestion = str(driver.find_element(By.ID, 'ContentPlaceHolder1_MFALoginControl1_KBARegistrationView_lblKBQ1').text)
        if securityQuestion not in questions:
            questions.append(securityQuestion)

    driver.quit()
    return questions


def get_driver():
    ser = 'chromedriver'
    op = Options()
    op.add_experimental_option('detach', True)
    op.add_argument("--no-sandbox")
    op.add_argument("--headless")
    op.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path = ser, options = op)
    driver.set_window_size(1920, 1080)

    return driver


if __name__ == '__main__':
    main()

    # Post270Img7.jpg