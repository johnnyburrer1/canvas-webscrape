from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import os

# receive google username and password
username = input('Username: ')
password = getpass()

# set up geckodriver
profile = webdriver.FirefoxProfile()
profile.set_preference("permissions.default.image", 2)
driver = webdriver.Firefox(executable_path='.\\geckodriver.exe', firefox_profile=profile, service_log_path=os.devnull)

# log into canvas
driver.get('https://clever.com/oauth/authorize?channel=clever&client_id=4c63c1cf623dce82caac&confirmed=true&district_id=51e5622080da6210550053a4&redirect_uri=https%3A%2F%2Fclever.com%2Fin%2Fauth_callback&response_type=code&state=252627ce3038700819bd26675138c750527d8b2ec197603aadbb90b13ce26ef8')
driver.find_element_by_link_text('Log in with Google').click()
driver.find_element_by_xpath('//*[@id ="identifierId"]').send_keys(username)
driver.find_elements_by_xpath('//*[@id ="identifierNext"]')[0].click()
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@name='password']"))).send_keys(password)
driver.find_elements_by_xpath('//*[@id ="passwordNext"]')[0].click()
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@href="https://clever.com/oauth/authorize?channel=clever-portal&client_id=edf6b13d6c0376d46bba&confirmed=true&district_id=51e5622080da6210550053a4&redirect_uri=https%3A%2F%2Fsamlidp.clever.com%2Fsaml-canvas%2Foauth&response_type=code"]'))).click()

# navigate to quizes page
driver.switch_to.window(driver.window_handles[1])
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "195880")]/./..'))).click()
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/nav/ul/li[3]/a'))).click()

# get quiz names
quiz_names = []
for element in driver.find_elements_by_xpath('//a[contains(@title, "Quiz")]'):
    quiz_names.append(element.get_attribute('title'))

# take quizzes
for quiz_name in quiz_names:
    quiz_link = driver.find_element_by_xpath('//a[contains(@title, "' + quiz_name + '")]')
    driver.execute_script("arguments[0].scrollIntoView();", quiz_link)
    quiz_link.click()
    start_quiz_button = driver.find_element_by_id('take_quiz_link')
    if start_quiz_button.get_attribute('innerHTML') == 'Take the Quiz':
        start_quiz_button.click()
        for question in driver.find_elements_by_class_name('answers'):
            answer = question.find_elements_by_class_name('answer')[0].find_element_by_tag_name('input')
            driver.execute_script("arguments[0].scrollIntoView();", answer)
            answer.click()
        driver.find_element_by_id('submit_quiz_button').click()
        driver.back()
        driver.back()
    driver.back()