import time
import random
import os

# --- Path Handling ---
# Get the directory where the script is located to ensure file paths work regardless of where it's run
base_path = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    """Helper function to join the base directory with a filename."""
    return os.path.join(base_path, filename)

# Check/Create necessary files (The Database)
# Each key is a filename, and the value is the default starting data
files_to_check = {
    "cashbal.txt": "0",
    "bankbal.txt": "0",
    "last_crime.txt": "0",
    "last_work.txt": "0",
    "last_daily.txt": "0"
}

# Ensure all text files exist before the game starts
for file, default in files_to_check.items():
    path = get_path(file)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(default)

# --- Initial Load ---
# Read the current balances from the files to initialize variables
with open(get_path("cashbal.txt"), "r") as f:
    cashbal = int(f.read())

with open(get_path("bankbal.txt"), "r") as f:
    bankbal = int(f.read())

print("\n 🎮 Welcome to the 'Economic Simulator' 📈")

# Text lists for flavor and variety in game messages
caught = ["stealing from the bank 🏦", "pickpocketing a stranger 🕵️", "running a black-market deal 🖤", "attempting an illegal trade 📦"]
pass_reason = ["✅ Crime successful! You escaped without being caught.", "💰 Crime successful! You earned some dirty money.", "🏃 You escaped with the loot!"]
work_statements = ["💼 You worked in a shop", "🍔 You worked in a restaurant.", "🛒 You worked at a grocery store.", "🏦 You worked in a bank."]

class Game:
    def __init__(self):
        # Initialize the game instance with the loaded balances
        self.cashbal = cashbal
        self.bankbal = bankbal

    def save_data(self):
        """Saves current balance variables back to the text files."""
        with open(get_path("cashbal.txt"), "w") as f:
            f.write(str(self.cashbal))
        with open(get_path("bankbal.txt"), "w") as f:
            f.write(str(self.bankbal))

    def check_cooldown(self, filename, cooldown_seconds):
        """
        Reads the last action time from a file and compares it to current time.
        Returns (is_ready: bool, remaining_time_string: str)
        """
        with open(get_path(filename), "r") as f:
            last_time = float(f.read())
        
        current_time = time.time()
        elapsed = current_time - last_time
        
        if elapsed < cooldown_seconds:
            remaining = cooldown_seconds - elapsed
            # Format the output string based on how much time is left
            if remaining > 3600:
                return False, f"{int(remaining//3600)}h {int((remaining%3600)//60)}m remaining"
            elif remaining > 60:
                return False, f"{int(remaining//60)}m {int(remaining%60)}s remaining"
            else:
                return False, f"{int(remaining)}s remaining"
        return True, ""

    def update_cooldown(self, filename):
        """Overwrites the cooldown file with the current Unix timestamp."""
        with open(get_path(filename), "w") as f:
            f.write(str(time.time()))

    def daily(self):
        """Claim a free daily reward once every 24 hours."""
        ready, msg = self.check_cooldown("last_daily.txt", 86400) # 86400s = 1 day
        if not ready:
            print(f"\n⏳ You already claimed your daily reward! Come back in {msg}.")
            return

        daily_r = random.randint(1000, 3000)
        self.cashbal += daily_r
        self.save_data()
        self.update_cooldown("last_daily.txt")
        print(f"\n✨ ---------------------- ✨\n🎁 Daily reward received: ${daily_r}\n✨ ---------------------- ✨")

    def balance(self):
        """Displays current Cash and Bank holdings."""
        print(f"\n💰 -------------------------------- 💰")
        print(f"🏦 Bank: ${self.bankbal} | 💵 Cash: ${self.cashbal}")
        print(f"💰 -------------------------------- 💰")
    
    def crime(self):
        """High risk, high reward action. 50% chance of failing and losing money."""
        ready, msg = self.check_cooldown("last_crime.txt", 60) # 1 min cooldown
        if not ready:
            print(f"\n⏳ The police are watching! Wait {msg} before your next crime.")
            return

        crime_s = random.randint(1, 100)
        if crime_s <= 50: # 50% chance of failure
            fine = random.randint(500, 2000)
            caught_reason = random.choice(caught)
            print(f"\n🚨 -------------------------------- 🚨")
            print(f"Caught while {caught_reason} \n💸 Paid a fine of: ${fine}")
            print(f"🚨 -------------------------------- 🚨")
            self.cashbal -= fine
        else: # Success
            earned = random.randint(1000, 5000)
            crime_s_r = random.choice(pass_reason)
            print(f"\n🧤 -------------------------------- 🧤")
            print(f"{crime_s_r} \n➕ Earned: ${earned}")
            print(f"🧤 -------------------------------- 🧤")
            self.cashbal += earned
        
        self.save_data()
        self.update_cooldown("last_crime.txt")

    def work(self):
        """Safe way to earn money with no risk of loss."""
        ready, msg = self.check_cooldown("last_work.txt", 60)
        if not ready:
            print(f"\n⏳ You are exhausted! Rest for {msg} before working again.")
            return

        work_s = random.choice(work_statements)
        earned_w = random.randint(500, 2000)
        print(f"\n🔨 -------------------------------- 🔨")
        print(f"{work_s} \n💵 Earned: ${earned_w}")
        print(f"🔨 -------------------------------- 🔨")
        self.cashbal += earned_w
        self.save_data()
        self.update_cooldown("last_work.txt")

    def deposit(self, amount):
        """Moves money from Cash to Bank."""
        if amount <= self.cashbal:
            self.bankbal += amount
            self.cashbal -= amount
            self.save_data()
            print(f"\n📥 Deposit of ${amount} successful!")
        else:
            print("\n❌ Insufficient cash funds!")

    def withdraw(self, amount):
        """Moves money from Bank to Cash."""
        if amount <= self.bankbal:
            self.bankbal -= amount
            self.cashbal += amount
            self.save_data()
            print(f"\n📤 Withdraw of ${amount} successful!")
        else:
            print("\n❌ Insufficient bank funds!")

# Create an instance of the Game class
Economy_game = Game()

# --- Main Game Loop ---
while True:
    print("\n--- 📟 MAIN MENU ---")
    print("1. 💰 Balance")
    print("2. 🧤 Crime")
    print("3. 🔨 Work")
    print("4. 📥 Deposit")
    print("5. 📤 Withdraw")
    print("6. 🎁 Daily Reward")
    print("7. 🚪 Exit")
    
    try:
        choice = int(input("\nEnter choice: "))
    except ValueError:
        print("⚠️ Please enter a valid number!")
        continue

    if choice == 1:
        Economy_game.balance()
    elif choice == 2:
        Economy_game.crime()
    elif choice == 3:
        Economy_game.work()
    elif choice == 4:
        try:
            amount = int(input("Enter amount: "))
            Economy_game.deposit(amount)
        except ValueError: 
            print("⚠️ Invalid amount.")
    elif choice == 5:
        try:
            amount = int(input("Enter amount: "))
            Economy_game.withdraw(amount)
        except ValueError: 
            print("⚠️ Invalid amount.")
    elif choice == 6:
        Economy_game.daily()
    elif choice == 7:
        print("\n👋 Thank you for playing! See you soon.")
        break
    else:
        print("⚠️ Invalid choice!")
