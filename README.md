# FinDash - Personal Finance Dashboard

FinDash is a modern and intuitive web application for managing your personal finances. It provides a clear overview of your financial situation, allowing you to track your accounts, transactions, and budgets with ease.

## Features

- **Dashboard:** A comprehensive dashboard that displays your net worth, cash, debt, and a summary of your recent transactions and account balances.
- **Transaction Management:** Add new transactions with descriptions, amounts, dates, accounts, and categories.
- **Account and Category Tracking:** Organize your finances with customizable accounts and categories.
- **Modern UI:** A clean and modern user interface based on the "stitch_dashboard_principal" layout.

## Project Structure

- **`app.py`:** The main Flask application file. It handles routing, database connections, and serves the frontend.
- **`database.py`:** Contains the data models (`Account`, `Category`, `Transaction`) and the `Database` class, which manages all interactions with the SQLite database.
- **`templates/index.html`:** The Jinja2 template for the main dashboard page.
- **`requirements.txt`:** A list of the Python dependencies required to run the project.
- **`.gitignore`:** A file that specifies which files and directories should be ignored by Git.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.
