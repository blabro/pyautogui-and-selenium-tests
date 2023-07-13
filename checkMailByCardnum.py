import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# Using Chrome to access web
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()

#take all mails from file mails.txt
f = open("mails.txt", "r")
mailName = ''
if f.mode == "r":
    mailName = f.read()

mailName = mailName.split('\n')

# Open the website
driver.get('https://rewards.heathrow.com/cc/login.do')
delay = 3
try:
    myPage = WebDriverWait(driver, delay)
    print("Loading in time OK")
except TimeoutException:
    print("Loading too long")

pyautogui.typewrite('bbroncel', interval=0.01)
pyautogui.typewrite(['tab'])
pyautogui.typewrite(                                                                                                                                                                                                                                                                                                 'secretpassword!')
pyautogui.hotkey('enter')
time.sleep(6)


#mmailName.splitlines()
LHRusers = ''
for x in mailName:
    driver.find_element_by_id('button-1011').click()
    driver.find_element_by_xpath('// *[ @ id = "findData_cardDisplayNumber-inputEl"]').send_keys(str(x))
    #driver.find_element_by_xpath('//*[@id="findData_email-inputEl"]').send_keys(str(x))
    time.sleep(0.1)
    driver.find_element_by_id('button-1010-btnInnerEl').click()
    time.sleep(1.5)
    if driver.find_elements_by_xpath('//*[@id="gridview-1037"]/table/tbody/tr[2]/td[3]/div/span/div'):
        #pyautogui.keyDown('ctrl')
        element = driver.find_element_by_id('accountBasicSearchResults-body')
        attrs = driver.execute_script(
            'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
            element)
        memberInfo = element.text
        #print(element.text)
        line = x + ' ' + memberInfo.splitlines()[2]
        print(line)
        #print(driver.find_element_by_xpath('//*[@id="gridview-1037"]/table/tbody/tr[2]').get_property('text'))
        #pyautogui.keyUp('ctrl')
        LHRusers = LHRusers + line + '\n'
    else: LHRusers = LHRusers + x + ' n/a\n'

outputFile = open("mailsAfter.txt", "w")
outputFile.write(LHRusers)
#print(LHRusers)

#while(True):
    #time.sleep(2)
    #pyautogui.moveTo(pyautogui.position().x+2, pyautogui.position().y, 1)
