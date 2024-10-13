from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
import http.client
import json


class Calculation:
    def __init__(self, user_data, expected_purchase_price=100, expected_interest_amount=None):
        self.user_data = user_data
        self.purchase_price_amount = expected_purchase_price
        self.interest_amount = expected_interest_amount

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
                if option.get_attribute('value').lower() == self.user_data.make.lower():
                    option.click()
                    break

            # Selecting Model
            time.sleep(1)
            model_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[3]/select')
            model_dropdown.click()
            model_options = model_dropdown.find_elements(By.TAG_NAME, 'Option')
            for option in model_options:
                if option.get_attribute('value').lower() == self.user_data.model.lower():
                    option.click()
                    break

            # Selecting Year
            time.sleep(1)
            year_dropdown = driver.find_element(By.XPATH, '//*[@id="P0-8"]/div[4]/select')
            year_dropdown.click()
            year_options = year_dropdown.find_elements(By.TAG_NAME, 'Option')
            for option in year_options:
                if option.get_attribute('value') == self.user_data.year:
                    option.click()
                    break
            # Clicking on Submit Button
            time.sleep(1)
            submit_button = driver.find_element(By.CLASS_NAME, 'e1ketqus1')
            submit_button.click()
            time.sleep(5)
            purchase_price = driver.find_element(By.CLASS_NAME, 'css-1qdemya')
            self.purchase_price_amount = int(purchase_price.text.replace("$", "").replace(",", ""))
            return self.purchase_price_amount

        except NoSuchElementException:
            return None



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
            if state_link and state_link.text.strip().lower() == self.user_data.state.lower():
                insurance_cost = row.find_all("div", class_="insurance-coverage-table--td text-black")[0]
                return insurance_cost.text.strip()
        return None

    # LOAN INTEREST RATE
    # Data from CNN :
    # https://edition.cnn.com/cnn-underscored/money/auto-loan-interest-rates-by-credit-score
    def get_interest_rate(self):
        if 781 <= self.user_data.credit_score <= 850:
            self.interest_amount = 5.25
        elif 661 <= self.user_data.credit_score <= 780:
            self.interest_amount = 6.87
        elif 601 <= self.user_data.credit_score <= 660:
            self.interest_amount = 9.83
        elif 501 <= self.user_data.credit_score <= 600:
            self.interest_amount = 13.18
        else:
            self.interest_amount = 15.77
        return self.interest_amount

    # CALCULATE THE MONTHLY LOAN PAYMENT
    def loan_calculator(self):

        if self.user_data.down_payment_amount is not None:
            p = self.purchase_price_amount - self.user_data.down_payment_amount
        else:
            p = self.purchase_price_amount

        r = self.interest_amount / 100 / 12
        n = self.user_data.time_of_loan
        monthly_payment = p*(r * np.power(1 + r, n)) / (np.power(1 + r, n) - 1)

        return monthly_payment

    # CALCULATE THE GAS COST
    def gas_cost_calculator(self):
        conn = http.client.HTTPSConnection("api.collectapi.com")

        state_abbreviations = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
            'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
            'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
            'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
            'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
            'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
            'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
            'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
            'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
            'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
            'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
        }

        user_state_abbrev = state_abbreviations.get(self.user_data.state.capitalize())

        headers = {
            'content-type': "application/json",
            'authorization': "apikey 2mEOtOkfOYQkkzpImIkoVB:0A45VXobnK5s425B50CbJp"
        }

        conn.request("GET", f"/gasPrice/stateUsaPrice?state={user_state_abbrev}", headers=headers)

        res = conn.getresponse()
        data = res.read()
        parsed_data = json.loads(data.decode("utf-8"))
        gas_price = parsed_data["result"]["state"]["gasoline"]
        return gas_price

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
            if cell_data[1].lower() == self.user_data.make.lower():
                final_price = int(cell_data[2].replace("$", "").replace(",", ""))
                # Devision by 10 because the website gives us the 10 Year Maintenance Cost
                yearly_repair_cost = final_price / 10
                monthly_repair_cost = yearly_repair_cost / 12
                return yearly_repair_cost, monthly_repair_cost

    def calling_all_methods(self):
        print("----- Calculating All Costs -----")

        expected_purchase_price = self.expected_purchase_price()
        print(f"Expected Purchase Price: {expected_purchase_price}")

        expected_insurance_cost = self.expected_insurance_cost()
        print(f"Expected Insurance Cost: {expected_insurance_cost}")

        interest_rate = self.get_interest_rate()
        print(f"Interest Rate: {interest_rate}")

        monthly_loan_payment = self.loan_calculator()
        print(f"Monthly Loan Payment: {monthly_loan_payment}")

        gas_cost = self.gas_cost_calculator()
        print(f"Gas Cost: {gas_cost}")

        yearly_repair_cost = self.repair_cost_calculation()[0]
        print(f"Repair Cost: {yearly_repair_cost}")

        monthly_repair_cost = self.repair_cost_calculation()[1]
        print(f"Monthly Repair Cost: {monthly_repair_cost}")

        car_data = {
            "make": self.user_data.make,
            "model": self.user_data.model,
            "year": self.user_data.year,
            "state": self.user_data.state,
            "credit_score": self.user_data.credit_score,
            "down_payment": self.user_data.down_payment_amount,
            "time_of_loan": self.user_data.time_of_loan,
            "average_miles_per_month": self.user_data.average_miles_per_month,
            "expected_purchase_price": expected_purchase_price,
            "expected_insurance_cost": expected_insurance_cost,
            "interest_rate": interest_rate,
            "monthly_loan_payment": monthly_loan_payment,
            "gas_cost": gas_cost,
            "yearly_repair_cost": yearly_repair_cost,
            "monthly_repair_cost": monthly_repair_cost
        }

        return car_data

    def set_car(self,recommendation):
        car_data = self.calling_all_methods()
        recommendation.add_car(car_data)

