from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)

# Determine database path - use Railway volume if available for persistence
if os.getenv('RAILWAY_VOLUME_PATH'):
    DB_PATH = os.path.join(os.getenv('RAILWAY_VOLUME_PATH'), 'expenses.db')
else:
    DB_PATH = os.getenv('SQLITE_PATH', 'expenses.db')

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Education", "Other"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            )
        """)
        conn.commit()

@app.route("/")
def index():
    conn = get_db()
    
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    
    expenses = conn.execute(
        "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC",
        (f"{month}%",)
    ).fetchall()
    
    total = sum(e["amount"] for e in expenses)
    
    # Category breakdown
    cat_data = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses WHERE date LIKE ? GROUP BY category",
        (f"{month}%",)
    ).fetchall()
    
    # Monthly summary for last 6 months
    monthly = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
        LIMIT 6
    """).fetchall()
    
    conn.close()
    
    return render_template("index.html",
        expenses=expenses,
        total=total,
        categories=CATEGORIES,
        cat_data=cat_data,
        monthly=monthly,
        current_month=month
    )

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount", 0)
    category = request.form.get("category", "Other")
    exp_date = request.form.get("date", date.today().isoformat())
    note = request.form.get("note", "").strip()
    
    if not title or not amount:
        return redirect(url_for("index"))
    
    with get_db() as conn:
        conn.execute(
            "INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
            (title, float(amount), category, exp_date, note)
        )
        conn.commit()
    
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
    return redirect(url_for("index"))

@app.route("/api/stats")
def api_stats():
    month = request.args.get("month", date.today().strftime("%Y-%m"))
    conn = get_db()
    cat_data = conn.execute(
        "SELECT category, SUM(amount) as total FROM expenses WHERE date LIKE ? GROUP BY category",
        (f"{month}%",)
    ).fetchall()
    conn.close()
    return jsonify([{"category": r["category"], "total": r["total"]} for r in cat_data])

if __name__ == "__main__":
    init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
