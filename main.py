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
        #options = webdriver.ChromeOptions()
        options = Options()
        #options.add_argument("--disable-blink-features=AutomationControlled")

          
        with open("./data/chrome.txt", "r+",encoding='utf-8') as chrome_dir:
          chrome = chrome_dir.readlines()
        with open("./data/number.txt", "r+",encoding='utf-8') as number_dir:
          number = number_dir.readlines()
          
        userCookieDir = os.path.abspath(f"./cookie")
        if os.path.exists(userCookieDir) == False:
          os.mkdir(userCookieDir)
          
        # userCookieDir = os.path.abspath(f"./cookie/{number[0]}")
        # if os.path.exists(userCookieDir) == False:
        #     os.mkdir(userCookieDir)
            
        if(chrome == ''):
          print("./data/chrome.txt 에 크롬의 위치를 입력 해주세요.")
          
        if(number == ''):
          print("./data/number.txt 에 숫자를 입력 해주세요.")
          
        #chrome_cmd = '\"'+chrome[0]+'\" --headless --remote-debugging-port=922'+str(number[0])+'  --user-data-dir="'+str(userCookieDir)+'" --disable-gpu --disable-popup-blocking --disable-dev-shm-usage --disable-plugins --disable-background-networking'
        chrome_cmd = '\"'+chrome[0]+'\" --user-data-dir="'+str(userCookieDir)+'" --disable-gpu --disable-popup-blocking --disable-dev-shm-usage --disable-plugins --disable-background-networking'
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:922"+str(number[0]))
        #p = subprocess.Popen(chrome_cmd, shell=True)

        release = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        # 버전명을 가져옵니다.
        version = requests.get(release).text
        driver = webdriver.Chrome(options=options)
        
        
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
            time.sleep(1)
            try:
                driver.execute_script("document.evaluate('//*[@id=\"lastName\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")    
                return 1
            except:
                print()
                
