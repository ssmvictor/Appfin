from flask import Flask, jsonify, render_template, request, redirect, url_for
from database import Database
from typing import Dict, Any

app = Flask(__name__)
db = Database('finance.db')

# Initialize database on startup
with app.app_context():
    db.connect()
    db.create_tables()
    # Only insert dummy data if the database is empty
    if not db.get_transactions():
        db.insert_dummy_data()
    db.close()

@app.before_request
def before_request() -> None:
    db.connect()

@app.teardown_request
def teardown_request(exception: Any) -> None:
    db.close()

@app.route('/')
def index() -> str:
    accounts = db.get_accounts()
    categories = db.get_categories()
    transactions = db.get_transactions()
    total_net_worth = db.get_total_net_worth()
    total_cash = db.get_total_cash()
    total_debt = db.get_total_debt()
    return render_template('index.html', accounts=accounts, categories=categories, transactions=transactions, total_net_worth=total_net_worth, total_cash=total_cash, total_debt=total_debt)

@app.route('/api/data')
def get_data() -> Dict[str, Any]:
    accounts = db.get_accounts()
    categories = db.get_categories()
    transactions = db.get_transactions()
    return jsonify({
        'accounts': [acc.__dict__ for acc in accounts],
        'categories': [cat.__dict__ for cat in categories],
        'transactions': [trans.__dict__ for trans in transactions]
    })

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    description = request.form['description']
    amount = float(request.form['amount'])
    date = request.form['date']
    account_id = int(request.form['account_id'])
    category_id = int(request.form['category_id'])
    db.add_transaction(description, amount, date, account_id, category_id)
    return redirect(url_for('index'))

@app.route('/update_transaction/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    description = request.form['description']
    amount = float(request.form['amount'])
    date = request.form['date']
    account_id = int(request.form['account_id'])
    category_id = int(request.form['category_id'])
    db.update_transaction(transaction_id, description, amount, date, account_id, category_id)
    return redirect(url_for('transactions'))

@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    db.delete_transaction(transaction_id)
    return redirect(url_for('transactions'))

@app.route('/transactions')
def transactions():
    transactions = db.get_transactions()
    accounts = db.get_accounts()
    categories = db.get_categories()
    return render_template('transactions.html', transactions=transactions, accounts=accounts, categories=categories)

@app.route('/budgets')
def budgets():
    budgets = db.get_budgets()
    categories = db.get_categories()
    return render_template('budgets.html', budgets=budgets, categories=categories)

@app.route('/add_budget', methods=['POST'])
def add_budget():
    category_id = int(request.form['category_id'])
    amount = float(request.form['amount'])
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    db.add_budget(category_id, amount, start_date, end_date)
    return redirect(url_for('budgets'))

@app.route('/update_budget/<int:budget_id>', methods=['POST'])
def update_budget(budget_id):
    category_id = int(request.form['category_id'])
    amount = float(request.form['amount'])
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    db.update_budget(budget_id, category_id, amount, start_date, end_date)
    return redirect(url_for('budgets'))

@app.route('/delete_budget/<int:budget_id>')
def delete_budget(budget_id):
    db.delete_budget(budget_id)
    return redirect(url_for('budgets'))

@app.route('/reports')
def reports():
    monthly_summary = db.get_monthly_summary()
    category_summary = db.get_category_summary()
    return render_template('reports.html', monthly_summary=monthly_summary, category_summary=category_summary)

@app.route('/settings')
def settings():
    accounts = db.get_accounts()
    categories = db.get_categories()
    return render_template('settings.html', accounts=accounts, categories=categories)

@app.route('/add_account', methods=['POST'])
def add_account():
    name = request.form['name']
    type = request.form['type']
    balance = float(request.form['balance'])
    db.add_account(name, type, balance)
    return redirect(url_for('settings'))

@app.route('/update_account/<int:account_id>', methods=['POST'])
def update_account(account_id):
    name = request.form['name']
    type = request.form['type']
    balance = float(request.form['balance'])
    db.update_account(account_id, name, type, balance)
    return redirect(url_for('settings'))

@app.route('/delete_account/<int:account_id>')
def delete_account(account_id):
    db.delete_account(account_id)
    return redirect(url_for('settings'))

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    db.add_category(name)
    return redirect(url_for('settings'))

@app.route('/update_category/<int:category_id>', methods=['POST'])
def update_category(category_id):
    name = request.form['name']
    db.update_category(category_id, name)
    return redirect(url_for('settings'))

@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    db.delete_category(category_id)
    return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(debug=True)
