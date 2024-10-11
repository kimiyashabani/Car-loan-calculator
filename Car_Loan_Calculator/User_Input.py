class Userinput:
    def __init__(self):
        self.make = input("What is your car brand? ")
        self.model = input("What is your car model? ")
        self.year = int(input("Enter the year of your car: "))
        self.state = input("In which state of United states do you live? ")
        self.credit_score = int(input("What is your credit score? "))
        self.down_payment_answer = input("Do you want to include a down payment? (yes/no)")
        if self.down_payment_answer.lower() == "yes":
            self.down_payment_amount = int(input("Please enter the amount of down payment: "))
        else:
            self.down_payment_amount = None
        self.time_of_loan = int(input("Please enter the time period of the loan in months: "))
        self.average_miles_per_month = int(input("How many miles do you drive in a month approximately? "))
