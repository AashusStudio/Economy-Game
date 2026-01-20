import time
import random

user = 1234
print("\n Welcome to the \'Economic Simulator\'")

with open("cashbal.txt", "r") as f:
    cashbal = int(f.read())

with open("bankbal.txt", "r") as f:
    bankbal = int(f.read())

caught = ["stealing from the bank.","pickpocketing a stranger.", "running a black-market deal.", "attempting an illegal trade."]
pass_reason = ["Crime successful! You escaped without being caught.", "Crime successful! You earned some dirty money.", "You escaped with the loot."]
work_statements = ["You worked in a shop", "You worked in a restaurant.", "You worked at a grocery store.", "You worked in a bank."]
class Game:
    def __init__(self):
        self.cashbal = cashbal
        self.bankbal = bankbal

    def daily(self):
        daily_r = random.randint(1000, 3000)
        self.cashbal += daily_r
        with open("cashbal.txt", "w") as f:
            f.write(str(self.cashbal))
        print(f"\n------------------------------\nDaily reward recived ${daily_r}\n------------------------------")


    def balance(self):
        print(f"\n----------------------------------------\nBank Balance: ${self.bankbal} | Cash Balance: ${self.cashbal}\n----------------------------------------")
    
    def crime(self):
        crime_s = random.randint(1, 100)
        if crime_s <=50:
            fine = random.randint(500, 2000)
            caught_reason = random.choice(caught)
            print(f"\n----------------------------------------\nYou got caught while {caught_reason} & paid a fine of {fine}\n----------------------------------------")
            self.cashbal -= fine
            with open("cashbal.txt", "w") as f:
                f.write(str(self.cashbal))

        elif crime_s > 50:
            earned = random.randint(1000, 5000)
            crime_s_r = random.choice(pass_reason)
            print(f"\n----------------------------------------\n{crime_s_r} & earned {earned}\n----------------------------------------")
            self.cashbal += earned
            with open("cashbal.txt", "w") as f:
                f.write(str(self.cashbal))

    def work(self):
        work_s = random.choice(work_statements)
        earned_w = random.randint(500, 2000)
        print(f"\n----------------------------------------\n{work_s} & earned {earned_w}\n----------------------------------------")
        self.cashbal += earned_w
        with open("cashbal.txt", "w") as f:
            f.write(str(self.cashbal))

    def deposit(self, amount):
        if amount <= self.cashbal:
            self.bankbal += amount
            self.cashbal -= amount
            with open("cashbal.txt", "w") as f:
                f.write(str(self.cashbal))
            with open("bankbal.txt", "w") as f:
                f.write(str(self.bankbal))
            print(f"\n----------------------------------------\nDeposit of ${amount} successful!\n----------------------------------------")

        elif amount > self.cashbal:
            print("\n----------------------------------------\nInsufficient funds!\n----------------------------------------")

    def withdraw(self, amount):
        if amount <= self.bankbal:
            self.bankbal -= amount
            self.cashbal += amount
            with open("cashbal.txt", "w") as f:
                f.write(str(self.cashbal))
            with open("bankbal.txt", "w") as f:
                f.write(str(self.bankbal))
            print(f"\n----------------------------------------\nWithdraw of ${amount} successful!\n----------------------------------------")

        elif amount > self.bankbal:
            print("\n----------------------------------------\nInsufficient funds!\n----------------------------------------")

Economy_game = Game()

while True:

    print("\n1. Balance\n2. Crime\n3. Work\n4. Deposit\n5. Withdraw\n6. Daily reward\n7. Exit")
    choice = int(input("\nEnter your choice: "))

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
        print("/nThank you for playing!")
        break

    else:
        print("Invalid choice!")