
from datetime import datetime

class Transaction:
    def __init__(self, amount, transaction_type, narration="", date_time=None):
        self.amount = amount
        self.transaction_type = transaction_type  
        self.narration = narration
        self.date_time = date_time or datetime.now()

    def __repr__(self):
        return (f"{self.date_time.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"{self.transaction_type.title()} | "
                f"Amount: {self.amount} | "
                f"Narration: {self.narration}")

class Account:
    def __init__(self, name, account_number, opening_amount):
        self.name = name
        self.__account_number = account_number  
        self.__balance = 0                     
        self.__loan = 0                         
        self.is_frozen = False
        self.is_closed = False
        self.minimum_balance = 0
        self.transactions = []
        self.deposit(opening_amount, narration="Initial deposit")

    def get_account_number(self):
        return self.__account_number

    def get_balance(self):
        balance = 0
        for txn in self.transactions:
            if txn.transaction_type == "deposit":
                balance += txn.amount
            elif txn.transaction_type == "withdraw":
                balance -= txn.amount
            elif txn.transaction_type == "interest":
                balance += txn.amount
            elif txn.transaction_type == "repay loan":
                balance -= txn.amount
            elif txn.transaction_type == "loan":
                balance += txn.amount
            elif txn.transaction_type == "close account":
                balance = 0
                break
        self.__balance = balance
        return self.__balance

    def deposit(self, amount, narration=""):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0:
            txn = Transaction(amount, "deposit", narration)
            self.transactions.append(txn)
            self.__balance = self.get_balance()
            return f"Deposited {amount}. Balance: {self.__balance}"
        return "Deposit must be positive."

    def withdraw(self, amount, narration=""):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0 and self.get_balance() - amount >= self.minimum_balance:
            txn = Transaction(amount, "withdraw", narration)
            self.transactions.append(txn)
            self.__balance = self.get_balance()
            return f"Withdrew {amount}. Balance: {self.__balance}"
        return "Withdrawal denied. Check amount, balance, or minimum balance."

    def transfer_funds(self, amount, other_account, narration=""):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        withdrawal_result = self.withdraw(amount, narration=f"Transfer to {other_account.name}. {narration}")
        if withdrawal_result.startswith("Withdrew"):
            other_account.deposit(amount, narration=f"Transfer from {self.name}. {narration}")
            return f"Transferred {amount} to {other_account.name}."
        return withdrawal_result

    def request_loan(self, amount, narration=""):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0:
            self.__loan += amount
            txn = Transaction(amount, "loan", narration)
            self.transactions.append(txn)
            self.__balance = self.get_balance()
            return f"Loan of {amount} granted. Loan total: {self.__loan}"
        return "Loan amount must be positive."

    def repay_loan(self, amount, narration=""):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0 and self.__loan > 0:
            pay = min(amount, self.__loan)
            self.__loan -= pay
            txn = Transaction(pay, "repay loan", narration)
            self.transactions.append(txn)
            self.__balance = self.get_balance()
            return f"Repaid {pay}. Remaining loan: {self.__loan}"
        return "No loan to repay or invalid amount."

    def view_account_details(self):
        return (f"Owner: {self.name}, "
                f"Balance: {self.get_balance()}, "
                f"Loan: {self.__loan}, "
                f"Frozen: {self.is_frozen}, "
                f"Closed: {self.is_closed}")

    def change_account_owner(self, new_name):
        self.name = new_name
        return f"Owner changed to {self.name}"

    def account_statement(self):
        print(f"Statement for {self.name}:")
        for i, txn in enumerate(self.transactions, 1):
            print(f"{i}. {txn}")

    def apply_interest(self, narration=""):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        interest = self.get_balance() * 0.05
        txn = Transaction(interest, "interest", narration)
        self.transactions.append(txn)
        self.__balance = self.get_balance()
        return f"Interest {interest} added. Balance: {self.__balance}"

    def freeze_account(self):
        self.is_frozen = True
        return "Account frozen."

    def unfreeze_account(self):
        self.is_frozen = False
        return "Account unfrozen."

    def set_minimum_balance(self, amount):
        self.minimum_balance = amount
        return f"Minimum balance set to {self.minimum_balance}"

    def close_account(self):
        self.is_closed = True
        self.transactions.append(Transaction(0, "close account", narration="Account closed"))
        self.__balance = 0
        return "Account closed. All balances set to zero."