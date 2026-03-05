import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp
from pathlib import Path
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
BASE_DIR = Path(__file__).resolve().parent
CREDS_FILE = BASE_DIR / "creds.local.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDS_FILE.as_posix(),
    scope
)
client = gspread.authorize(creds)

sheet = client.open("AutoOutreach").sheet1   
data = sheet.get_all_records() 

#read latest
# src/sheets/client.py

def get_todo_rows():
    """
    returns: list of dicts, one per row where status == 'to do'
    """
    all_rows = sheet.get_all_records()
    todo_rows = []
    for idx, row in enumerate(all_rows, start=2):  # gspread is 1-indexed, header is row 1
        if row.get("status", "").strip().lower() == "to do":
            row_copy = row.copy()
            row_copy["row_id"] = idx
            todo_rows.append(row_copy)
    return todo_rows


def mark_done(row_id,sheet):
    """
    sets status = 'done' and updates last_contacted to now
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # find column indexes
    headers = sheet.row_values(1)
    status_col = headers.index("status") + 1
    last_contacted_col = headers.index("last_contacted") + 1

    sheet.update_cell(row_id+1, status_col, "done")
    sheet.update_cell(row_id+1, last_contacted_col, now)



#reading entire sheet/row/col/cell

#pp(data)

#row = sheet.row_values(1)
#pp(row)
#col = sheet.col_values(3)
#pp(col)
#cell = sheet.cell(1,2).value

#writing in sheet
#insertRow = ["Guptasanya@gmail.com", "Sam", "HR at outreach", 0, 'Done']

#sheet.insert_row(insertRow,3)  #row insertion
#sheet.delete_rows(2,2)     #row deletion