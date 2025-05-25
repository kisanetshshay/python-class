class Account:
    def __init__(self,name,amount):
        self.name = name
        self.deposits = [amount]         
        self.withdrawals = []             
        self.transactions = [("deposit", amount)]
        self.loan = 0
        self.is_frozen = False
        self.is_closed = False
        self.minimum_balance = 0

    def deposit(self, amount):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0:
            self.deposits.append(amount)
            self.transactions.append(("deposit", amount))
            return f"Deposited {amount}. Balance: {self.get_balance()}"
        return "Deposite must be positive."

    def withdraw(self, amount):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0 and self.get_balance_value() - amount >= self.minimum_balance:
            self.withdrawals.append(amount)
            self.transactions.append(("withdraw", amount))
            return f"Withdrew {amount}. Balance: {self.get_balance()}"
        return "Withdrawal denied. Check amount, balance, or minimum balance."

    def transfer_funds(self, amount, other_account):
        result = self.withdraw(amount)
        if result.startswith("Withdrew"):
            other_account.deposit(amount)
            return f"Transferred {amount} to {other_account.name}."
        return result

    def get_balance_value(self):
        return sum(self.deposits) - sum(self.withdrawals)

    def get_balance(self):
        return self.get_balance_value()
    def request_loan(self, amount):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0:
            self.loan += amount
            self.transactions.append(("loan", amount))
            return f"Loan of {amount} granted. Loan total: {self.loan}"
        return "Loan amount must be positive."

    def repay_loan(self, amount):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        if amount > 0 and self.loan > 0:
            pay = min(amount, self.loan)
            self.loan -= pay
            self.transactions.append(("repay loan", pay))
            return f"Repaid {pay}. Remaining loan: {self.loan}"
        return "No loan to repay or invalid amount."

    def view_account_details(self):
        return f"Owner: {self.name},Balance: {self.get_balance()},Loan: {self.loan},Frozen: {self.is_frozen},Closed: {self.is_closed}"

    def change_account_owner(self, new_name):
        self.name = new_name
        return f"Owner changed to {self.name}"

    def account_statement(self):
        print(f"Statement for {self.name}:")
        for i, (typ, amt) in enumerate(self.transactions, 1):
            print(f"{i}. {typ.capitalize()} - {amt}")

    def apply_interest(self):
        if self.is_closed or self.is_frozen:
            return "Account not active."
        interest = self.get_balance() * 0.05
        self.deposits.append(interest)
        self.transactions.append(("interest", interest))
        return f"Interest {interest} added. Balance: {self.get_balance()}"

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
        self.deposits = []
        self.withdrawals = []
        self.transactions.append(("close account", 0))
        return "Account closed. All balances set to zero."    
    
    