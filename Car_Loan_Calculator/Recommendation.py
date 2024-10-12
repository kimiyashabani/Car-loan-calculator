import matplotlib.pyplot as plt
import numpy as np
class Recommendation:
    def __init__(self):
        self.cars = []
    def add_car(self, cardata):
        self.cars.append(cardata)

    def visualiza_data(self):
        #define categories to compare together
        categories = ["Purchase Price", "Insurance Cost", "Loan Payment", "Gas Cost", " Yearly Repair Cost", "Monthly Repair Cost", "Interest Rate"]
        first_car = [self.cars[0]["expected_purchase_price"], self.cars[0]["expected_insurance_cost"], self.cars[0]["monthly_loan_payment"], self.cars[0]["gas_cost"], self.cars[0]["yearly_repair_cost"], self.cars[0]["monthly_repair_cost"], self.cars[0]["interest_rate"],self.cars[0]["model"]]
        second_car = [self.cars[1]["expected_purchase_price"], self.cars[1]["expected_insurance_cost"], self.cars[1]["monthly_loan_payment"], self.cars[1]["gas_cost"], self.cars[1]["yearly_repair_cost"], self.cars[1]["monthly_repair_cost"], self.cars[1]["interest_rate"],self.cars[1]["model"]]

        fig, axs = plt.subplots(3, 3, figsize=(15, 10))

        # Plot 1: Bar chart for comparing purchase price
        axs[0,0].bar([first_car[-1],second_car[-1]], [first_car[0], second_car[0]], color=['blue','green'])
        axs[0,0].set_title(categories[0])

        # Plot 2: Bar chart for comparing insurance cost
        axs[0,1].bar([first_car[-1],second_car[-1]], [first_car[1], second_car[1]], color=['blue','green'])
        axs[0,1].set_title(categories[1])

        # Plot 3: Line chart for comparing loan payment
        axs[0,2].plot([first_car[-1],second_car[-1]], [first_car[2], second_car[2]], marker='o', color='red')
        axs[0,2].set_title(categories[2])

        # Plot 4: Bar chart for gas cost
        axs[1,0].bar([first_car[-1],second_car[-1]], [first_car[3], second_car[3]], color=['orange','yellow'])
        axs[1,0].set_title(categories[3])

        # Plot 5: Bar chart for yearly repair cost
        axs[1,1].bar([first_car[-1],second_car[-1]], [first_car[4], second_car[4]], color=['blue','green'])
        axs[1,1].set_title(categories[4])

        # Plot 6: Line plot for monthly repair cost
        axs[1,2].plot([first_car[-1],second_car[-1]], [first_car[5], second_car[5]], marker='o', color='orange')
        axs[1,2].set_title(categories[5])

        # Plot 7: Line plot for interest rate
        axs[2,0].scatter([first_car[-1],second_car[-1]], [first_car[6], second_car[6]], marker='o', color='brown')
        axs[2,0].set_title(categories[6])

        #Hiding the empty subplots
        axs[2,1].axis('off')
        axs[2, 2].axis('off')

        plt.tight_layout()

        plt.show()
    def print_car(self):
        print(self.cars)





