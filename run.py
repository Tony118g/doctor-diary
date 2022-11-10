"""
Main file to run the application.
"""

# Import libraries/packages.
import os
import datetime
import pyinputplus as pyip
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

# Global variables for app processes.

# Variable for sheet in the spreadsheet.
APPTS = SHEET.worksheet("appointments")
# Stores the current date.
CURRENT_DATE = datetime.date.today()
# Places and stores the current date into the correct format for when required.
CURRENT_DATE_FMTED = datetime.datetime.strftime(CURRENT_DATE, "%d/%m/%Y")


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
        search_date("today")
    elif main_menu_ans == ("3"):
        search_menu()
    elif main_menu_ans == ("4"):
        cancelation_prompt()
    elif main_menu_ans == ("5"):
        app_info()


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
        search_date("search")
    elif search_ans == ("3"):
        main_menu()


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
    print("NB - You can enter 'Exit' at any stage to stop and return to menu.\n")

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


def collect_details():
    """
    Collects the patients details from other functions
    and adds them to a list that can be appended to the
    appointments sheet after being checked and confirmed.
    """
    clear_tmnl()
    print("Please enter the relevant details for each category that appears.")
    appt_categories = APPTS.row_values(1)
    appt_detail = dict.fromkeys(appt_categories)

    appt_detail["Date"] = get_date()
    appt_detail["Time"] = get_time(appt_detail["Date"])
    appt_detail["Name"] = get_name("f_name")
    appt_detail["Surname"] = get_name("l_name")

    appt_details = list(appt_detail.values())
    existing_appt_check = check_existing_appts(appt_details)
    if existing_appt_check:
        clear_tmnl()
        print("A booking for this patient already exists on this date.")
        print("You can only book one appointment per day per patient.")
        book_again_prompt("terminated")
    else:
        confirm_appointment(appt_details)


def get_date():
    """
    Gets the date input from the user and validates that it is in correct
    format, is not a past date and is available for booking. Requests
    input untill it is valid or returns to menu if 'Exit' is input.
    """
    clear_tmnl()
    print("Please enter appointment date in format dd/mm/yyyy.")

    while True:
        date_input = input("\n").capitalize()
        if date_input == "Exit":
            main_menu()
            break
        else:
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
                    if CURRENT_DATE > date_fm:
                        print("Invalid date, please enter present or future date.")
                    else:
                        return date_input


def get_time(data):
    """
    Provides list options of available times and requests input for desired
    time.If only one time, prompts user to continue or enter a new date.
    Requests input untill it is valid or returns to menu if 'Exit' is input.
    """
    clear_tmnl()
    times = get_avail_times(data)
    if len(times) == 1:
        print(f"The only available time on {data} is {times[0]}.\n")
        print("Press 1 to continue with this time or 2 to enter new a date.")
        while True:
            time_ans = input("")
            if time_ans not in ("1", "2"):
                print("invalid, pick one or two.")
            elif time_ans == "1":
                time_input = times[0]
                return time_input
            else:
                collect_details()
    else:
        print(f"Below is a list of avaliable times for {data}.\n")
        time_input = pyip.inputMenu(times,
                                    prompt="Select a time from the list.\n",
                                    numbered=True,
                                    allowRegexes=[("Exit"), ("exit")]
                                    )
        if time_input.capitalize() == "Exit":
            main_menu()
        else:
            return time_input


def get_avail_times(data):
    """
    Gets return value from get_appts_for_date function for booked times
    and removes them from the appointment times list to create
    a list of available times and returns the available times.
    If current date, past times are removed from available times.
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
    if data == CURRENT_DATE_FMTED:
        current_time = datetime.datetime.now().strftime("%H%M")
        today_av_times = [time for time in av_times if time > current_time]
        return today_av_times
    else:
        return av_times


def get_name(name_part):
    """
    Gets the name input from user and validates that it contains
    only letters, no spaces and at least 2 letters in length.
    If user inputs 'Exit', it returns them to menu. Input is 
    requested until it is valid.
    """
    clear_tmnl()
    if name_part == ("f_name"):
        name_prompt = "first name"
    elif name_part == ("l_name"):
        name_prompt = "surname:"

    print(f"Please enter the patients {name_prompt}")

    while True:
        pat_name = input("\n").capitalize()
        if pat_name.isalpha() and len(pat_name) > 1:
            break
        else:
            print("Invalid input, a name must contain:")
            print("At least 2 letters, only letters and no spaces.\n")
            print(f"please enter a valid {name_prompt}.")

    if pat_name == "Exit":
        main_menu()
    else:
        return pat_name


def check_existing_appts(details):
    """
    Checks the appointment records for the name and date provided
    and if a booking already exists for the details, returns true,
    otherwise it returns false.
    """
    detail_date = details[0]
    detail_name = details[2:4]
    date_bookings = get_appts_for_date(detail_date, "bookings")

    # Idea on how to implement check came from stackoverflow.
    existing_appt = None
    for booking in date_bookings:
        for i in range(len(booking) - len(detail_name) + 1):
            if detail_name == booking[i:i+len(detail_name)]:
                existing_appt = True

    return existing_appt


def confirm_appointment(data):
    """
    Presents the user with the appointment details entered
    and asks for final confirmation to make the booking
    or cancel. Input is requested untill a valid option
    is input.
    """
    clear_tmnl()
    appt_headers = ["Date", "Time", "Name", "Surname"]
    print("Please confirm the following details before booking.\n")
    print(tabulate([data], headers=appt_headers, tablefmt="fancy_grid"))
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


def update_appts(data):
    """
    Updates the appointments sheet using the data provided.
    """
    print("Updating appointments...")
    APPTS.append_row(data, value_input_option='USER_ENTERED')
    print("Appointment booked successfully!")
    sort_sheet()


def book_again_prompt(status):
    """
    Provides user with option to either re-enter details or enter
    details for a new booking depending on the confirmation
    status provided from the confirm_appointment function.
    Input is requested untill it is valid.
    """
    if status == "terminated":
        prompt = "Enter new details"
    elif status == "booked":
        prompt = "Book another appointment"
    
    print("Please select an option below.")
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


def search_name(reason):
    """
    Gets return values of get_name function for both name and surname
    and defines them in a single variable (search_name) as a list
    to pass to get_appts_for_name function and finally passes the
    returned records to the display_records function or returns them
    to the cancelation prompt, depending on argument given.
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

    if reason == "cancelation":
        return [search_nme, name_appts, name_recs]
    else:
        display_records(name_recs, name_desc, name_heads)


