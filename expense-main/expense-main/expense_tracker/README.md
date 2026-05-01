# 💸 SpendLens — Expense Tracker

A clean, dark-themed expense tracker web app built with Flask + SQLite.

## Features
- Add / delete expenses with title, amount, category, date, note
- Filter expenses by month
- Category breakdown with visual bars
- Monthly spending trend chart
- 4 summary stats cards
- Indian Rupee (₹) formatting

## Project Structure
```
expense_tracker/
├── app.py              # Flask backend
├── requirements.txt    # Dependencies
├── expenses.db         # SQLite DB (auto-created)
└── templates/
    └── index.html      # Frontend UI
```

## Setup & Run

### 1. Install dependencies
```bash
npm install
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Main dashboard |
| POST | `/add` | Add new expense |
| POST | `/delete/<id>` | Delete expense |
| GET | `/api/stats?month=YYYY-MM` | JSON category stats |

## How to Extend
- Add user authentication (Flask-Login)
- Add export to CSV feature
- Add budget limits per category
- Add recurring expenses
- Deploy to Heroku / Railway