def start():
  with open("./data/password.txt", "r", encoding='utf-8') as password_file:
    password_str = password_file.readline().strip()
  
  print("페이 비밀번호 :  ",password_str)
  
  while True:
    goodUrl = input("구매할 무신사 주소 : ")
    if goodUrl:
          print("주소 : ",goodUrl)
          break
        
  while True:
      size = input("구매할 사이즈(미입력시 랜덤 선택) : ")

      # 입력값이 비어있거나 숫자로 이루어져 있는지 확인
      if size == '' or size.isnumeric():
          break
      else:
          print("Invalid input. Please enter a number or leave it blank.")

  driver = chromeStart()

  #옵션값 확인 및 선택

  driver.get(goodUrl)
  print("로그인을 진행 해주세요.")
  try:
    option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="topCommonPc"]/header/div[3]/button')))
    
    option_element.click()
  except Exception:
    print("로그인 확인..")


  # 로그인이 되길 기다려줘야하는데....
  #상품 주소일때 로그인 값이 없다면 그때 작동하도록
  while 1:
    if(driver.current_url in goodUrl):
      try : 
          #element = driver.find_element(By.XPATH, '//*[@id="topCommonPc"]/header/div[4]/div[1]/a')
          element = driver.find_element(By.XPATH, '//*[@id="topCommonPc"]/header/div[3]/div[1]/a')
          
          if (element):
              #로그인되어있음
              break
      except Exception:
          print()
      time.sleep(1)
  print("로그인 확인..")
  print("품절 체크")  
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '품절 또는 판매가 중지된 상품입니다.')]")
        time.sleep(3)
        driver.refresh()
      except:
        break
  print("판매 예정 체크")  
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '판매 예정')]")
        #element = driver.find_element(By.XPATH, '//*[@id="buy_option_area"]/div[9]/div[1]/a')
        # '품절' 또는 '판매가 중지' 문구가 포함되어 있는지 확인
        time.sleep(3)
        driver.refresh()
      except:
        break

  try:
    if(size != ''):
      try:
        option_value_to_select = size
        option_element = WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, f"//option[@value='{option_value_to_select}']")))
        option_element.click()
      except:
        option_dropdown = driver.find_element(By.XPATH, "//select[@id='option1']")
        # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
        available_options = option_dropdown.find_elements(By.XPATH, "./option[not(contains(text(), '옵션 선택'))]")
        # 재입고와 관련된 옵션을 제거
        available_options = [option for option in available_options if "재입고" not in option.text]
        # 랜덤으로 옵션 선택
        selected_option = random.choice(available_options)
        selected_option.click()  
    else:
      # 옵션 선택 드롭다운을 찾음
      option_dropdown = driver.find_element(By.XPATH, "//select[@id='option1']")
      # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
      available_options = option_dropdown.find_elements(By.XPATH, "./option[not(contains(text(), '옵션 선택'))]")
      # 재입고와 관련된 옵션을 제거
      available_options = [option for option in available_options if "재입고" not in option.text]
      # 랜덤으로 옵션 선택
      selected_option = random.choice(available_options)
      selected_option.click()


      # # 옵션 리스트 가져오기
      # options_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='option1']")))
      # print(options_list)
      # # "재입고 알림 받기"가 없는 옵션들만 필터링
      # available_options = [option for option in options_list if "재입고 알림 받기" not in option.get_attribute("data-txt")]
      # if available_options:
      #   # 랜덤으로 하나의 옵션 선택
      #   selected_option = random.choice(available_options)
      #   option_value = selected_option.get_attribute("value")
      #   selected_option.click()
      # else:
      #   print("모든 옵션이 품절 상태입니다.")
  except Exception as e:
    print("옵션창을 찾을 수 없습니다.")

  try:
      buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '바로구매')]")))
      #buy_button.click()
          # Click the element using JavaScript
      driver.execute_script("arguments[0].click();", buy_button)
      try:
        # 얼럿이 표시될 때까지 대기 (10초로 설정)
        WebDriverWait(driver, 0.1).until(EC.alert_is_present())
        # 얼럿 객체 가져오기
        alert = driver.switch_to.alert
        # 얼럿 텍스트 출력 (선택사항)
        print("Alert Text:", alert.text)
        # 얼럿 확인 버튼 클릭 (선택사항)
        alert.accept()
        # 옵션 선택 드롭다운을 찾음
        option_dropdown = driver.find_element(By.XPATH, "//select[@id='option1']")
        # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
        available_options = option_dropdown.find_elements(By.XPATH, "./option[not(contains(text(), '옵션 선택'))]")
        # 재입고와 관련된 옵션을 제거
        available_options = [option for option in available_options if "재입고" not in option.text]
        # 랜덤으로 옵션 선택
        selected_option = random.choice(available_options)
        selected_option.click()
        buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '바로구매')]")))
        driver.execute_script("arguments[0].click();", buy_button)
        #buy_button.click()
      except Exception as e:
          # 얼럿이 표시되지 않은 경우 예외 처리
          print()
  except Exception as e:
      print("바로구매 버튼을 클릭하는데 실패했습니다.")
      buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="buy_option_area"]/div[7]/div[1]/a')))
      buy_button.click()
      print(str(e))


  while 1:
    try:
      # html 로딩 대기
      goods = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
      if(goods):
        break
    except:
      time.sleep(1)
  
  radio_button = driver.find_element(By.XPATH,'//*[@id="payment_btn0"]')
    # Click the radio button using JavaScript
  driver.execute_script("arguments[0].click();", radio_button)
    
  
  option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cardSwiper"]/div[2]')))
  option_element.click()
  time.sleep(0.5)
  try:
    option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheckAgree"]')))
    option_element.click()
  except:
    print()

  option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
  option_element.click()    

  try:
      # 얼럿이 표시될 때까지 대기 (10초로 설정)
      WebDriverWait(driver, 0.1).until(EC.alert_is_present())
      # 얼럿 객체 가져오기
      alert = driver.switch_to.alert
      # 얼럿 텍스트 출력 (선택사항)
      print("Alert Text:", alert.text)
      # 얼럿 확인 버튼 클릭 (선택사항)
      alert.accept()
      option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheckAgree"]')))
      option_element.click()
      option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
      option_element.click()    
  except Exception as e:
      # 얼럿이 표시되지 않은 경우 예외 처리
      print("No alert found.", str(e))


  #새창 대기
  current_window = driver.current_window_handle
  # 새로운 창 핸들 찾기
  new_window = None
  while not new_window:
      for window_handle in driver.window_handles:
          if window_handle != current_window:
              new_window = window_handle
              driver.switch_to.window(window_handle)
              time.sleep(0.5)
              current_url = driver.current_url
              print("새창 찾기 창 주소: " + driver.current_url)
              if "https://pay.musinsa.com/certify/req"  in current_url:
                  print("찾는 주소가 열린 창입니다.")
                  break
              driver.switch_to.window(new_window)
          time.sleep(0.5)

  iFrame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__tosspayments_brandpay_iframe__"]')))
  driver.switch_to.frame(iFrame)

  while 1:
    try:
      # html 로딩 대기
      goods = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="brandpay-portal-container"]/div/div/a[2]')))
      if(goods):
        break
    except:
      time.sleep(0.1)

  def click_number_keypad(driver, number):
      script = f"""
          var keypadElement = document.querySelector("#brandpay-portal-container > div > div");
          var numberButtons = keypadElement.querySelectorAll("a[data-virtual-keypad='{number}']");
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

  script = f"""
          var keypadElement = document.querySelector("#brandpay-portal-container > div > div");
          return keypadElement.querySelectorAll("a");
      """
  a_elements = driver.execute_script(script)
  #a_elements = driver.find_element(By.XPATH, '//*[@id="connectpay-portal-container"]/div/div/a')
      # a 태그의 텍스트 값 출력

  while 1:
    try:
      for password in password_str:  
        for a_element in a_elements:
          virtual_keypad_value = a_element.get_attribute("data-virtual-keypad")
          if(password == a_element.text):
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
start()
