"""
Main file to run the application.
"""

# Import libraries/packages.
import os
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

# Global variables used in multiple functions.

# Variable for sheet in the spreadsheet.
appointments = SHEET.worksheet("appointments")
# Variable for all data in appointments sheet.
all_appts = appointments.get_all_values()
# Stores the current date.
current_date = datetime.date.today()
# Places and stores the current date into the correct format for the program.
current_date_fmted = datetime.datetime.strftime(current_date, "%d/%m/%Y")


def clear_tmnl():
    """
    Clears the terminal when called.
    """
    os.system("clear")  # Idea taken from a post on slack.


def display_records(records, topic, heads, reason):
    """
    Displays data in a table format using headers and data provided
    as arguments (records and heads) and prints text about the table
    using the argument provided to the topic parameter. If the records
    are empty then it informs the user that no records are available.
    """
    clear_tmnl()
    if records == []:
        print(f"There are no appointments booked for {topic}.")
    else:
        print(f"Below are the appointments booked for {topic}.")
        print(tabulate(records, headers=heads, tablefmt="fancy_grid"))

    if reason == "view":
        print("Press 1 for search menu or 2 for main menu.")
        while True:
            after_view_ans = input("\n")
            if after_view_ans not in ("1", "2"):
                print("Invalid input.")
                print("Please choose an option between 1 and 2")
            else:
                break

        if after_view_ans == ("1"):
            search_menu()
        elif after_view_ans == ("2"):
            main_menu()
      
    elif reason == "cancelation":
        pass


def update_appts(data):
    """
    Updates the appointments sheet using the data provided.
    """
    print("Updating appointments...")
    appointments.append_row(data, value_input_option='USER_ENTERED')
    print("Appointment booked successfully!")


def book_again_prompt(status):
    """
    Provides user with option to either re-enter details
    or enter details for a new booking depending on
    the confirmation status.
    """
    clear_tmnl()
    if status == "terminated":
        prompt = "Enter new details"
    elif status == "booked":
        prompt = "Book another appointment"
       
    print(f"(1) {prompt}.")
    print("(2) Return to main menu.")

    while True:
        re_book_ans = input("")
        if re_book_ans not in ("1", "2"):
            print("Invalid, enter options 1 or 2.")
        else:
            break
    
    if re_book_ans == "1":
        collect_details()
    elif re_book_ans == "2":
        main_menu()


def confirm_appointment(data):
    """
    Presents the user with the appointment details entered
    and asks for final confirmation to make the booking.
    The patient will be asked for input (Y or N) untill 
    the input is valid.
    """
    clear_tmnl()
    print("Please confirm the following details before booking.\n")
    print(tabulate([data], headers=all_appts[0], tablefmt="fancy_grid"))
    print("Enter Y to proceed or N to cancel and re-enter details.\n")
    print("WARNING!")
    print("Entering 'N' will cancel the appointment and data will be lost.")

    while True:
        confirmation = input("\n")
        if confirmation not in ("Y", "N"):
            print("Please input a valid option (Y/N).")
        else:
            break

    if confirmation == ("Y"):
        update_appts(data)
        book_again_prompt("booked")
    elif confirmation == ("N"):
        book_again_prompt("terminated")


def get_appts_for_name(name):
    """
    Gets and returns the appointments booked for the name
    povided as an argument.
    """

    name_appts = []
    for appt in all_appts[1:]:
        appt_name = appt[2:4]
        if appt_name == name:
            name_appt_row = [all_appts.index(appt) + 1]
            name_appt = appt + name_appt_row
            name_appts.append(name_appt)

    return name_appts


def search_name(reason):
    """
    Gets return values of get_name function for both name and surname
    and defines them in a single variable (search_name) as a list
    to pass to get_appts_for_name function and finally passes the
    returned records to the display_records function to be displayed
    along with relevant topic and table headers.
    """
    clear_tmnl()
    f_name = get_name("f_name")
    l_name = get_name("l_name")
    search_nme = [f_name, l_name]
    name_appts = get_appts_for_name(search_nme)

    name_recs = []
    for name_appt in name_appts:
        name_rec = name_appt[0:2]
        name_recs.append(name_rec)

    name_desc = f"the name {' '.join(search_nme)}"
    name_heads = ["Date", "Time"]

    display_records(name_recs, name_desc, name_heads, reason)
    return name_appts


