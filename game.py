import time
import random
import os

# --- Path Handling ---
# This finds the folder where game.py is located
base_path = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    return os.path.join(base_path, filename)

# Check if files exist, if not, create them with '0'
for file in ["cashbal.txt", "bankbal.txt"]:
    path = get_path(file)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("0")

# --- Initial Load ---
with open(get_path("cashbal.txt"), "r") as f:
    cashbal = int(f.read())

with open(get_path("bankbal.txt"), "r") as f:
    bankbal = int(f.read())

user = 1234
print("\n Welcome to the 'Economic Simulator'")

caught = ["stealing from the bank.", "pickpocketing a stranger.", "running a black-market deal.", "attempting an illegal trade."]
pass_reason = ["Crime successful! You escaped without being caught.", "Crime successful! You earned some dirty money.", "You escaped with the loot."]
work_statements = ["You worked in a shop", "You worked in a restaurant.", "You worked at a grocery store.", "You worked in a bank."]

class Game:
    def __init__(self):
        self.cashbal = cashbal
        self.bankbal = bankbal

    def save_data(self):
        """Helper function to save both balances to files"""
        with open(get_path("cashbal.txt"), "w") as f:
            f.write(str(self.cashbal))
        with open(get_path("bankbal.txt"), "w") as f:
            f.write(str(self.bankbal))

    def daily(self):
        daily_r = random.randint(1000, 3000)
        self.cashbal += daily_r
        self.save_data()
        print(f"\n------------------------------\nDaily reward received ${daily_r}\n------------------------------")

    def balance(self):
        print(f"\n----------------------------------------\nBank Balance: ${self.bankbal} | Cash Balance: ${self.cashbal}\n----------------------------------------")
    
    def crime(self):
        crime_s = random.randint(1, 100)
        if crime_s <= 50:
            fine = random.randint(500, 2000)
            caught_reason = random.choice(caught)
            print(f"\n----------------------------------------\nYou got caught while {caught_reason} & paid a fine of {fine}\n----------------------------------------")
            self.cashbal -= fine
            self.save_data()
        else:
            earned = random.randint(1000, 5000)
            crime_s_r = random.choice(pass_reason)
            print(f"\n----------------------------------------\n{crime_s_r} & earned {earned}\n----------------------------------------")
            self.cashbal += earned
            self.save_data()

    def work(self):
        work_s = random.choice(work_statements)
        earned_w = random.randint(500, 2000)
        print(f"\n----------------------------------------\n{work_s} & earned {earned_w}\n----------------------------------------")
        self.cashbal += earned_w
        self.save_data()

    def deposit(self, amount):
        if amount <= self.cashbal:
            self.bankbal += amount
            self.cashbal -= amount
            self.save_data()
            print(f"\n----------------------------------------\nDeposit of ${amount} successful!\n----------------------------------------")
        else:
            print("\n----------------------------------------\nInsufficient funds!\n----------------------------------------")

    def withdraw(self, amount):
        if amount <= self.bankbal:
            self.bankbal -= amount
            self.cashbal += amount
            self.save_data()
            print(f"\n----------------------------------------\nWithdraw of ${amount} successful!\n----------------------------------------")
        else:
            print("\n----------------------------------------\nInsufficient funds!\n----------------------------------------")

Economy_game = Game()

while True:
    print("\n1. Balance\n2. Crime\n3. Work\n4. Deposit\n5. Withdraw\n6. Daily reward\n7. Exit")
    try:
        choice = int(input("\nEnter your choice: "))
    except ValueError:
        print("Please enter a number!")
        continue

    if choice == 1:
        Economy_game.balance()
    elif choice == 2:
        Economy_game.crime()
    elif choice == 3:
        Economy_game.work()
    elif choice == 4:
        amount = int(input("\nEnter amount to deposit: "))
        Economy_game.deposit(amount)
    elif choice == 5:
        amount = int(input("\nEnter amount to withdraw: "))
        Economy_game.withdraw(amount)
    elif choice == 6:
        Economy_game.daily()
    elif choice == 7:
        print("\nThank you for playing!")
        break
    else:
        print("Invalid choice!")