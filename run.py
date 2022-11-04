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


def main_menu():
    """
    Displays the main menu options for the user
    to select in order to navigate the application.
    """
    print("Welcome to Dentist's Diary!")
    print("Please select an option below.")

    print("(1) Book new appointment.")
    print("(2) View today's appointments.")
    print("(3) Search appointments by date.")
    print("(4) Search appointments by name.")
    print("(5) Cancel appointment.")

    while True:
        main_menu_ans = input("")
        if main_menu_ans not in ("1", "2", "3", "4", "5"):
            print("Invalid input.")
            print("Please choose an option between 1 and 5")
        else:
            break

    if main_menu_ans == ("1"):
        print("Booking option.")
    elif main_menu_ans == ("2"):
        print("Todays appointments.")
    elif main_menu_ans == ("3"):
        print("Search by date.")
    elif main_menu_ans == ("4"):
        print("Search by name.")
    elif main_menu_ans == ("5"):
        print("Cancelo appointment.")


main_menu()
