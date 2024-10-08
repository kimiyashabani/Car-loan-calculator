from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
class Calculation:
    def __init__(self, car_make, car_model, car_year, user_state, user_credit_score, down_payment=None, time_of_loan=30, average_miles_per_month=1000):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.user_state = user_state
        self.user_credit_score = user_credit_score
        self.down_payment = down_payment
        self.time_of_loan = time_of_loan
        self.average_miles_per_month = average_miles_per_month


    # EXPECTED PURCHASE PRICE
    def expected_purchase_price(self):
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
                if option.get_attribute('value').lower() == self.car_make.lower():
                    option.click()
                    break

            # Selecting Model
            time.sleep(1)
            model_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[3]/select')
            model_dropdown.click()
            model_options = model_dropdown.find_elements(By.TAG_NAME, 'Option')
            for option in model_options:
                if option.get_attribute('value').lower() == self.car_model.lower():
                    option.click()
                    break

            # Selecting Year
            time.sleep(1)
            year_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[4]/select')
            year_dropdown.click()
            year_options = year_dropdown.find_elements(By.TAG_NAME, 'Option')
            for option in year_options:
                if option.get_attribute('value') == self.car_year:
                    option.click()
                    break
            # Clicking on Submit Button
            time.sleep(1)
            submit_button = driver.find_element(By.CLASS_NAME, 'e1ketqus1')
            submit_button.click()
            time.sleep(5)
            purchase_price = driver.find_element(By.CLASS_NAME, 'css-1qdemya')
            return int(purchase_price.text.replace("$", "").replace(",", ""))

        except NoSuchElementException:
            print("Element not found")

        # closing the driver
        driver.quit()


    # EXPECTED INSURANCE COST
    def expected_insurance_cost(self):
        insurance_url = "https://www.bankrate.com/insurance/car/average-cost-of-car-insurance/#car-insurance-cost-by-state"
        insurance_response = requests.get(insurance_url)
        soup = BeautifulSoup(insurance_response.content, "html.parser")
        rows = soup.find_all("tr",
                             class_="display-flex flex-direction-column border-b border-gray mb-3 sm:display-table-row")
        for row in rows:
            state_link = row.find("a")
            if state_link and state_link.text.strip().lower() == self.user_state.lower():
                insurance_cost = row.find_all("div", class_="insurance-coverage-table--td text-black")[0]
                return insurance_cost.text.strip()
        return None


    # LOAN INTEREST RATE
    # Data from CNN :
    # https://edition.cnn.com/cnn-underscored/money/auto-loan-interest-rates-by-credit-score
    def get_interest_rate(self, user_credit_score):
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
        return interest_rate



    # CALCULATE THE MONTHLY LOAN PAYMENT
    def loan_calculator(self):
        purchase_price = self.expected_purchase_price()
        interest_rate = self.get_interest_rate(self.user_credit_score)
        if self.down_payment is not None:
            p = purchase_price - self.down_payment
        else:
            p = purchase_price

        r = interest_rate / 100 / 12
        n = self.time_of_loan
        monthly_payment = p(r * np.power(1 + r, n)) / (np.power(1 + r, n) - 1)

        return monthly_payment


    # CALCULATE THE GAS COST
    def gas_cost_calculator(self):
        gas_cost_url = "https://www.fueleconomy.gov/ws/rest/vehicle/menu/options"
        params = {
            'year': self.car_year,
            'make': self.car_make,
            'model': self.car_model
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
        monthly_gas_cost = (self.average_miles_per_month / float(combined_mpg)) * gas_price_per_gallon
        return (monthly_gas_cost)


    # CALCULATE THE REPAIR AND MAINTENANCE COST (YEARLY & MONTHLY)
    def repair_cost_calculation(self):
        # Web scraping from caredge.com
        repair_cost_url = "https://caredge.com/ranks/maintenance/popular/10-year/best#models"
        repair_cost_response = requests.get(repair_cost_url)
        repair_soup = BeautifulSoup(repair_cost_response.content, "html.parser")
        tables = repair_soup.find_all("table",
                                      class_="table table-striped table-bordered table-hover ranks-table")
        target_table = tables[0]
        tbody = target_table.find("tbody")
        rows = tbody.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            cell_data = [cell.get_text(strip=True) for cell in cells]
            if cell_data[1].lower() == self.car_make.lower():
                final_price = int(cell_data[2].replace("$", "").replace(",", ""))
                # Devision by 10 because the website gives us the 10 Year Maintenance Cost
                return final_price/10


    def calling_all_methods(self):
        print("----- Calculating All Costs -----")

        expected_purchase_price = self.expected_purchase_price()
        print(f"Expected Purchase Price: {expected_purchase_price}")

        expected_insurance_cost = self.expected_insurance_cost()
        print(f"Expected Insurance Cost: {expected_insurance_cost}")

        interest_rate = self.get_interest_rate(self.user_credit_score)
        print(f"Interest Rate: {interest_rate}")

        monthly_loan_payment = self.loan_calculator()
        print(f"Monthly Loan Payment: {monthly_loan_payment}")

        gas_cost = self.gas_cost_calculator()
        print(f"Gas Cost: {gas_cost}")

        repair_cost = self.repair_cost_calculation()
        print(f"Repair Cost: {repair_cost}")

        monthly_repair_cost = repair_cost / 12
        print(f"Monthly Repair Cost: {monthly_repair_cost}")
        #return expected_purchase_price, expected_insurance_cost, interest_rate, monthly_loan_payment, gas_cost, repair_cost, yearly_repair_cost






