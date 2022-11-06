"""
Main file to run the application.
"""

# Import libraries.
import datetime
from tabulate import tabulate
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

# Variable for sheet in the spreadsheet.
appointments = SHEET.worksheet("appointments")

# Variable for all data in sheet.
all_appts = appointments.get_all_values()

# Global variables used in multiple functions.
current_date = datetime.date.today()


def display_records(records, topic, heads):
    """
    Displays data in a table format using headers and data provided
    as arguments (records and heads) and prints text about the table
    using the argument provided to the topic parameter. If the records
    are empty then it informs the user that no records are available.
    """
    if records == []:
        print(f"There are no appointments booked for {topic}.")
    else:
        print(f"Below are the appointments booked for {topic}.")
        print(tabulate(records, headers=heads, tablefmt="fancy_grid"))


def update_appts(data):
    """
    Updates the appointments sheet using the data provided.
    """
    print("Updating appointments...")
    appointments.append_row(data)
    print("Appointment booked successfully!")


def confirm_appointment(data):
    """
    Presents the user with the appointment details entered
    and asks for final confirmation to make the booking.
    The patient will be asked for input (Y or N) untill 
    the input is valid.
    """
    print("Please confirm the following details before booking.\n")
    print(tabulate([data], headers=all_appts[0], tablefmt="fancy_grid"))
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
        update_appts(data)
    elif confirmation == ("N"):
        collect_details()


def get_appts_for_name(name):
    """
    Gets and returns the appointments booked for the name
    povided as an argument.
    """

    name_appts = []
    for appt in all_appts[1:]:
        appt_name = appt[2:4]
        if appt_name == name:
            name_appts.append(appt)

    return name_appts


def search_name():
    """
    Gets return values of get_name function for both name and surname
    and defines them in a single variable (search_name) as a list
    to pass to get_appts_for_name function and finally passes the
    returned records to the display_records function to be displayed
    along with relevant topic and table headers.
    """

    f_name = get_name("f_name")
    l_name = get_name("l_name")
    search_nme = [f_name, l_name]
    name_appts = get_appts_for_name(search_nme)

    name_desc = f"the name {search_nme}"
    name_heads = ["Date", "Time"]

    display_records(name_appts, name_desc, name_heads)


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

    if required_return == "bookings":
        return bookings
    elif required_return == "booked_times":
        return booked_times


def search_date(specification):
    """
    Defines search_dte variable using current date or returned
    date depending on the argument provided and passes it to
    get_appts_for_date function to get the relevant records to
    pass to the display_records function.
    """
    
    if specification == "today":
        search_dte = datetime.datetime.strftime(current_date, "%d/%m/%Y")
        date_desc = "today"
    elif specification == "search":
        search_dte = get_date()
        date_desc = f"the date {search_dte}"

    dte_heads = ["Time", "Name", "Surname"]
    date_appts = get_appts_for_date(search_dte, "bookings")

    display_records(date_appts, date_desc, dte_heads)


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
        search_date("today")
    elif main_menu_ans == ("3"):
        search_date("search")
    elif main_menu_ans == ("4"):
        search_name()
    elif main_menu_ans == ("5"):
        print("Cancel appointment.")


main_menu()
