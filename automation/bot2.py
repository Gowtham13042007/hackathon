from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def googleforms(email_address,three_links):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://docs.google.com/forms/d/16o8uoY43FdPu5yoYb71yi_pip2N1RoFehPCRSRU7j58/viewform?pli=1&pli=1&edit_requested=true')
    time.sleep(2)

    email=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    email.send_keys(f"{email_address}")

    choice1=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    choice1.send_keys(f"{three_links[0]}")

    choice2=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    choice2.send_keys(f"{three_links[1]}")

    choice3=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    choice3.send_keys(f"{three_links[2]}")

    submit=driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit.click()

    driver.quit()
