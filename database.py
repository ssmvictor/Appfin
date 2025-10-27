import sqlite3
from typing import List, Optional

class Account:
    def __init__(self, id: int, name: str, type: str, balance: float):
        self.id = id
        self.name = name
        self.type = type
        self.balance = balance

class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Transaction:
    def __init__(self, id: int, description: str, amount: float, date: str, account_id: int, category_id: int, category_name: str):
        self.id = id
        self.description = description
        self.amount = amount
        self.date = date
        self.account_id = account_id
        self.category_id = category_id
        self.category_name = category_name

class Budget:
    def __init__(self, id: int, category_id: int, amount: float, start_date: str, end_date: str, category_name: str):
        self.id = id
        self.category_id = category_id
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.category_name = category_name

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def create_tables(self) -> None:
        if not self.conn:
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                balance REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                account_id INTEGER,
                category_id INTEGER,
                FOREIGN KEY (account_id) REFERENCES accounts (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                amount REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        self.conn.commit()

    def get_accounts(self) -> List[Account]:
        if not self.conn:
            return []

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        rows = cursor.fetchall()
        return [Account(row['id'], row['name'], row['type'], row['balance']) for row in rows]

    def get_categories(self) -> List[Category]:
        if not self.conn:
            return []

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        return [Category(row['id'], row['name']) for row in rows]

    def get_transactions(self) -> List[Transaction]:
        if not self.conn:
            return []

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.*, c.name as category_name
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            ORDER BY t.date DESC
        """)
        rows = cursor.fetchall()
        return [Transaction(row['id'], row['description'], row['amount'], row['date'], row['account_id'], row['category_id'], row['category_name']) for row in rows]

    def get_budgets(self) -> List[Budget]:
        if not self.conn:
            return []

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.*, c.name as category_name
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
        """)
        rows = cursor.fetchall()
        return [Budget(row['id'], row['category_id'], row['amount'], row['start_date'], row['end_date'], row['category_name']) for row in rows]

    def insert_dummy_data(self) -> None:
        if not self.conn:
            return

        cursor = self.conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM accounts")
        cursor.execute("DELETE FROM categories")

        # Insert dummy accounts
        accounts = [
            ('Checking Account', 'Checking', 8123.45),
            ('Savings Account', 'Savings', 7087.05),
            ('Primary Credit Card', 'Credit Card', -800.00),
            ('Investment Portfolio', 'Investment', 110219.50)
        ]
        cursor.executemany("INSERT INTO accounts (name, type, balance) VALUES (?, ?, ?)", accounts)

        # Insert dummy categories
        categories = [
            ('Groceries',),
            ('Salary',),
            ('Utilities',),
            ('Transport',)
        ]
        cursor.executemany("INSERT INTO categories (name) VALUES (?)", categories)

        # Insert dummy transactions
        transactions = [
            ('SuperMart', -85.50, '2024-06-28', 1, 1),
            ('Monthly Salary', 4500.00, '2024-06-27', 1, 2),
            ('Utility Bill', -120.00, '2024-06-26', 1, 3),
            ('Public Transport', -22.75, '2024-06-25', 2, 4)
        ]
        cursor.executemany("INSERT INTO transactions (description, amount, date, account_id, category_id) VALUES (?, ?, ?, ?, ?)", transactions)

        self.conn.commit()

    def add_transaction(self, description: str, amount: float, date: str, account_id: int, category_id: int) -> None:
        if not self.conn:
            return

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (description, amount, date, account_id, category_id) VALUES (?, ?, ?, ?, ?)",
            (description, amount, date, account_id, category_id)
        )
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        self.conn.commit()

    def update_transaction(self, transaction_id: int, description: str, amount: float, date: str, account_id: int, category_id: int) -> None:
        if not self.conn:
            return

        cursor = self.conn.cursor()
        # First, revert the old transaction amount from the account balance
        cursor.execute("SELECT amount, account_id FROM transactions WHERE id = ?", (transaction_id,))
        old_transaction = cursor.fetchone()
        if old_transaction:
            old_amount = old_transaction['amount']
            old_account_id = old_transaction['account_id']
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (old_amount, old_account_id))

        # Update the transaction
        cursor.execute(
            "UPDATE transactions SET description = ?, amount = ?, date = ?, account_id = ?, category_id = ? WHERE id = ?",
            (description, amount, date, account_id, category_id, transaction_id)
        )

        # Apply the new transaction amount to the new account balance
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        self.conn.commit()

    def delete_transaction(self, transaction_id: int) -> None:
        if not self.conn:
            return

        cursor = self.conn.cursor()
        # Revert the transaction amount from the account balance
        cursor.execute("SELECT amount, account_id FROM transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        if transaction:
            amount = transaction['amount']
            account_id = transaction['account_id']
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))

        # Delete the transaction
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        self.conn.commit()

    def get_total_net_worth(self) -> float:
        if not self.conn:
            return 0.0

        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(balance) as total FROM accounts")
        row = cursor.fetchone()
        return row['total'] if row and row['total'] else 0.0

    def get_total_cash(self) -> float:
        if not self.conn:
            return 0.0

        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(balance) as total FROM accounts WHERE type IN ('Checking', 'Savings')")
        row = cursor.fetchone()
        return row['total'] if row and row['total'] else 0.0

    def get_total_debt(self) -> float:
        if not self.conn:
            return 0.0

        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(balance) as total FROM accounts WHERE type = 'Credit Card'")
        row = cursor.fetchone()
        return abs(row['total']) if row and row['total'] else 0.0

    def add_account(self, name: str, type: str, balance: float) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO accounts (name, type, balance) VALUES (?, ?, ?)", (name, type, balance))
        self.conn.commit()

    def update_account(self, account_id: int, name: str, type: str, balance: float) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("UPDATE accounts SET name = ?, type = ?, balance = ? WHERE id = ?", (name, type, balance, account_id))
        self.conn.commit()

    def delete_account(self, account_id: int) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        self.conn.commit()

    def add_category(self, name: str) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        self.conn.commit()

    def update_category(self, category_id: int, name: str) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
        self.conn.commit()

    def delete_category(self, category_id: int) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()

    def add_budget(self, category_id: int, amount: float, start_date: str, end_date: str) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO budgets (category_id, amount, start_date, end_date) VALUES (?, ?, ?, ?)",
                       (category_id, amount, start_date, end_date))
        self.conn.commit()

    def update_budget(self, budget_id: int, category_id: int, amount: float, start_date: str, end_date: str) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("UPDATE budgets SET category_id = ?, amount = ?, start_date = ?, end_date = ? WHERE id = ?",
                       (category_id, amount, start_date, end_date, budget_id))
        self.conn.commit()

    def delete_budget(self, budget_id: int) -> None:
        if not self.conn:
            return
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        self.conn.commit()

    def get_monthly_summary(self):
        if not self.conn:
            return []

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                strftime('%Y-%m', date) as month,
                SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
                SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) as expenses
            FROM transactions
            GROUP BY month
            ORDER BY month DESC
        """)
        return cursor.fetchall()

    def get_category_summary(self):
        if not self.conn:
            return []

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                c.name as category_name,
                SUM(-t.amount) as total_expenses
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.amount < 0
            GROUP BY c.name
            ORDER BY total_expenses DESC
        """)
        return cursor.fetchall()
