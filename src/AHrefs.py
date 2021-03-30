from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import urllib.parse

driver = webdriver.Chrome('chromedriver.exe')

driver.get("https://ahrefs.com/keywords-explorer/google/us/ideas/phraseMatch?keyword="+urllib.parse.quote("mercedes benz")+"&difficulty=Min-50")
webElement = driver.find_element_by_link_text("Sign in").click()
driver.find_element_by_name("email").send_keys("support@marketxls.com")
driver.find_element_by_name("password").send_keys("London20#")
driver.find_element_by_xpath("//*[@id='root']/div/div/div[1]/div/div/div/div/form/div/button/div").click()
driver.implicitly_wait(5)
element = driver.find_element_by_xpath("//*[@id='root']/div/div/main/div/div[2]/div/div[2]/div[2]/div[2]/table/tbody[1]/tr[1]/td[2]/div/div/a/div")
print(element.text)
