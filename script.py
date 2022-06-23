import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

i=True

chrome_driver_path="/Users/lirajkhanna/Desktop/clutch/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("https://clutch.co/")
driver.maximize_window()
driver.find_element_by_id("CybotCookiebotDialogBodyButtonAccept").click()
time.sleep(1)

def fetch_data(firm):
  data=[]
  try:
    heading = driver.find_element_by_css_selector("h1 > .website-link__item")
    data.append(heading.text)
    data.append(heading.get_attribute("href"))
    data.append(driver.find_element_by_class_name("location-name").text)
    data.append(driver.find_element_by_class_name("phone_icon").text)
    data.append(driver.find_element_by_css_selector("span.rating:nth-child(2)").text)
    data.append(driver.find_element_by_css_selector("a.reviews-link:nth-child(5) > span:nth-child(1)").text+" Reviews")
    data.append(driver.find_element_by_css_selector("div.list-item:nth-child(2) > span:nth-child(2)").text)
    data.append(driver.find_element_by_css_selector("div.list-item:nth-child(1) > span:nth-child(2)").text)
    data.append(driver.find_element_by_css_selector("div.list-item:nth-child(3) > span:nth-child(2)").text)
    return data
  except NoSuchElementException:
    return None
    
  

with open('firms.csv', 'w', encoding='UTF8') as f:
  writer = csv.writer(f)
  writer.writerow(["Company",	"Website",	"Location",	"Contact",	"Rating",	"Review Count",	"Hourly Rate",	"Min Project Size",	"Employee Size"])

  driver.find_element_by_class_name("sitemap-nav__item").click()
  time.sleep(1)

  while True:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0)")
    time.sleep(1)

    if i==True:
      driver.find_element_by_class_name("slideInCta-close").click()
      i=False


    firms_list = driver.find_elements_by_class_name("website-profile")

    for firm in firms_list:
      driver.execute_script("window.scrollBy(0,300)")
      firm.click()

      try:
        parent = driver.window_handles[0]
        chld = driver.window_handles[1]
        driver.switch_to.window(chld)

        data = fetch_data(firm)
        if data!=None:
          writer.writerow(data)

        driver.close()
        driver.switch_to.window(parent)
      except IndexError:
        continue


    driver.execute_script("window.scrollBy(0,250)")
    time.sleep(3)

    next=driver.find_elements_by_css_selector(".next > .page-link")
    if len(next)>0:
      next[0].click()
    else:
      break

driver.quit()


