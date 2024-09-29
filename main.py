import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
import subprocess
import time
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import random
import time
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import re
goodUrl = ""
password_str = ""
pw = ""
id = ""
def click_number_keypad(driver, number):
  script = f"""
    var keypadElement = document.querySelector("#brandpay-portal-container > div > div");
    var numberButtons = keypadElement.querySelectorAll("a[aria-label='가상키패드-{number}']");
    if (numberButtons.length > 0) {{
      var randomNumberButton = numberButtons[Math.floor(Math.random() * numberButtons.length)];
      randomNumberButton.dispatchEvent(new MouseEvent('mouseup', {{
        bubbles: true,
        cancelable: true,
        view: window
    }}));
  }}
  """
  driver.execute_script(script)
  
def is_within_last_week(date_string):
  # Convert the input date string to a datetime object
  input_date = datetime.strptime(date_string, "%Y-%m-%d")
  # Get the current date
  current_date = datetime.now()
  # Calculate the date one week ago from the current date
  one_week_ago = current_date + timedelta(weeks=2)
  # Check if the input date is within the last week
  return current_date <= input_date <= one_week_ago

def chromeStart():
  try:
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(options=options)
    
    driver = webdriver.Chrome()
    return driver
  except Exception as e:
    print(e)
    input("아무키나 누르세요... ")


def find_button_by_xpath(driver: webdriver, xpath: str) -> bool:
    try:
        # XPATH를 사용하여 버튼을 찾음
        driver.find_element(By.XPATH, xpath)
        return True  # 성공적으로 클릭했을 경우 True 반환
    except:
        return False  # 버튼을 못찾으면 False 반환
      
def wait_and_click_quick_pay_button(driver:webdriver, xpath) -> bool:
    try:
      # 버튼이 나타날 때까지 기다림
      quick_pay_button = driver.find_element(By.XPATH, xpath)
      # 버튼 클릭
      quick_pay_button.click()
      print(xpath + "버튼을 클릭했습니다.")
      return True 
    except:
      return False

def click(driver:webdriver, xpath):
  try:
    # 버튼이 나타날 때까지 기다림
    quick_pay_button =  driver.find_element(By.XPATH, xpath)
    # 버튼 클릭
    quick_pay_button.click()
    print(xpath + "버튼을 클릭했습니다.")
  except:
    print(xpath + "버튼이 아직 나타나지 않았습니다. 다시 시도합니다...")
    
def sellout_check(driver:webdriver):
  global goodUrl
  if(driver.current_url in goodUrl):
    try:
      # 해당 요소의 텍스트 가져오기
      driver.execute_script("document.body.style.zoom='10%'")
      driver.find_element(By.XPATH, "//*[contains(text(), '품절')]")
      try:
        # 10초 내로 페이지가 새로고침되길 기다림
        WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # 새로고침
        driver.refresh()
      except:
        print("새로고침이 너무 오래 걸립니다. 다른 방법으로 새로고침 시도.")
        driver.get(driver.current_url)
        time.sleep(5)
    except:
      goodUrl
      
def sell_plan(driver:webdriver):
  global goodUrl
  if(driver.current_url in goodUrl):
    try:
      # 해당 요소의 텍스트 가져오기
      driver.execute_script("document.body.style.zoom='10%'")
      driver.find_element(By.XPATH, "//*[contains(text(), '판매 예정')]")
      try:
        # 10초 내로 페이지가 새로고침되길 기다림
        WebDriverWait(driver, 5).until(
          EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        # 새로고침
        driver.refresh()
      except:
        print("새로고침이 너무 오래 걸립니다. 다른 방법으로 새로고침 시도.")
        driver.get(driver.current_url)
      time.sleep(5)
    except:
      goodUrl
def toss_payment(driver:webdriver):
  global password_str
  #새창 대기
  current_window = driver.current_window_handle
  # 새로운 창 핸들 찾기
  
  new_window = None
  if(len(driver.window_handles) <= 1):
    return
  
  for window_handle in driver.window_handles:
    if window_handle != current_window:
      new_window = window_handle
      driver.switch_to.window(new_window)
      current_url = driver.current_url
      if "pay.musinsapayments.com"  in current_url:
        driver.switch_to.window(new_window)
      else:
        driver.switch_to.window(current_window)
        return
  iFrame = WebDriverWait(driver, 99).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__tosspayments_brandpay_iframe__"]')))
  driver.switch_to.frame(iFrame)
  while 1:
    try:
      # html 로딩 대기
      goods = WebDriverWait(driver, 99).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="brandpay-portal-container"]/div/div/a[2]')))
      if(goods):
        break
    except:
      goodUrl
  script = """
      var keypadElement = document.querySelector("#brandpay-portal-container > div > div");
      return keypadElement.querySelectorAll("a");
  """
  a_elements = driver.execute_script(script)
  while 1:
    try:
      for password in password_str:  
        for a_element in a_elements:
          virtual_keypad_value = a_element.get_attribute("aria-label").replace("가상키패드-","")
          if(password == a_element.text):
            print(password)
            click_number_keypad(driver, virtual_keypad_value)
            break
      #창이 닫혔는지
      new_window_still_open = False
      for window_handle in driver.window_handles:
        if window_handle != current_window:
          new_window_still_open = True
          break
      #안닫혔으면 비번일 틀린건
      if not new_window_still_open:
        print("새 창이 닫혔습니다.")
        input("아무키나 누르세요... ")
        break
      else:
        print("새 창이 아직 열려 있습니다.")
        goods = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[1]/span[2]')))
        if(goods):
          print("비번틀림")
          break
    except Exception as e:
      print(e)
      input("아무키나 누르세요... ")
      break