def get_appts_for_name(name):
    """
    Gets and returns the appointments booked for the name
    povided as an argument.
    """
    all_appts = APPTS.get_all_values()
    name_appts = []
    for appt in all_appts[1:]:
        appt_name = appt[2:4]
        if appt_name == name:
            name_appt_row = [all_appts.index(appt) + 1]
            name_appt = appt + name_appt_row
            name_appts.append(name_appt)

    return name_appts


def search_date(specification):
    """
    Defines search_dte variable using current date or returned
    date depending on the argument provided and passes it to
    get_appts_for_date function to get the relevant records to
    pass to the display_records function.
    """
    clear_tmnl()
    if specification == "today":
        search_dte = CURRENT_DATE_FMTED
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

    display_records(date_recs, date_desc, dte_heads)


def get_appts_for_date(data, required_return):
    """
    Gets the booked appointments for the date providedand returns
    the requested data depending on the argument given for the
    required_return parameter.
    """
    date_appts = APPTS.findall(data)

    bookings = []
    booked_times = []
    for date_appt in date_appts:
        booking = APPTS.row_values(date_appt.row)
        booked_time = booking[1]
        bookings.append(booking)
        booked_times.append(booked_time)

    if required_return == "bookings":
        return bookings
    elif required_return == "booked_times":
        return booked_times


def display_records(records, topic, heads):
    """
    Displays data in a table format using headers and data provided
    as arguments (records and heads) and prints text about the table
    using the argument provided to the topic parameter. If the records
    are empty then it informs the user that no records are available.
    User is then prompted to input options to return to search menu
    or main menu. Input is requested untill it is valid.
    """
    clear_tmnl()
    if records == []:
        print(f"There are no appointments booked for {topic}.")
    else:
        print(f"Below are the appointments booked for {topic}.")
        print(tabulate(records, headers=heads, tablefmt="fancy_grid"))

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


def cancelation_prompt():
    """
    Calls the search_name function to get bookings relative to searched name
    and presents them to the user. If no bookings are present, allows user to
    search again or return to menu. If one booking, passes it to cancel_appt
    function for final confirmation. If multiple bookings, prompts user to
    choose one to cancel then passes it to cancel_appt function.
    """
    clear_tmnl()
    search_info = search_name("cancelation")
    cncl_name = ' '.join(search_info[0])
    appt_opts = search_info[1]
    dates_and_times = search_info[2]

    cncl_opts = []
    for date_and_time in dates_and_times:
        cncl_opt = ' at '.join(date_and_time)
        cncl_opts.append(cncl_opt)        

    if bool(appt_opts) is False:
        print(f"There are no appointments booked for {cncl_name}.\n")
        print("Press 1 to search again or 2 to return to menu.")
        while True:
            search_again_ans = input("\n")
            if search_again_ans not in ("1", "2"):
                print("Invalid, enter an option 1 or 2.")
            else:
                break
        if search_again_ans == "1":
            cancelation_prompt()
        elif search_again_ans == "2":
            main_menu()

    if len(cncl_opts) == 1:
        appt_to_cncl = appt_opts[0]

    else:
        cncl_ans = pyip.inputMenu(cncl_opts,
                                  prompt="Select an appointment to cancel.\n",
                                  numbered=True,
                                  allowRegexes=[("Exit"), ("exit")]
                                  )
        if cncl_ans.capitalize() == "Exit":
            main_menu()
        else:
            for appt_opt in appt_opts:
                if cncl_ans.split(" ")[0] in appt_opt:
                    appt_to_cncl = appt_opt

    cancel_appt(appt_to_cncl)


def cancel_appt(appointment):
    """
    Prompts user to input options to either confirm cancelation or stop it.
    If confirmed, it gets the row number of the appointment to cancel
    and deletes the row from the appointments sheet. If stopped it
    returns user to main menu.
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
            APPTS.delete_rows(row_to_dlte)
            break


def dlte_past_appts():
    """
    Removes appointment records from the sheet for dates that are in the past.
    """
    all_appt_dates = APPTS.col_values(1)
    for appt_date in all_appt_dates[1:]:
        appt_date_fmt = datetime.datetime.strptime(appt_date, "%d/%m/%Y").date()
        if appt_date_fmt < CURRENT_DATE:
            date_cells = APPTS.findall(appt_date)
            for date_cell in date_cells:
                row_num = date_cell.row
                APPTS.delete_rows(row_num)


def sort_sheet():
    """
    Sorts the sheet by dates and times.
    """
    APPTS.sort((2, "asc"))
    APPTS.sort((1, "asc"))


def clear_tmnl():
    """
    Clears the terminal when called.
    """
    os.system("clear")  # Idea taken from a post on slack.


def main():
    """
    Runs necessary functions at start of the program.
    """
    dlte_past_appts()
    sort_sheet()
    main_menu()


main()
