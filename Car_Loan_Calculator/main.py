from Calculation import *
# TODO 1 : ASK THE USER TO PUT THE NEEDED INFORMATION
car_make = input("What is your car brand? ")
car_model = input("What is your car model? ")
car_year = int(input("Enter the year of your car: "))
user_state = input("In which state of United states do you live? ")
user_credit_score = int(input("What is your credit score? "))
time_of_loan = int(input("Please enter the time period of the loan in months: "))
average_miles_per_month = int(input("How many miles do you drive in a month approximately? "))
down_payment_answer = input("Do you want to include a down payment? (yes/no)")
if down_payment_answer.lower() == "yes":
    down_payment_amount = int(input("Please enter the amount of down payment: "))

# TODO 2 : CREATE AN OBJECT OF THE CLASS AND PASS THE USER INPUTS
cost_calc = Calculation(car_make, car_model, car_year, user_state, user_credit_score, down_payment_amount, time_of_loan, average_miles_per_month)
cost_calc.run_all_methods()



