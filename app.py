from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)

# Railway storage strategy
# Railway provides ephermeral filesystem + optional persistent volumes
# Use volume if available, otherwise fall back to /tmp (ephemeral but writable)
RAILWAY_VOLUME = os.getenv('RAILWAY_VOLUME_PATH')
RAILWAY_TEMP = os.getenv('RAILWAY_TEMP_DIR', '/tmp')

def get_db_path():
    """Resolve database path with Railway volume support."""
    if RAILWAY_VOLUME:
        # Persistent volume (survives restarts)
        try:
            os.makedirs(RAILWAY_VOLUME, exist_ok=True)
            return os.path.join(RAILWAY_VOLUME, 'expenses.db')
        except Exception as e:
            print(f"[WARN] Cannot use volume: {e}, falling back to temp")
    
    # Ephemeral temp directory
    try:
        os.makedirs(RAILWAY_TEMP, exist_ok=True)
        return os.path.join(RAILWAY_TEMP, 'expenses.db')
    except:
        # Last resort: current directory (may be read-only on some platforms)
        return os.path.join(os.getcwd(), 'expenses.db')

DB_PATH = get_db_path()
print(f"[INFO] Database path: {DB_PATH}")

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Education", "Other"]

def get_db():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        raise

def init_db():
    try:
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
        print(f"[INFO] Database initialized at {DB_PATH}")
    except Exception as e:
        print(f"[ERROR] Database init failed: {e}")
        raise

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
