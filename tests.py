import unittest

from bank_account import BankAccount, InsufficientFunds


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Alex", 1000.0)
        self.account1 = BankAccount("Lesya", 500.0)

    def test_init(self):
        self.assertEqual(self.account.balance, 1000.0)
        acc_default = BankAccount()
        self.assertEqual(acc_default.balance, 0)

        acc_negative = BankAccount(-100)
        self.assertEqual(acc_negative.balance, -100)

    def test_deposit_success(self):
        self.account.deposit(250)
        self.assertEqual(self.account.balance, 1250.0)

    def test_deposit_negative(self):
        with self.assertRaisesRegex(ValueError, "Deposit amount must be positive"):
            self.account.deposit(0)
        with self.assertRaisesRegex(ValueError, "Deposit amount must be positive"):
            self.account.deposit(-100)

    def test_deposit_invalid_type(self):
        with self.assertRaises(TypeError):
            self.account.deposit("one hundred hryvnias")

    def test_withdraw_success(self):
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)

    def test_withdraw_exact_balance(self):
        self.account.withdraw(1000)
        self.assertEqual(self.account.balance, 0)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaisesRegex(ValueError, "Withdraw amount must be positive"):
            self.account.withdraw(0)
        with self.assertRaisesRegex(ValueError, "Withdraw amount must be positive"):
            self.account.withdraw(-100)

    def test_withdraw_negative_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)
        with self.assertRaises(ValueError):
            self.account.withdraw(-100)

    def test_withdraw_invalid_type(self):
        with self.assertRaises(TypeError):
            self.account.withdraw("all hryvnias")

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 1050)
        self.account.withdraw(100)
        self.assertEqual(self.account.get_balance(), 950)

    def test_transfer_success(self):
        self.account.transfer(self.account1, 200)
        self.assertEqual(self.account.get_balance(), 800)
        self.assertEqual(self.account1.get_balance(), 700)

    def test_transfer_insufficient_funds(self):
        initial_balance = self.account.get_balance()
        initial_balance1 = self.account1.get_balance()
        with self.assertRaisesRegex(InsufficientFunds, "Insufficient funds"):
            self.account.transfer(self.account1, 1500)
        self.assertEqual(self.account.get_balance(), initial_balance)
        self.assertEqual(self.account1.get_balance(), initial_balance1)

    def test_transfer_negative(self):
        initial_balance = self.account.get_balance()
        initial_balance1 = self.account1.get_balance()
        with self.assertRaisesRegex(ValueError, "Withdraw amount must be positive"):
            self.account.transfer(self.account1, 0)
        with self.assertRaisesRegex(ValueError, "Withdraw amount must be positive"):
            self.account.transfer(self.account1, -50)
        self.assertEqual(self.account.get_balance(), initial_balance)
        self.assertEqual(self.account1.get_balance(), initial_balance1)

    def test_transfer_invalid_type(self):
        initial_balance = self.account.get_balance()
        not_a_account = "card account"
        with self.assertRaisesRegex(TypeError, "Other account must be BankAccount"):
            self.account.transfer(not_a_account, 100)
        self.assertEqual(self.account.get_balance(), initial_balance)

    def test_transfer_to_self(self):
        initial_balance = self.account.get_balance()
        self.account.transfer(self.account, 100)
        self.assertEqual(self.account.get_balance(), initial_balance)


if __name__ == '__main__':
    unittest.main()
