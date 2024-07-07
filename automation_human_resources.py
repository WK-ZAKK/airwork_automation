import os
import re
import sys
import json
import pandas as pd
import subprocess
from retry import retry
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from logging import getLogger
from selenium.webdriver.chrome.service import Service


def get_webdriver():
    """自動でWebdriverをダウンロードしてSeleniumを起動

    Returns:
        _type_: _description_
    """
    driver_path = ChromeDriverManager().install()
    print(driver_path)
    driver = webdriver.Chrome(service=Service(executable_path=driver_path))
    return driver


def click_xpath(driver, xpath):
    sleep(.5)
    driver.find_element("xpath", xpath).click()


def send_xpath(driver, xpath, send_value):
    driver.find_element("xpath", xpath).send_keys(send_value)


def field_clear(driver, xpath):
    driver.find_element("xpath", xpath).clear()


def get_laps(driver):
    click_xpath(driver, "/html/body/div[1]/div/main/div[1]/div[3]/table/tbody/tr[1]/td[6]/a[2]")
    click_xpath(driver, "/html/body/div[1]/div/main/div[1]/div/div[2]/form/table[1]/tbody/tr[1]/td/span[2]")
    # 勤務地選択の際に、勤務地がいくつあるのかliタグの数を数えて確認する。
    ul_element = driver.find_element("xpath", "/html/body/div[1]/div/main/div[2]/div/div/div/ul")
    # ul要素内の全てのli要素を取得
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    # li要素の数を取得
    li_count = len(li_elements)

    click_xpath(driver, "/html/body/div[1]/div/main/div[2]/div/footer/div/a[1]")
    click_xpath(driver, "/html/body/div[1]/div/main/fieldset/div/a")

    # 2秒待つ
    sleep(2)


    try:
        # アラートが表示されていればOKボタンをクリック
        Alert(driver).accept()
    except NoAlertPresentException:
        # アラートが表示されていなければ何もしない
        pass

    return li_count


def copy_to_application(driver, application_xpath, li_count):
    """
    求人管理ページに挙げられている'作成中'の応募書類をコピーして作成する関数。
    引き数に「コピー」ボタンのxpathを指定する。
    """
    i = 0
    for i in range(li_count - 1):

        # 対象の応募をコピー。
        element = driver.find_element("xpath", application_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        click_xpath(driver, application_xpath)
        print('コピーボタンをクリック')
        i = i + 1

        click_xpath(driver, "/html/body/div[1]/div/main/div[1]/div/div[2]/form/table[1]/tbody/tr[1]/td/span[2]")
        # 要素を取得
        element = driver.find_element("xpath", f"/html/body/div[1]/div/main/div[2]/div/div/div/ul/li[{i}]/label/div/p/span[1]")
        # 要素のテキストを取得
        element_text = element.text
        if '株式会社Faitria マニュファクチャリング採用部' in element_text:
            print('株式会社Faitria マニュファクチャリング採用部だったので掲載しませんでした')
            break

        sleep(1)
        element = driver.find_element("xpath", f'/html/body/div[1]/div/main/div[2]/div/div/div/ul/li[{i}]/label/div')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        click_xpath(driver, f'/html/body/div[1]/div/main/div[2]/div/div/div/ul/li[{i}]/label/div')
        sleep(1)
        click_xpath(driver, "/html/body/div[1]/div/main/div[2]/div/footer/div/a[2]")
        sleep(1)
        # field_clear(driver, '/html/body/div[1]/div/main/div[1]/div/div[2]/form/div[4]/table/tbody/tr[1]/td/div[3]/span[3]/span[2]/input')
        # sleep(1)
        # lower_limit = 255000
        # send_xpath(driver, '/html/body/div[1]/div/main/div[1]/div/div[2]/form/div[4]/table/tbody/tr[1]/td/div[3]/span[3]/span[2]/input', lower_limit)
        sleep(1)
        click_xpath(driver, '/html/body/div[1]/div/main/fieldset/div/button[2]')
        sleep(1)
        click_xpath(driver, '/html/body/div[1]/div/main/div[3]/div/button[4]/label/a')
        print('掲載するボタンクリック')
        sleep(1)
        click_xpath(driver, '/html/body/div[2]/div/div[2]/div/button[2]')
        print('掲載を確認')

# LOGの設定
logger = getLogger()
logger.info("Process Start")


try:
    # アカウント情報の取得
    acc_id = "faitria.seizou.info4@gmail.com"
    # acc_id = "seizou.job.time@gmail.com"
    acc_pass = "fait0601!"


    driver = get_webdriver()

    driver.get('https://ats.joboplite.jp/')
    driver.maximize_window()
    driver.implicitly_wait(10)
    print('open webpage')
    # driver.find_element("xpath", '/html/body/header/div[2]/div/div[2]/ul/li[1]/a').click()
    click_xpath(driver, '/html/body/div[1]/header/div[2]/div/div/div[2]/div[1]/a[1]')
    # login page
    sleep(2)
    click_xpath(driver, '/html/body/div/div/main/div/div[3]/div[1]/div/a')
    driver.find_element("xpath", '//*[@id="form"]/dl[1]/dd/span/input').send_keys(acc_id)
    sleep(0.5)
    driver.find_element("xpath", '//*[@id="form"]/dl[2]/dd/span/input').send_keys(acc_pass)
    driver.implicitly_wait(10)
    sleep(2)
    click_xpath(driver, '//*[@id="submit_btn"]')
    print('login')

    sleep(3)
    click_xpath(driver, '/html/body/div[1]/div/nav/ul/li[3]')
    print('求人管理ページ')

    li_count = get_laps(driver)

    count = 0
    i = 1

    while True:
        try:
            element = driver.find_element("xpath", f"/html/body/div[1]/div/main/div[1]/div[3]/table/tbody/tr[{i}]/th/div/p")
            print(element.text)
            if element.text == "作成中":
                count += 1
            else:
                print('テンプレート数: ' + str(count))
                break
        except Exception as e:
            print(e)
            break
        i += 1
    # 本来は作成中となっている募集の数を数えて、その回数分、copy_to_application関数を回す。
    for c in range(count):
        application_xpath = f'/html/body/div[1]/div/main/div[1]/div[3]/table/tbody/tr[{c + 1}]/td[6]/a[2]'
        copy_to_application(driver, application_xpath, li_count)
    print('登録終了')

except Exception as e:
    print(e)
    driver.quit()
sleep(2)
driver.quit()