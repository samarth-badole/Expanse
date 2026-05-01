# 💸 SpendLens - Expense Tracker

A beautiful, modern expense tracking app that runs entirely in your browser.

> **Note:** This is a **static site** hosted on GitHub Pages. All data is stored locally in your browser using `localStorage`.

## ✨ Features

- Add, view, and delete expenses
- Categorize spending (Food, Transport, Shopping, Bills, Health, Entertainment, Education, Other)
- Monthly spending statistics
- Visual category breakdown with progress bars
- Monthly trend charts
- Indian Rupee (₹) currency support
- Dark theme with gradient accents
- Works offline - no internet required after first load

## 🚀 Live Demo

**👉 [Open SpendLens](https://samarth-badole.github.io/Expanse/)**

Hosted on GitHub Pages - loads instantly.

## 📱 How to Use

1. Open the app at the link above
2. Add your first expense using the form on the right
3. View your spending stats, category breakdown, and monthly trends
4. Data is automatically saved in your browser

**Important**: Data is stored locally in your browser. Clearing browser data will erase all expenses. For backup, you can export your data (feature coming soon) or take screenshots.

## 🛠️ Local Development

Just open `index.html` in any modern browser. No build process required.

```bash
# Clone the repository
git clone https://github.com/samarth-badole/Expanse.git
cd Expanse

# Open index.html in your browser, or use a local server
python -m http.server 8000
# Then visit http://localhost:8000
```

## 📂 Project Structure

```
Expanse/
├── index.html        # Main app (self-contained HTML+CSS+JS)
├── .gitignore        # Git ignore rules
├── .nojekyll         # Disable Jekyll on GitHub Pages
└── README.md         # This file
```

All code lives in a single `index.html` file for easy deployment.

## 🌐 Deployment

This site is automatically deployed to GitHub Pages whenever you push to the `main` branch.

**To enable GitHub Pages for your fork:**
1. Go to repository Settings → Pages
2. Source: Deploy from a branch → `main` → `/ (root)`
3. Save
4. Your site will be at: `https://<username>.github.io/Expanse/`

## 📝 Technical Details

- **Frontend**: Vanilla JavaScript (no frameworks)
- **Storage**: Browser `localStorage` (key: `spendlens_expenses`)
- **Styling**: CSS3 with custom properties, Flexbox & Grid
- **Fonts**: Syne (display), DM Mono (monospace)
- **No build step** - just edit and push

### Data Format

Expenses are stored as JSON in localStorage:

```json
[
  {
    "id": 1712345678901,
    "title": "Lunch",
    "amount": 350,
    "category": "Food",
    "date": "2026-05-01",
    "note": "At cafe"
  }
]
```

## 🔒 Privacy

All data stays in your browser. No server, no tracking, no analytics.

## 📄 License

MIT
