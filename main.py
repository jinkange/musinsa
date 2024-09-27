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
  one_week_ago = current_date + timedelta(weeks=4)
  # Check if the input date is within the last week
  return current_date <= input_date <= one_week_ago

def chromeStart():
  try:
    # 크롬드라이버 옵션 설정
    with open("./data/chrome.txt", "r+",encoding='utf-8') as chrome_dir:
      chrome = chrome_dir.readlines()
    with open("./data/number.txt", "r+",encoding='utf-8') as number_dir:
      number = number_dir.readlines()
    if(chrome == ''):
      print("./data/chrome.txt 에 크롬의 위치를 입력 해주세요.")
    if(number == ''):
      print("./data/number.txt 에 숫자를 입력 해주세요.")
    options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)
    
    driver = webdriver.Chrome()
    return driver
  except Exception as e:
    print(e)
    input("아무키나 누르세요... ")

def htmlLoadingCheck(driver:webdriver, xpath):
  while 1:
    try:
      driver.execute_script("document.evaluate('"+xpath+"', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
      return
    except:
      time.sleep(0.1)
      try:
        driver.execute_script("document.evaluate('//*[@id=\"lastName\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")    
        return 1
      except:
        print()
def wait_and_click_quick_pay_button(driver:webdriver, xpath):
  while True:  # 무한 루프
    try:
      # 버튼이 나타날 때까지 기다림
      quick_pay_button = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, xpath))
      )
      # 버튼 클릭
      quick_pay_button.click()
      print(xpath + "버튼을 클릭했습니다.")
      break  # 클릭 후 루프 종료
    except Exception as e:
      print(xpath + "버튼이 아직 나타나지 않았습니다. 다시 시도합니다...")
      # 예외 발생 시 잠시 대기 후 재시도
      time.sleep(1)  
def click(driver:webdriver, xpath):
  try:
    # 버튼이 나타날 때까지 기다림
    quick_pay_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, xpath))
    )
    # 버튼 클릭
    quick_pay_button.click()
    print(xpath + "버튼을 클릭했습니다.")
  except Exception as e:
    print(xpath + "버튼이 아직 나타나지 않았습니다. 다시 시도합니다...")

def start():
  with open("./data/password.txt", "r", encoding='utf-8') as password_file:
    password_str = password_file.readline().strip()
  print("페이 비밀번호 :  ",password_str)
  while True:
    goodUrl = input("구매할 무신사 주소 : ")
    if goodUrl:
          print("주소 : ",goodUrl)
          break
  # while True:
  #   size = input("구매할 사이즈(미입력시 랜덤 선택) : ")
  #   # 입력값이 비어있거나 숫자로 이루어져 있는지 확인
  #   if size == '' or size.isnumeric():
  #     break
  #   else:
  #     print("Invalid input. Please enter a number or leave it blank.")

  driver = chromeStart()
  #옵션값 확인 및 선택
  driver.get("https://www.musinsa.com/auth/login")
  print("로그인을 진행 해주세요.")
  # 로그인이 되길 기다려줘야하는데....
  #상품 주소일때 로그인 값이 없다면 그때 작동하도록
  while 1:
    if(driver.current_url in "https://www.musinsa.com/auth/login"):
      time.sleep(0.1)
    else:
      break
  driver.get(goodUrl)
  driver.execute_script("window.scrollBy(0, 1000);")  # 500px 만큼 내리기
  print("품절 체크")  
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '품절')]")
        driver.refresh()
        time.sleep(5)
      except:
        break
  print("판매 예정 체크")  
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '판매 예정')]")
        driver.refresh()
        time.sleep(5)
      except:
        break

  try:
    # 구매하기
    # 옵션 선택 단어 클릭  //*[@id="root"]/div[1]/div[19]/div[2]/div[1]/div/div
    wait_and_click_quick_pay_button(driver, '//button[span[text()="구매하기"]]')
    try:
      option_select_div = driver.find_element(By.XPATH, '//input[@placeholder="옵션 선택"]')
      input_count = len(option_inputs)
      if(input_count != 0):
        for index, input_field in enumerate(option_inputs):
          wait_and_click_quick_pay_button(driver, '//input[@placeholder="옵션 선택"]')
          # 약간의 대기 (로딩 시간 고려)
          time.sleep(1)
          # '옵션 선택'의 두 번째 상위 div에서 첫 번째 요소 제외한 나머지 요소 선택
          parent_div = option_select_div.find_element(By.XPATH, '../..')  # 두 번째 상위 div로 이동
          dropdown_items = parent_div.find_elements(By.XPATH, './div[position()>1]')  # 첫 번째 요소 제외
          # 나머지 요소 중 랜덤 선택
          random_choice = random.choice(dropdown_items)
          random_choice.click()
    except:
      print("옵션없음")
    wait_and_click_quick_pay_button(driver, '')
    #https://www.musinsa.com/products/672867 프리 테스트
    #https://www.musinsa.com/products/4311482 옵션 n개

    

    # CSS 선택자를 사용하여 "원 결제하기" 버튼 클릭
    payment_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-button-name="결제하기"]'))
    )
    payment_button.click()  # 버튼 클릭
    
    click(driver, '//*[contains(text(), "바로 구매하기")]')
    #새창 대기
    current_window = driver.current_window_handle
    # 새로운 창 핸들 찾기
    new_window = None
    while not new_window:
      for window_handle in driver.window_handles:
        if window_handle != current_window:
          new_window = window_handle
          driver.switch_to.window(window_handle)
          time.sleep(0.3)
          current_url = driver.current_url
          print("새창 찾기 창 주소: " + driver.current_url)
          if "https://pay.musinsa.com/certify/req"  in current_url:
            print("찾는 주소가 열린 창입니다.")
            break
          driver.switch_to.window(new_window)
          time.sleep(0.3)
      iFrame = WebDriverWait(driver, 99).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__tosspayments_brandpay_iframe__"]')))
      driver.switch_to.frame(iFrame)
      while 1:
        try:
          # html 로딩 대기
          goods = WebDriverWait(driver, 99).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="brandpay-portal-container"]/div/div/a[2]')))
          if(goods):
            break
        except:
          time.sleep(1)
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
          break
        else:
          print("새 창이 아직 열려 있습니다.")
          goods = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[1]/span[2]')))
          if(goods):
            print("비번틀림")
            break
      except Exception as e:
        print(e)
    time.sleep(60)
  except Exception as e:
    print(e)
    
start()