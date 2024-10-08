from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from xml.etree import ElementTree as ET
import time
import requests
import numpy as np
import math
# TODO 1 : ASK THE USER TO PUT THE NEEDED INFORMATION
car_make = input("What is your car brand? ")
car_model = input("What is your car model? ")
car_year = int(input("Enter the year of your car: "))
car_mileage = int(input("How much distance you have traveled with your car?")) #in miles
car_fuel_efficiency = int(input("Enter the fuel efficiency of your car: "))
driving_habits_weekday = int(input("In what frequency do you drive in a week?"))
user_state = input("In which state of United states do you live? ")
user_credit_score = int(input("What is your credit score? "))
time_of_loan = int(input("Please enter the time period of the loan in months: "))
average_miles_per_month = int(input("How many miles do you drive in a month approximately? "))
down_payment_answer = input("Do you want to include a down payment? (yes/no)")
if down_payment_answer.lower() == "yes":
    down_payment_amount = int(input("Please enter the amount of down payment: "))

interest_rate = 0
# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 2 : GET DATA FROM API OR WEB SCRAPING

# TODO 2.1 : EXPECTED PURCHASE PRICE FOR THE VEHICLE
#Keep the browser open after the program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.caranddriver.com/research/a32771057/what-should-i-pay-for-a-car/")
time.sleep(3)
#accepting the cookies
accept_cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
accept_cookies.click()
try:
    time.sleep(3)
    research_car = driver.find_element(By.CLASS_NAME, 'css-dhv4gi')
    research_car.click()
    time.sleep(1)
    #Selecting Make
    make_dropdown = driver.find_element(By.XPATH,'//*[@id="P0-8"]/div[2]/select')
    make_dropdown.click()
    make_options = make_dropdown.find_elements(By.TAG_NAME, 'Option')
    for option in make_options:
        if option.get_attribute('value').lower() == car_make.lower():
            option.click()
            break
        else:
            print(f"Make {car_make} not found in the options")
    #Selecting Model
    time.sleep(1)
    model_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[3]/select')
    model_dropdown.click()
    model_options = model_dropdown.find_elements(By.TAG_NAME, 'Option')
    for option in model_options:
        if option.get_attribute('value').lower() == car_model.lower():
            option.click()
            break
        else:
            print(f"Model {car_model} not found in the options")

    #Selecting Year
    time.sleep(1)
    year_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[4]/select')
    year_dropdown.click()
    year_options = year_dropdown.find_elements(By.TAG_NAME, 'Option')
    for option in year_options:
        if option.get_attribute('value') == car_year:
            option.click()
            break
        else:
            print(f"Year {car_year} not found in the options")
    #Clicking on Submit Button
    time.sleep(1)
    submit_button = driver.find_element(By.CLASS_NAME, 'e1ketqus1')
    submit_button.click()
    time.sleep(5)
    purchase_price = driver.find_element(By.CLASS_NAME, 'css-1qdemya')

except NoSuchElementException:
    print("Element not found")

#closing the driver
driver.quit()


# TODO 2.2 :EXPECTED INSURANCE COST
# Web scraping from bankrate.com
insurance_url = "https://www.bankrate.com/insurance/car/average-cost-of-car-insurance/#car-insurance-cost-by-state"
insurance_response = requests.get(insurance_url)
soup = BeautifulSoup(insurance_response.content, "html.parser")
def get_insurance_cost(user_state):
    rows = soup.find_all("tr", class_="display-flex flex-direction-column border-b border-gray mb-3 sm:display-table-row")
    for row in rows:
        state_link = row.find("a")
        if state_link and state_link.text.strip().lower() == user_state.lower():
            insurance_cost = row.find_all("div", class_="insurance-coverage-table--td text-black")[0]
            return insurance_cost.text.strip()
    return None
insurance_cost = (get_insurance_cost(user_state))

#TODO 2.3 : MPG OR FUEL EFFICIENCY


# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 3 : LOAN INTEREST RATE
# Data from CNN :
#https://edition.cnn.com/cnn-underscored/money/auto-loan-interest-rates-by-credit-score

def get_interest_rate(user_credit_score):
    if user_credit_score >= 781 and user_credit_score <= 850:
        interest_rate = 5.25
    elif user_credit_score >= 661 and user_credit_score <= 780:
        interest_rate = 6.87
    elif user_credit_score >= 601 and user_credit_score <= 660:
        interest_rate = 9.83
    elif user_credit_score >= 501 and user_credit_score <= 600:
        interest_rate = 13.18
    else:
        interest_rate = 15.77

# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 4 : CALCULATE THE DOWNPAYMENT
# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 5 : CALCULATE THE MONTHLY LOAN PAYMENT
def loan_calculator():

    if down_payment_amount is not None:
        p = purchase_price - down_payment_amount
    else:
        p = purchase_price

    r = interest_rate / 100 / 12
    n = time_of_loan
    monthly_payment = p(r * np.power(1 + r, n)) / (np.power(1 + r, n) - 1)

    return monthly_payment


# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 6 : CALCUATE THE GAS COST
def gas_cost_calculator(car_year, car_make, car_model):
    gas_cost_url = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/options"
    params = {
        'year': car_year,
        'make': car_make,
        'model': car_model
    }
    response = requests.get(gas_cost_url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch vehicle data from API.")
    # This API returns data in XML so:
    vehicle_data = ET.fromstring(response.content)
    # Extract MPG values from the response
    combined_mpg = vehicle_data.find('comb08').text
    # I assumed the gas price is 4.0 euros per gallon
    gas_price_per_gallon = 4.0
    monthly_gas_cost = (average_miles_per_month / float(combined_mpg)) * gas_price_per_gallon
    return (monthly_gas_cost)

# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 7 : CALCULATE THE REPAIR AND MAINTENANCE COST (YEARLY & MONTHLY)
def repair_cost_calculation():
 pass
# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 8 : GIVE RECOMMENDATION TO THE USER
# ------------------------------------------------------------------------------------------------------------------------------#

# TODO 9 : PRINT THE RESULT



