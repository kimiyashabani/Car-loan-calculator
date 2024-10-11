from Calculation import *
from User_Input import *
from Recommendation import *
# TODO 1 : ASK THE USER TO PUT THE NEEDED INFORMATION


def main():
    for i in range(0, 2):
        userinput = Userinput()
        calculation = Calculation(userinput)
        calculation.set_car()
    recommendation = Recommendation()
    recommendation.visualiza_data()


if __name__ == "__main__":
    main()






