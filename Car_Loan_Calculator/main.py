from Calculation import *
from User_Input import *
from Recommendation import *
# TODO 1 : ASK THE USER TO PUT THE NEEDED INFORMATION


def main():
    recommendation = Recommendation()
    car_count = 0
    while car_count < 2:
        userinput = Userinput()
        calculation = Calculation(userinput)
        expected_purchase_price = calculation.expected_purchase_price()
        if expected_purchase_price is None:
            print("expected purchase price is none. please enter the correct information")
        else:
            calculation.set_car(recommendation)
            car_count += 1

    recommendation.visualiza_data()


if __name__ == "__main__":
    main()