def get_name(name_part):
    """
    Gets the patient's name input by the user and validates
    that it contains only letters and no spaces.
    """
    clear_tmnl()
    if name_part == ("f_name"):
        name_prompt = "first name"
    elif name_part == ("l_name"):
        name_prompt = "surname:"

    print(f"Please enter the patients {name_prompt}")

    while True:
        pat_name = input("\n").capitalize()
        if pat_name.isalpha():
            break
        else:
            print("Please enter a name without spaces using only letters.")

    return pat_name


def cancel_appt(appointment):
    """
    Gets the row number of the appointment to cancel
    and deletes the row from the appointments sheet
    if the user provides final confirmation.
    """
    clear_tmnl()
    print(f"Appointment cancelation for {appointment[2]} on {appointment[0]}")
    print("Enter 1 to proceed or 2 to stop the cancelation.")

    while True:
        cncl_confirmation = input("\n")
        if cncl_confirmation not in ("1", "2"):
            print("Invalid, enter an option 1 or 2.")
        elif cncl_confirmation == "2":
            main_menu()
            break
        elif cncl_confirmation == "1":
            row_to_dlte = appointment[-1]
            appointments.delete_rows(row_to_dlte)
            break


def cancelation_prompt():
    """
    Calls the search_name function to get bookings relative to searched name
    and presents them to the user. Prompts the user to enter a valid date of
    booking they wish to cancel both for selection in case of multiple choices
    and for confirmation of cancelation.
    """
    clear_tmnl()
    appt_opts = search_name("cancelation")
    if bool(appt_opts) is False:
        print("Press 1 to search again or 2 to return to menu.")
        while True:
            search_again_ans = input("\n")
            if search_again_ans not in ("1", "2"):
                print("Invalid, enter an option 1 or 2.")
            elif search_again_ans == "1":
                cancelation_prompt()
                break
            elif search_again_ans == "2":
                main_menu()
                break
    else:
        date_opts = []
        for appt in appt_opts:
            date_opt = appt[0]
            date_opts.append(date_opt)
            
        print("Input the booking date you intend to cancel for confirmation.")
        while True:
            cncl_opt = get_date()
            if cncl_opt not in date_opts:
                print("Invalid choice, enter one of the booked dates.")
            else:
                break

        appt_to_cncl = None
        for appt_opt in appt_opts:
            if str(cncl_opt) in appt_opt:
                appt_to_cncl = appt_opt

        cancel_appt(appt_to_cncl)


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


def search_date(specification, reason):
    """
    Defines search_dte variable using current date or returned
    date depending on the argument provided and passes it to
    get_appts_for_date function to get the relevant records to
    pass to the display_records function.
    """
    clear_tmnl()
    if specification == "today":
        search_dte = current_date_fmted
        date_desc = "today"
    elif specification == "search":
        search_dte = get_date()
        date_desc = f"the date {search_dte}"

    dte_heads = ["Time", "Name", "Surname"]
    date_appts = get_appts_for_date(search_dte, "bookings")

    date_recs = []
    for date_appt in date_appts:
        date_rec = date_appt[1:4]
        date_recs.append(date_rec)

    display_records(date_recs, date_desc, dte_heads, reason)


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
    if data == current_date_fmted:
        current_time = datetime.datetime.now().strftime("%H%M")
        today_av_times = [time for time in av_times if time > current_time]
        return today_av_times
    else:
        return av_times


def get_time(data):
    """
    Provides a list of available times and requests input for desired time.
    It then validates whether it is one of the provided options and will
    request input untill valid data is provided by the user.
    """
    clear_tmnl()
    times = get_avail_times(data)
    print("Please enter one of the available times.")

    while True:
        print(f"Available times are:\n{', '.join(times)}")
        time_input = input("\n")
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
    clear_tmnl()
    print("Please enter appointment date in format dd/mm/yyyy.")

    while True:
        date_input = input("\n")
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


