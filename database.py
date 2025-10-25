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
    def __init__(self, id: int, description: str, amount: float, date: str, account_id: int, category_id: int):
        self.id = id
        self.description = description
        self.amount = amount
        self.date = date
        self.account_id = account_id
        self.category_id = category_id

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
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        rows = cursor.fetchall()
        return [Transaction(row['id'], row['description'], row['amount'], row['date'], row['account_id'], row['category_id']) for row in rows]

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
