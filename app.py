from flask import Flask, jsonify, render_template, request, redirect, url_for
from database import Database
from typing import Dict, Any

app = Flask(__name__)
db = Database('finance.db')

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
    return render_template('index.html', accounts=accounts, categories=categories, transactions=transactions)

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

if __name__ == '__main__':
    with app.app_context():
        db.connect()
        db.create_tables()
        db.insert_dummy_data()
        db.close()
    app.run(debug=True)
