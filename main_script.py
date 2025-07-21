import os, re, datetime, sys, time
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# === CONFIG ===
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]
LABEL_NAME  = ''  # Leave blank or 'ALL' to ignore label filtering
SHEET_ID    = ''  # <-- Add your Google Sheets ID here
SHEET_RANGE = 'Transactions!A2:A1000'
DATE_QUERY  = 'after:2025/01/03'

# === LOAD CREDS ===
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except:
            creds = None

if not creds or not creds.valid:
    print("❌ Missing or invalid token.json; generate it locally first.")
    sys.exit(1)

# === INIT CLIENTS ===
gmail  = build('gmail', 'v1', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)

# === FETCH EXISTING ROWS FROM SHEET (Column A only) ===
res = sheets.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=SHEET_RANGE
).execute()

sheet_rows = res.get('values', [])
existing_ids = set()
empty_row_indices = []

for i in range(999):  # A2 to A1000
    row = sheet_rows[i] if i < len(sheet_rows) else []
    msg_id = row[0] if row else ""
    if msg_id.strip():
        existing_ids.add(msg_id.strip())
    else:
        empty_row_indices.append(i + 2)

# === GET LABEL ID IF SET ===
label_id = None
if LABEL_NAME and LABEL_NAME.upper() != 'ALL':
    labels = gmail.users().labels().list(userId='me').execute().get('labels', [])
    label_id = next((l['id'] for l in labels if l['name'] == LABEL_NAME), None)
    if not label_id:
        print(f"❌ Label not found: {LABEL_NAME}")
        sys.exit(1)

# === GET MESSAGES ===
all_msgs = []
page_token = None
list_args = {
    'userId': 'me',
    'q': DATE_QUERY,
}
if label_id:
    list_args['labelIds'] = [label_id]

while True:
    if page_token:
        list_args['pageToken'] = page_token

    r = gmail.users().messages().list(**list_args).execute()
    all_msgs.extend(r.get('messages', []))
    page_token = r.get('nextPageToken')
    if not page_token:
        break

print(f"📩 Gmail returned {len(all_msgs)} total messages")

# === PARSE MESSAGES ===
rows = []

for mref in all_msgs:
    mid = mref['id']
    if mid in existing_ids:
        continue

    try:
        msg = gmail.users().messages().get(userId='me', id=mid).execute()
    except Exception as e:
        continue  # Skip fetch errors silently

    subj = next((h['value'] for h in msg['payload']['headers'] if h['name'] == 'Subject'), '')
    m = re.search(r'(BOUGHT|SOLD)\s+([\d.,]+)\s+([A-Z. ]+?)\s+@\s+([\d.]+)', subj)
    if not m:
        continue  # Skip regex mismatch silently

    act, qty, sym, pr = m.groups()

    # Normalize qty: remove commas, allow float
    qty = float(qty.replace(',', ''))

    ts = int(msg['internalDate']) / 1000
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

    rows.append([
        mid,
        date,
        'Buy' if act == 'BOUGHT' else 'Sell',
        sym,
        int(qty),
        float(pr),
        '1.80'
    ])

    print(f"✅ New trade: {sym} {act} {qty} @ {pr}")

if not rows:
    print("ℹ️ No new trades to append.")

# === BATCH INSERT WITH PAUSE TO AVOID 429 ERROR ===
rows.reverse()
if len(empty_row_indices) < len(rows):
    print("❌ Not enough empty rows in sheet. Add more.")
    sys.exit(1)

for i, (row_data, row_num) in enumerate(zip(rows, empty_row_indices)):
    range_str = f'Transactions!A{row_num}:G{row_num}'
    try:
        sheets.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=range_str,
            valueInputOption='USER_ENTERED',
            body={'values': [row_data]}
        ).execute()
        print(f"✅ Wrote row to {range_str}")
    except Exception as e:
        print(f"❌ Failed writing to {range_str}: {e}")
        break

    if i % 10 == 0 and i > 0:
        print("⏳ Rate limit protection: sleeping 10 seconds …")
        time.sleep(10)

print(f"✅ Inserted {len(rows)} new rows safely.")
