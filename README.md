# 📊 IBKR Gmail Trade Importer

Automatically fetch your Interactive Brokers trade confirmation emails from Gmail and append them to a Google Sheets spreadsheet for tracking and analysis.

> 💡 Works without labels, but optionally supports Gmail label filtering.
> 🎯 Compatible with `BOUGHT` / `SOLD` email formats from Interactive Brokers.

---

## 🔧 Installation
📦 Install Python & pip (if missing)
Make sure Python 3 and pip are installed:
macOS (using Homebrew):
```bash
brew install python
```

Ubuntu / Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip
```
Windows:
```bash
Download Python installer
During install, check “Add Python to PATH”
```

Confirm pip is available:
```bash
pip --version
```

Clone the repo and install dependencies:

```bash
git clone https://github.com/danielshaulov1/IBKR-Trade-Tracker.git
cd IBKR-Trade-Tracker
python3 -m pip install -r requirements.txt
```

---

## ⚙️ Setup

1. **Enable APIs**
   - Go to: https://console.cloud.google.com/
   - Create a new project.
   - Enable:
     - Gmail API
     - Google Sheets API

2. **🔐 How to generate `client_secret.json`**
   1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
   2. Create a new project or select an existing one.
   3. Navigate to **APIs & Services > Credentials**.
   4. Click **Create Credentials > OAuth Client ID**.
   5. Choose **Desktop App** as the application type.
   6. Download the JSON and rename it to `client_secret.json`.
   7. Save this file in the same directory as your script.


3. **Authorize token**
   ```bash
   python generate_token.py
   ```
   It will prompt your browser to log in and authorize access.
   This will create `token.json`.

---

## 📁 Google Sheets Structure

Use the ready-to-use Google Sheets template to track your trades:

🔗 [Click here to open the sheet template](https://docs.google.com/spreadsheets/d/1LXaW6vJzmrlqaLyOZGVJnye97EwmJ92IkVHccgb5MV8/edit?usp=sharing)

- Make a copy: `File` → `Make a copy` to use it with your own account.
- Update the `SHEET_ID` in your `.env` file accordingly.
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

If you organize your emails using a Gmail label (like `Interactive Brokers`), set it in your `.env` file :

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
