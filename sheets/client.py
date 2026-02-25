import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint as pp
from pathlib import Path

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
BASE_DIR = Path(__file__).resolve().parent
CREDS_FILE = BASE_DIR / "creds.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    CREDS_FILE.as_posix(),
    scope
)
client = gspread.authorize(creds)

sheet = client.open("AutoOutreach").sheet1   
data = sheet.get_all_records() 
#reading entire sheet/row/col/cell

#pp(data)

row = sheet.row_values(1)
#pp(row)
col = sheet.col_values(3)
#pp(col)
cell = sheet.cell(1,2).value

#writing in sheet
insertRow = ["Guptasanya@gmail.com", "Sam", "HR at outreach", 0, 'Done']
sheet.insert_row(insertRow,3)
sheet.delete_rows(2,2)