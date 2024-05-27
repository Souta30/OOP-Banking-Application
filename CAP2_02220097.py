import random
import json

class Account:
    def __init__(self, account_number, account_type, initial_balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = initial_balance
        self.password = self.generate_password()

    def generate_password(self):
        # Generate a 4-digit password
        return str(random.randint(1000, 9999))

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

class SavingsAccount(Account):
    def __init__(self, account_number, initial_balance=0):
        super().__init__(account_number, 'savings', initial_balance)

class CurrentAccount(Account):
    def __init__(self, account_number, initial_balance=0):
        super().__init__(account_number, 'current', initial_balance)


def save_account(account):
    account_data = {
        'account_number': account.account_number,
        'password': account.password,
        'account_type': account.account_type,
        'balance': account.balance
    }
    with open('accounts.txt', 'a') as f:
        f.write(json.dumps(account_data) + '\n')

def save_all_accounts(accounts):
    with open('accounts.txt', 'w') as f:
        for account in accounts:
            account_data = {
                'account_number': account.account_number,
                'password': account.password,
                'account_type': account.account_type,
                'balance': account.balance
            }
            f.write(json.dumps(account_data) + '\n')

def load_accounts():
    accounts = []
    try:
        with open('accounts.txt', 'r') as f:
            for line in f:
                account_data = json.loads(line.strip())
                if account_data['account_type'] == 'savings':
                    account = SavingsAccount(account_data['account_number'], account_data['balance'])
                elif account_data['account_type'] == 'current':
                    account = CurrentAccount(account_data['account_number'], account_data['balance'])
                account.password = account_data['password']
                accounts.append(account)
    except FileNotFoundError:
        pass
    return accounts

def get_account_by_number(account_number):
    accounts = load_accounts()
    for account in accounts:
        if account.account_number == account_number:
            return account
    return None

def login(account_number, password):
    account = get_account_by_number(account_number)
    if account and account.password == password:
        return account
    return None

def delete_account(account_number, password):
    accounts = load_accounts()
    account_to_delete = None
    for account in accounts:
        if account.account_number == account_number and account.password == password:
            account_to_delete = account
            break
    if account_to_delete:
        accounts.remove(account_to_delete)
        save_all_accounts(accounts)
        return True
    return False

def transfer_funds(from_account_number, to_account_number, amount):
    accounts = load_accounts()
    from_account = get_account_by_number(from_account_number)
    to_account = get_account_by_number(to_account_number)
    if from_account and to_account:
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            for i, account in enumerate(accounts):
                if account.account_number == from_account_number:
                    accounts[i] = from_account
                elif account.account_number == to_account_number:
                    accounts[i] = to_account
            save_all_accounts(accounts)
            return True
        else:
            print("You have insufficient balance to complete the transfer.")
            return False
    print("The recipient account does not exist.")
    return False

def main():
    while True:
        print("\nGreetings from the JAZZI Banking Application")
        print("1. Open a new account")
        print("2. Login to an existing account")
        print("3. Exit")
        choice = input("Enter your selection here: ")

        if choice == '1':
            account_type = input("Type in the account type (current or savings): ").lower()
            initial_deposit = float(input("Enter the amount of the initial deposit: "))
            account_number = random.randint(100000000, 999999999)  # 9-digit account number
            if account_type == 'savings':
                account = SavingsAccount(account_number, initial_deposit)
            elif account_type == 'current':
                account = CurrentAccount(account_number, initial_deposit)
            else:
                print("The account type is invalid!")
                continue
            save_account(account)
            print(f"Account created! Your account number is {account.account_number} and your password is {account.password}")

        elif choice == '2':
            account_number = int(input("Put your account number here: "))
            password = input("Enter your password: ")
            account = login(account_number, password)
            if account:
                print(f"Login successful! Welcome, Account Number: {account.account_number}")
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit Funds")
                    print("3. Withdraw Funds")
                    print("4. Transfer Funds")
                    print("5. Delete Account")
                    print("6. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == '1':
                        print(f"Your current balance is: {account.balance}")

                    elif sub_choice == '2':
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            accounts = load_accounts()
                            for i, acc in enumerate(accounts):
                                if acc.account_number == account.account_number:
                                    accounts[i] = account
                            save_all_accounts(accounts)
                            print(f"Deposit successful! New account balance: {account.balance}")
                        else:
                            print("Invalid deposit amount!")

                    elif sub_choice == '3':
                        amount = float(input("Enter the desired withdrawal amount: "))
                        if account.withdraw(amount):
                            accounts = load_accounts()
                            for i, acc in enumerate(accounts):
                                if acc.account_number == account.account_number:
                                    accounts[i] = account
                            save_all_accounts(accounts)
                            print(f"Withdrawal successful! New account balance: {account.balance}")
                        else:
                            print("Not enough money or an incorrect quantity!")

                    elif sub_choice == '4':
                        to_account_number = int(input("Enter recipient's account number: "))
                        amount = float(input("Enter amount to transfer: "))
                        if transfer_funds(account.account_number, to_account_number, amount):
                            print(f"Transfer successful! Your new account balance is: {account.balance}")
                        else:
                            print("Transfer failed! You have insufficient balance to complete the transfer.")

                    elif sub_choice == '5':
                        if delete_account(account.account_number, password):
                            print("Account deleted successfully!")
                            break
                        else:
                            print("Account deletion was unsuccessful! The wrong identification.")

                    elif sub_choice == '6':
                        print("Logged out successfully!")
                        break

                    else:
                        print("Not a valid option! Please give it another go.")
            else:
                print("Login failed! Verify the password and account number you have.")

        elif choice == '3':
            print("Closing the application. Farewell!")
            break

        else:
            print("Not a valid option! Kindly give it another shot.")

if __name__ == "__main__":
    main()