def check_existing_appts(details):
    """
    Check the appointment records for the name and date
    provided and if a booking already exists for the details,
    returns false. Otherwise returns true.
    """
    detail_date = details[0]
    detail_name = details[2:4]
    date_bookings = get_appts_for_date(detail_date, "bookings")

    for booking in date_bookings:
        if set(detail_name).issubset(booking):
            return True
        else:
            return False


def collect_details():
    """
    Collects the patients details from other functions
    and adds them to a list that can be appended to the
    appointments sheet.
    """
    clear_tmnl()
    print("Please enter the relevant details for each category that appears.")
    appt_categories = appointments.row_values(1)
    appt_detail = dict.fromkeys(appt_categories)

    appt_detail["Date"] = get_date()
    appt_detail["Time"] = get_time(appt_detail["Date"])
    appt_detail["Name"] = get_name("f_name")
    appt_detail["Surname"] = get_name("l_name")

    appt_details = list(appt_detail.values())
    existing_appt_check = check_existing_appts(appt_details)
    if existing_appt_check is True:
        print("A booking for this patient already exists on this date.")
        print("You can only book one appointment per day per patient.")
        book_again_prompt("terminated")
    else:
        confirm_appointment(appt_details)


def app_info():
    """
    Provides the user with instructions on how to use the app.
    Once the user has read and is satisfied, they may press enter
    to return to the main menu.
    """
    clear_tmnl()
    print("Doctor's diary is designed to make managing appointments simple!\n")

    print("To book an appointment:-\n")
    print("1 - Select option '(1)' in the menu.")
    print("2 - Enter the details that are requested one by one.")
    print("3 - Confirm the details to book or cancel the booking.")
    print("NB - You can enter 'E' at any stage to stop and return to menu.\n")

    print("To view today's appointments, select option '(2)' in the menu.\n")

    print("To search for specific appointments:-\n ")
    print("1 - Select option '(3)' in main menu to go to the search menu.")
    print("2 - Select between options to search for a name or a date.")
    print("3 - Enter the name/date you wish to search for.")
    print("4 - View the results of your search.\n")

    print("To cancel an appointment:-\n")

    print("1 - Select option '(4)' in the menu.")
    print("2 - Enter the name and surname you wish to cancel for one by one.")
    print("3 - Enter the appointment date to cancel to select/confirm.")
    print("4 - Provide final confirmation to cancel the appointment.")

    input("Press enter to return to menu\n")
    main_menu()


def search_menu():
    """
    Displays options to search by date, by name or return to main menu.
    """
    clear_tmnl()
    print("What would you like to do?\n")

    print("(1) Search appointments by name.")
    print("(2) Search appointments by date.")
    print("(3) Return to main menu.")

    while True:
        search_ans = input("\n")
        if search_ans not in ("1", "2", "3"):
            print("Invalid input.")
            print("Please choose an option between 1 and 2")
        else:
            break

    if search_ans == ("1"):
        search_name("view")
    elif search_ans == ("2"):
        search_date("search", "view")
    elif search_ans == ("3"):
        main_menu()


def main_menu():
    """
    Displays the main menu options for the user
    to select in order to navigate the application.
    """
    clear_tmnl()
    print("Welcome to Doctor's Diary!\n")
    print("Please select an option below.\n")
    
    print("(1) Book new appointment.")
    print("(2) View today's appointments.")
    print("(3) Search appointments.")
    print("(4) Cancel appointment.")
    print("(5) View application information.")

    while True:
        main_menu_ans = input("\n")
        if main_menu_ans not in ("1", "2", "3", "4", "5"):
            print("Invalid input.")
            print("Please choose an option between 1 and 5")
        else:
            break

    if main_menu_ans == ("1"):
        collect_details()
    elif main_menu_ans == ("2"):
        search_date("today", "view")
    elif main_menu_ans == ("3"):
        search_menu()
    elif main_menu_ans == ("4"):
        cancelation_prompt()
    elif main_menu_ans == ("5"):
        app_info()


main_menu()
