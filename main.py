from selenium import webdriver
import time
from bs4 import BeautifulSoup

# Module for Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ActionChain
from selenium.webdriver.common.action_chains import ActionChains

from Credential import ecampusID,ecampusPW

mainPage = 'http://ecampus.konkuk.ac.kr'
loginPage = 'http://ecampus.konkuk.ac.kr/ilos/main/member/login_form.acl'

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

driver = webdriver.Chrome("driver/chromedriver")
driver.get(loginPage)

campusId = driver.find_element_by_id('usr_id')
campusId.send_keys(ecampusID)
time.sleep(0.5)
passwordInput = driver.find_element_by_id('usr_pwd')
passwordInput.send_keys([ecampusPW])
time.sleep(0.5)
signInButton = driver.find_element_by_id('login_btn').click()
#_______________________________________________________________________________________________________________________
#Get today subject

# 수강중인 과목들 로딩이 다 될때까지 대기
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'em')))

# 1학기 수업을 포함한 비정규과목, 강의 과목이 `sub_open` 클래스에 포함됨.
classes = driver.find_elements_by_css_selector(".m-box2 .sub_open")

# 정규과목만 솎아내기
lecture_cnt = 0

print("\n-------------------수강중인 과목\n")

for i in range(len(classes)):
    contentText = classes[i].text
    # 비정규,강의 과목의 경우 `[건국대]` 로 강의명 표시.  
    if (contentText.find("[서울]") != -1):
        print(contentText)
        lecture_cnt += 1

print("\n------------------------------")
#_______________________________________________________________________________________________________________________

finishedLecture = []
unfinishedLecture = []

for i in range(lecture_cnt):
    # 완료,미완료 강의목록 배열에 저장
    # 페이지 리로딩되면서 강의실로 이동하는 링크의 auth가 계속 바뀌므로 메인 페이지로 복귀시 링크정보 다시 받아옴
    # 페이지 content 로딩 기다리기

    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'em')))

    classes = driver.find_elements_by_class_name("sub_open")
    contentText = classes[i].text

    # 수강과목 마우스 hover 시 class 이름이 `sub_open site-font-color` 로 바뀌면서 강의실로 가는 링크 활성화
    # Action chain을 통해 1. 마우스 올리기 2.클릭 해서 이동
    hover = ActionChains(driver).move_to_element(classes[i]).click()
    hover.perform()

    # 좌측 메뉴의 `온라인 강의` 탭으로 이동
    # content 로딩 대기
    lecture_menu = wait.until(EC.element_to_be_clickable((By.ID, 'st_lecture2')))
    lecture_menu.click()
    time.sleep(1)

    # 아직까지 강의를 하나도 안올린 과목이 있어서 분기처리
    if(driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]").text=="조회할 자료가 없습니다"):
        print("조회할 강의가 없습니다\n")
    else:
        currentWeek = driver.find_element_by_css_selector(".ibox3.wb.wb-on.wb-choice .wb-week").text
        lectureWrapper = driver.find_elements_by_class_name("lecture-box")
        print(f"현재 {contentText}과목의 {currentWeek}차 까지 강의를 완료했습니다.\n\
{currentWeek}차의 강의 개수는 {len(lectureWrapper)}개 이며")
        
# /html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[1]/ol/li[1]/div[2]
# /html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[1]/ol/li[5]/div/div[1]/div[1]/div/span
# /html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[1]/ol/li[5]/div/div[2]/div[1]/div/span

# 이 xpath의 자식들이 차시 카테고리의 자식 영상들 /html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div/div/ul/li[1]/ol/li[5]/div/div[1]
# n차시: //*[@id="lecture-n"]/div/ul/li[1]/ol/li[5]/div/div[1]/div[2]/div[3]

        for i in range(len(lectureWrapper)):
            timeStat = driver.find_element_by_xpath('//*[@id="lecture-1"]/div/ul/li[1]/ol/li[5]/div/div/div[2]/div[3]').text.split('/')
            lectureName = driver.find_element_by_xpath(f"/html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div[{i+1}]/div/ul/li[1]/ol/li[1]/div[2]").text
            print(f"{i+1}번째 강의인 {lectureName} 의 수강을", end=' ')
            if(timeStat[0] >= timeStat[2]):
                 print("마쳤습니다")
            else:
                print("마치지 못했습니다.")
                print(f"남은 시간: {timeStat[2]}")
    print("")
    driver.get(mainPage)



# /html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div/div[1]/div



# /html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/ul/li[1]/ol/li[5]/div/div/div[2]/div[3]


