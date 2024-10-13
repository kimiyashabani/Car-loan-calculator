class Userinput:
    car_brands = ["Toyota", "Fiat", "Volkswagen", "Mitsubishi", "Honda", "Mazda", "Hyundai",
                  "Kia", "Mini", "Subaru", "Nissan", "Buick", "Chevrolet", "Dodge", "Chrysler",
                  "GMC", "Ford", "Jeep", "Ram"]

    us_states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
        "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
        "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    ]

    def __init__(self):
        self.make = input("What is your car brand? ")
        while self.make.title() not in Userinput.car_brands:
            print("Please enter a valid car brand ")
            print(f"Valid car brands are: {', ' .join(Userinput.car_brands)}")
            self.make = input("What is your car brand? ")
        self.model = input("What is your car model? ")
        self.year = int(input("Enter the year of your car: "))
        self.state = input("In which state of United states do you live? ")
        while self.state.title() not in Userinput.us_states:
            print("Please enter a valid state")
            print(f"Valid states are: {', ' .join(Userinput.us_states)}")
            self.state = input("In which state of United states do you live? ")
        self.credit_score = int(input("What is your credit score? "))
        self.down_payment_answer = input("Do you want to include a down payment? (yes/no)")
        if self.down_payment_answer.lower() == "yes":
            self.down_payment_amount = int(input("Please enter the amount of down payment: "))
        else:
            self.down_payment_amount = None
        self.time_of_loan = int(input("Please enter the time period of the loan in months: "))
        self.average_miles_per_month = int(input("How many miles do you drive in a month approximately? "))
