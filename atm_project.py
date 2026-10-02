import random
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="", database="atm_1")
cur = con.cursor()


def save():

    cur.execute("UPDATE accounts SET balance = %s WHERE account_number = %s",
                (balance, account_number))
    con.commit()


def get_pin():

    cur.execute("SELECT pin FROM accounts WHERE account_number = %s", (account_number,))
    return cur.fetchone()[0]


def record(kind, amount):

    cur.execute("INSERT INTO transactions (account_number, type, amount, balance_after) VALUES (%s, %s, %s, %s)",
                (account_number, kind, amount, balance))
    save()


def bank_selection():

    banks = {"1":"SBI", "2": "ICICI", "3": "PNB",
            "4": "CANARA", "5": "AXIS", "6": "HDFC"}
    for key, name in banks.items():
        print(f"{key}.{name}")

    bank = input("Choose your bank:")
    if bank not in banks:
        print("Invalid input!")
    return banks.get(bank)


def pin_check():

    for attempt in range(3):
        pin = int(input("Enter your pin:"))
        if get_pin() == pin:
            print(f"Welcome {customer_name} to our {selected_bank} BANK")
            print("login successfull")
            return True
        else:
            print("Invalid pin!")
            print(f"Attempts left: {2- attempt}")
    print("login failed")
    return False


def forgot_pin():

    forgot = input("Forgot pin? (y/n):")
    if forgot.lower() == "y":
        print("Forgot pin selected")
    else:
        print("Please try again!")
        return

    account = int(input("Enter your account number:"))
    if account == account_number:
        otp = random.randint(1000,9999)
        print(f"Your OTP is {otp}")
        user_otp = int(input("Enter your OTP:"))
        if user_otp == otp:
            new_pin = int(input("Enter your new pin:"))
            confirm_pin = int(input("Confirm your new pin:"))
            if new_pin == confirm_pin:
                cur.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (new_pin, account_number))
                record("PIN Change", 0)
                print("Pin changed successfully!")
            else:
                print("Pin does not match!")
        else:
            print("Invalid OTP!")
    else:
        print("Invalid account number!")


def ATM_menu():

    menu = {"1" : "CHECK BALANCE", "2" : "DEPOSIT", "3" :"WITHDRAW", "4" : "CHANGE PIN",
            "5" : "TRANSFER MONEY", "6" : "MINI STATEMENT", "7" : "EXIT"}
    
    print("========== ATM MENU ========== ")
    for key, name in menu.items():
        print(f"{key}.{name}")
    print("===============================")
    
    atm = input("Enter your option:")

    if atm not in menu:
        print("Invalid input!")
    return menu.get(atm)


def check_balance():

    global balance,account_number
    account = int(input("Enter your account number:"))
    if account == account_number:
        print("Current balance:",balance)
    else:
        print("Invalid account number!")


def deposit():

    global balance
    amount = int(input("Enter your deposit amount:"))
    balance += amount
    record("Deposit", amount)
    print("Updated balance:", balance)


def withdraw():

    global balance
    amount = int(input("Enter your withdraw amount:"))
    if amount <= balance:
        balance -= amount
        record("Withdrawal", amount)
        print(f"Remaining balance:{balance}")
    else:
        print("Insufficient balance!")


def change_pin():

    current_pin = int(input("Enter your current pin:"))
    if current_pin == get_pin():
        new_pin = int(input("Enter your new pin:"))
        confirm_pin = int(input("Confirm your new pin:"))
        if new_pin == confirm_pin:
            cur.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (new_pin, account_number))
            record("PIN Change", 0)
            print("Pin changed successfully!")
        else:
            print("Pin does not match!")
    else:
        print("Wrong current pin!")


def transfer():

    global balance
    recipient_account = int(input("Enter recipient account number:"))
    cur.execute("SELECT customer_name FROM accounts WHERE account_number = %s", (recipient_account,))
    row = cur.fetchone()
    if recipient_account == account_number:
        print("You can't transfer to your own account!")
    elif row is None:
        print("Invalid recipient account number!")
    else:
        amount = int(input("Enter amount to transfer:"))
        if amount <= balance:
            balance -= amount
            cur.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s",
                        (amount, recipient_account))
            cur.execute("INSERT INTO transactions (account_number, type, amount, balance_after) SELECT account_number, 'Received', %s, balance FROM accounts WHERE account_number = %s",
                        (amount, recipient_account))
            record("Transfer", amount)
            print(f"Transferred {amount} to {row[0]} ({recipient_account}). Remaining balance: {balance}")
        else:
            print("Insufficient balance!")


def mini_statement():

    print("\n----------MINI STATEMENT-------------")
    print("Customer:", customer_name)
    
    cur.execute("SELECT type, amount, balance_after, date_time FROM transactions WHERE account_number = %s AND type != 'PIN Change' ORDER BY id DESC LIMIT 5",
                (account_number,))
    for t in cur.fetchall():
        print(f"{t[3]:%d-%m-%Y %H:%M}  {t[0]}: {t[1]}  (Balance: {t[2]})")
    print("Balance:", balance)
    print("--------------------------------------")


selected_bank = bank_selection()

account_number = int(input("Enter your account number:"))

cur.execute("SELECT customer_name, balance FROM accounts WHERE account_number = %s AND bank = %s",
            (account_number, selected_bank))
row = cur.fetchone()

if row is None:
    print("Account not found for this bank!")
else:
    customer_name, balance = row
    if pin_check():
        while True:
            atm_system = ATM_menu()
            if atm_system == "CHECK BALANCE":
                check_balance()
            elif atm_system == "DEPOSIT":
                deposit()
            elif atm_system == "WITHDRAW":
                withdraw()
            elif atm_system == "CHANGE PIN":
                change_pin()
            elif atm_system == "TRANSFER MONEY":
                transfer()
            elif atm_system == "MINI STATEMENT":
                mini_statement()
            elif atm_system == "EXIT":
                print("Thank you!")
                break
    else:
        forgot_pin()

con.close()
