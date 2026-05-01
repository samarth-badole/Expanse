# SpendLens - Expense Tracker

A beautiful, modern expense tracking web application built with Flask and SQLite.

## Features

- Add, view, and delete expenses
- Categorize spending (Food, Transport, Shopping, Bills, Health, Entertainment, Education, Other)
- Monthly spending statistics
- Visual category breakdown with progress bars
- Monthly trend charts
- Indian Rupee (₹) currency support
- Dark theme with gradient accents

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Jinja2 templates, CSS3 with custom properties, vanilla JavaScript
- **Deployment**: Railway / Render / PythonAnywhere

## Live Demo

**🚀 [Click here to use the live app](https://samarth-badole.up.railway.app)**

*(Deployed on Railway)*

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup

```bash
# Navigate to the project
cd expense-main/expense_tracker

# Install dependencies
pip install -r requirements.txt

# Initialize database (auto-runs on first request)
python app.py
```

Open http://localhost:5000 in your browser.

## Deployment

### Railway (Easiest - 1 click)

1. Fork this repository
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Select your forked repo
5. Done! Your app is live

**Or manually:**
```bash
# Install Railway CLI
pip install railway-cli

# Login and deploy
railway login
railway init
railway up
```

### Render

1. Create account at render.com
2. New Web Service → Connect GitHub repo
3. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy

## File Structure

```
expense_tracker/
├── app.py                 # Flask application (routes, DB logic)
├── expenses.db           # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
├── Procfile              # Deployment configuration
├── templates/
│   └── index.html       # Main frontend template
└── static_index.html    # Static landing page (GitHub Pages)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage with expense list |
| POST | `/add` | Add new expense |
| POST | `/delete/<id>` | Delete expense |
| GET | `/api/stats?month=YYYY-MM` | JSON category breakdown |

## Database Schema

```sql
CREATE TABLE expenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  amount REAL NOT NULL,
  category TEXT NOT NULL,
  date TEXT NOT NULL,
  note TEXT
);
```

## Customization

### Add new category
Edit `CATEGORIES` list in `app.py` line 9.

### Change currency
Replace `₹` symbol in `templates/index.html` with your preferred currency.

### Modify theme colors
Edit CSS variables in `templates/index.html` under `:root`:
```css
--accent: #7c6aff;    /* Primary purple */
--accent2: #ff6a9e;   /* Secondary pink */
```

## License

MIT
