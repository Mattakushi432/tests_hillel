class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, owner=None, initial_balance=0):
        if isinstance(owner, (int, float)) and initial_balance == 0 and not isinstance(owner, bool):
            self.owner = None
            self.balance = owner
        else:
            self.owner = owner
            self.balance = initial_balance

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Amount must be a number")
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount

    def transfer(self, other_account, amount):
        if not isinstance(other_account, BankAccount):
            raise TypeError("Other account must be BankAccount")
        self.withdraw(amount)
        other_account.deposit(amount)

    def get_balance(self):
        return self.balance
