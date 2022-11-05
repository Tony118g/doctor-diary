"""
Main file to run the application.
"""

# Import libraries.
import datetime
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

# Global variables used in multiple functions.
current_date = datetime.date.today()


def confirm_appointment(data):
    """
    Presents the user with the appointment details entered
    and asks for final confirmation to make the booking.
    The patient will be asked for input (Y or N) untill 
    the input is valid.
    """
    print("Please confirm the following details before booking.\n")
    print(f"{data}\n")
    print("Enter Y to proceed or N to cancel and re-enter details.\n")
    print("WARNING!")
    print("Entering 'N' will cancel the appointment and data will be lost.")

    while True:
        confirmation = input("")
        if confirmation not in ("Y", "N"):
            print("Please input a valid option (Y/N).")
        else:
            break

    if confirmation == ("Y"):
        print("confirmed")
    elif confirmation == ("N"):
        collect_details()


def get_name(name_part):
    """
    Gets the patient's name input by the user and validates
    that it contains only letters and no spaces.
    """
    if name_part == ("f_name"):
        name_prompt = "first name"
    elif name_part == ("l_name"):
        name_prompt = "surname:"

    print(f"Please enter the patients {name_prompt}")

    while True:
        pat_name = input("").capitalize()
        if pat_name.isalpha():
            break
        else:
            print("Please enter a name without spaces using only letters.")

    return pat_name


def get_appts_for_date(data, required_return):
    """
    Gets the booked appointments for the data argument provided
    and returns the requested data depending on the argument given
    for the required_return parameter.
    """
    date_appts = appointments.findall(data)

    bookings = []
    booked_times = []
    for date_appt in date_appts:
        booking = appointments.row_values(date_appt.row)
        booked_time = booking[1]
        bookings.append(booking)
        booked_times.append(booked_time)

    if required_return == "Bookings":
        return bookings
    elif required_return == "booked_times":
        return booked_times


def get_avail_times(data):
    """
    Gets return value from get_appts_for_date function for booked times
    and removes them from the appointment times list to create
    a list of available times and returns the available times.
    """
    appt_times = ["0800",
                  "0900",
                  "1000",
                  "1100",
                  "1200",
                  "1400",
                  "1500",
                  "1600"
                  ]
    unav_times = get_appts_for_date(data, "booked_times")

    av_times = [time for time in appt_times if time not in unav_times]
    return av_times


def get_time(data):
    """
    Provides a list of available times and requests input for desired time.
    It then validates whether it is one of the provided options and will
    request input untill valid data is provided by the user.
    """
    times = get_avail_times(data)
    print("Please enter one of the available times.")

    while True:
        print(f"Available times are:\n{', '.join(times)}")
        time_input = input("")
        if time_input not in times:
            print(f"{time_input} is not a valid option.")
            print("Please enter one of the available times in 24hr format")
        else:
            return time_input


def get_date():
    """
    Gets the date input by the user and validates
    that it is in correct format as well as not a past date.
    """
    print("Please enter appointment date in format dd/mm/yyyy.")

    while True:
        date_input = input("")
        try:
            date_fm = datetime.datetime.strptime(date_input, "%d/%m/%Y").date()
        except ValueError:
            print("Incorrect data format, should be dd/mm/yyyy")
        else:
            date_available = bool(get_avail_times(date_input))
            if date_available is False:
                print(f"Sorry, {date_input} is unavailable.")
                print("Please enter a new date.")
            else:
                if current_date > date_fm:
                    print("Invalid date, please enter present or future date.")
                else:
                    return date_input


def collect_details():
    """
    Collects the patients details from other functions
    and adds them to a list that can be appended to the
    appointments sheet.
    """
    print("Please enter the relevant details for each category that appears.")
    appt_categories = appointments.row_values(1)
    appt_detail = dict.fromkeys(appt_categories)

    appt_detail["Date"] = get_date()
    appt_detail["Time"] = get_time(appt_detail["Date"])
    appt_detail["Name"] = get_name("f_name")
    appt_detail["Surname"] = get_name("l_name")

    appt_details = list(appt_detail.values())
    confirm_appointment(appt_details)


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
        collect_details()
    elif main_menu_ans == ("2"):
        print("Todays appointments.")
    elif main_menu_ans == ("3"):
        print("Search by date.")
    elif main_menu_ans == ("4"):
        print("Search by name.")
    elif main_menu_ans == ("5"):
        print("Cancel appointment.")


main_menu()