def one_payment(driver: webdriver) -> bool:
  try:
    # CSS_SELECTOR를 사용하여 버튼 찾기
    button = driver.find_element(By.CSS_SELECTOR, 'button[data-button-name="결제하기"]')
    # 버튼 클릭 시도
    button.click()
    return True  # 클릭 성공 시 True 반환
  except:
    return False  # 버튼을 찾지 못했을 때 False 반환
    
def init():
  global goodUrl
  global password_str
  with open("./data/password.txt", "r", encoding='utf-8') as password_file:
    password_str = password_file.readline().strip()
  print("페이 비밀번호 :  ",password_str)
  while True:
    goodUrl = input("구매할 무신사 주소 : ")
    if goodUrl:
      print("주소 : ",goodUrl)
      break
  # id = input("무신사 아이디 : ")
  # pw = input("무신사 비밀번호 : ")
def login(driver:webdriver):
  global goodUrl
  global id
  global pw
  driver.get("https://www.musinsa.com/auth/login")
  # input_field = driver.find_element(By.CSS_SELECTOR, 'input[title="아이디 입력"]')
  # input_field.send_keys(id)
  # input_field = driver.find_element(By.CSS_SELECTOR, 'input[title="비밀번호 입력"]')
  # input_field.send_keys(pw)
  # driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
  while 1:
    if(driver.current_url in "https://www.musinsa.com/auth/login"):
      time.sleep(1)
    else:
      break
  driver.get(goodUrl)
  driver.execute_script("document.body.style.zoom='10%'")
def click_buy(driver:webdriver):
  if((find_button_by_xpath(driver,  '//button[span[text()="구매하기"]]') == True and
     find_button_by_xpath(driver, '//input[@placeholder="옵션 선택"]') == False and
     find_button_by_xpath(driver, '//button[span[text()=" 빠른결제"]]') == False) or
     (find_button_by_xpath(driver,  '//button[span[text()="구매하기"]]') == True and
     find_button_by_xpath(driver, '//span[contains(text(), "FREE")]') == False and
     find_button_by_xpath(driver, '//button[span[text()=" 빠른결제"]]') == False)):
    wait_and_click_quick_pay_button(driver, '//button[span[text()="구매하기"]]')
    
    try:
      option_select_div = driver.find_elements(By.XPATH, '//input[@placeholder="옵션 선택"]')
      input_count = len(option_select_div)
      print(input_count)
      if(input_count == 0):
        return
      for index, input_field in enumerate(option_select_div):
        wait_and_click_quick_pay_button(driver, '//input[@placeholder="옵션 선택"]')
        # 약간의 대기 (로딩 시간 고려)
        # '옵션 선택'의 두 번째 상위 div에서 첫 번째 요소 제외한 나머지 요소 선택
        parent_div = input_field.find_element(By.XPATH, '../..')  # 두 번째 상위 div로 이동
        dropdown_items = parent_div.find_elements(By.XPATH, './div[position()>1]')  # 첫 번째 요소 제외
        # 나머지 요소 중 랜덤 선택
        random_choice = random.choice(dropdown_items)
        random_choice.click()
    except Exception:
      print("옵션없음")
      #https://www.musinsa.com/products/672867 프리 테스트
      #https://www.musinsa.com/products/4311482 옵션 n개
def click_fast(driver:webdriver):
  
  wait_and_click_quick_pay_button(driver, '//button[span[text()=" 빠른결제"]]')
  wait_and_click_quick_pay_button(driver, '//*[contains(text(), "바로 구매하기")]')
  
def start():
  init()
  driver = chromeStart()
  login(driver)
  while True:
    toss_payment(driver)
    one_payment(driver)
    click_fast(driver)
    click_buy(driver)
    sell_plan(driver)
    sellout_check(driver)
    
    
    
    

start()


