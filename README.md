# 📊 IBKR Gmail Trade Importer

Automatically fetch your **Interactive Brokers** trade confirmation emails from Gmail and append them to a **Google Sheets spreadsheet** for tracking and analysis.

> 💡 Works without labels, but optionally supports Gmail label filtering.
> 🎯 Compatible with `BOUGHT` / `SOLD` email formats from Interactive Brokers.

---

## 🔧 Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yourusername/ibkr-trade-importer.git
cd ibkr-trade-importer
pip install -r requirements.txt
```

### 📦 Required Python packages

Put this in `requirements.txt`:

```txt
google-api-python-client
google-auth
google-auth-oauthlib
```

---

## ⚙️ Setup

1. **Enable APIs**
   - Go to: https://console.cloud.google.com/
   - Create a new project.
   - Enable:
     - Gmail API
     - Google Sheets API

2. **Create OAuth credentials**
   - Go to **APIs & Services → Credentials**.
   - Click **Create Credentials → OAuth client ID → Desktop App**.
   - Download `client_secret.json` into the project folder.

3. **Authorize token**
   ```bash
   python generate_token.py
   ```
   It will prompt your browser to log in and authorize access.
   This will create `token.json`.

---

## 📁 Google Sheets Structure

Create a spreadsheet with a sheet called `Transactions`:

| A (MessageID) | B (Date) | C (Type) | D (Stock) | E (Units) | F (Price) | G (Fees) |
|---------------|----------|----------|-----------|-----------|-----------|----------|
| `abc123...`   | 2025-07-18 | Buy     | TSLA      | 10        | 123.45    | 1.80     |

Put the **Spreadsheet ID** into your script:
```python
SHEET_ID = 'your-spreadsheet-id-here'
```

---

## 🚀 Run the script

```bash
python main_script.py
```

It will:
- Load messages from Gmail (optionally filtered by label and date)
- Extract trade data from subject lines
- Append to the sheet only if not already present

---

## 📌 Optional: Use Gmail Label

If you organize your emails using a Gmail label (like "Interactive Brokers"), set it in the script:

```python
LABEL_NAME = 'Interactive Brokers'
```

If you want to **use all emails** (not labeled), set it to:

```python
LABEL_NAME = ''
# or
LABEL_NAME = 'ALL'
```

---

## 🔒 Security Notes

- Never commit `token.json` or `client_secret.json` to GitHub.
- Add them to `.gitignore`:
```txt
token.json
client_secret.json
```

---

## ✅ Example Output

```
📩 Gmail returned 14 total messages
✅ New trade: TSLA BOUGHT 10.0 @ 123.45
✅ Wrote row to Transactions!A243:G243
✅ Inserted 1 new rows safely.
```

---

## 🧠 Feature Ideas

- [ ] Live P&L calculator via API (e.g., Yahoo Finance)
- [ ] Automatic chart dashboard with Looker Studio
- [ ] Auto-labeling script

---

## 🏷️ License

MIT

---

## 🤝 Contribute

PRs welcome. Make sure to test with your own Gmail + IBKR setup.

## 🔐 How to generate `client_secret.json`

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials > OAuth Client ID**.
5. Choose **Desktop App** as the application type.
6. Download the JSON and rename it to `client_secret.json`.
7. Save this file in the same directory as your script.
