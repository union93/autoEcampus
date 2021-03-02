from selenium import webdriver
import time
from bs4 import BeautifulSoup

from Credential import ecampusID,ecampusPW


todaySubjectList0 = []
todaySubjectList1 = []
#_______________________________________________________________________________________________________________________
#LoginPart
#Your ID,PW should located in Credential
"""
#HEADLESS OPTION, Only for lazy student 
option = webdriver.ChromeOptions()
option.headless = True
driver = webdriver.Chrome('chromedriver',options=option)
"""

driver = webdriver.Chrome()
driver.get('https://ecampus.konkuk.ac.kr/ilos/main/member/login_form.acl')

driver.implicitly_wait(3)
campusId = driver.find_element_by_id('usr_id')
campusId.send_keys(ecampusID)
time.sleep(1)
passwordInput = driver.find_element_by_id('usr_pwd')
passwordInput.send_keys([ecampusPW])
time.sleep(1)
signInButton = driver.find_element_by_id('login_btn').click()
driver.implicitly_wait(5)
#_______________________________________________________________________________________________________________________
#Get today subject

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
todaySubject = soup.select('td.subject')

for list in todaySubject:
    todaySubjectList0.append(list.get_text())
for v in todaySubjectList0:
    if v not in todaySubjectList1:
        todaySubjectList1.append(v)
#_______________________________________________________________________________________________________________________















