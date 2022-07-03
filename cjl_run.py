from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
import time

def get_posts():
    conn = pymysql.connect(host='192.168.15.84', port=3306, user='remote', passwd='00000000', db='jsb')
    cur = conn.cursor()

    driver = webdriver.Chrome()
    driver.get('https://cryptojobslist.com/?sort=recent')

    xp = '//*[@id="__next"]/div[1]/div[6]/div'
    el = driver.find_elements(By.XPATH, xp)

    print("Starting.... If there's anything new, this will be added to DB")

    db_siz_st = len(el)

    db_sz_now = 0

    ln = 0
    add_tt = 0

    for i in el:
        try:
            ln += 1
            lk = i.find_element(By.TAG_NAME, 'a')
            txt = i.get_attribute('title')
            lks = lk.get_attribute('href').title()
            dt = [(txt),(lks)]
            ce = "INSERT INTO list(title, link) VALUES(%s, %s)"
            cur.execute(ce, dt)
            conn.commit()
            print("Added: ")
            print(str(ln) + ") " + str(txt) + " -> " + str(lks) + "\n")
        except:
            ln += 1
            lk = i.find_element(By.TAG_NAME, 'a')
            txt = i.get_attribute('title')
            lks = lk.get_attribute('href').title()
            pass

    conn.close()
    driver.close()



def time_to_run():
    while True:
        try:
            print("Running now....")
            print("'CTRL' + 'C' to leave")
            get_posts()
            #RUN EVERY 4 HOURS
            time.sleep(14400)
        except:
            pass


time_to_run()
