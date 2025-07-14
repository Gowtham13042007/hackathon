from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def botwork(fields):
    related_fields=[]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.mynextmove.org/")
    time.sleep(3)

    profession = driver.find_element(By.XPATH, '//*[@id="s"]')
    profession.send_keys(f"{fields}")

    go = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[1]/div[2]/div/div/form/div[1]/button')
    go.click()
    time.sleep(2)

    career_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.list-group.border li a')

    count = 1
    for elem in career_elements:
        name = elem.text.strip()
        if name: 
            related_fields.append(name)
            count += 1

    driver.quit()
    return related_fields 