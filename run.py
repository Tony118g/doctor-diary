"""
Main file to run the application.
"""

# Import libraries.
import gspread
from google.oauth2.service_account import Credentials

# Define the APIs used by the program.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("doctor's_diary")

# Variables for each sheet in the spreadsheet.
appointments = SHEET.worksheet("appointments")
visit_history = SHEET.worksheet("visit_history")

# Variables for all data in each sheet.
all_appts = appointments.get_all_values()
all_visits = visit_history.get_all_values()
