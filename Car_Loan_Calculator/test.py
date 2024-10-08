
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
car_make = input("What is your car brand? ")
car_model = input("What is your car model? ")
car_year = int(input("Enter the year of your car: "))
def expected_purchase_price():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.caranddriver.com/research/a32771057/what-should-i-pay-for-a-car/")
    time.sleep(3)
    # accepting the cookies
    accept_cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    accept_cookies.click()
    try:
        time.sleep(3)
        research_car = driver.find_element(By.CLASS_NAME, 'css-dhv4gi')
        research_car.click()
        time.sleep(1)
        # Selecting Make
        make_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[2]/select')
        make_dropdown.click()
        make_options = make_dropdown.find_elements(By.TAG_NAME, 'Option')
        for option in make_options:
            if option.get_attribute('value').lower() == car_make.lower():
                option.click()
                break

        # Selecting Model
        time.sleep(1)
        model_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[3]/select')
        model_dropdown.click()
        model_options = model_dropdown.find_elements(By.TAG_NAME, 'Option')
        for option in model_options:
            if option.get_attribute('value').lower() == car_model.lower():
                option.click()
                break

        # Selecting Year
        time.sleep(1)
        year_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[4]/select')
        year_dropdown.click()
        year_options = year_dropdown.find_elements(By.TAG_NAME, 'Option')
        for option in year_options:
            if option.get_attribute('value') == car_year:
                option.click()
                break

        # Clicking on Submit Button
        time.sleep(1)
        submit_button = driver.find_element(By.CLASS_NAME, 'e1ketqus1')
        submit_button.click()
        time.sleep(5)
        purchase_price = driver.find_element(By.CLASS_NAME, 'css-1qdemya')

    except NoSuchElementException:
        print("Element not found")

    # closing the driver
    driver.quit()

print(expected_purchase_price())
