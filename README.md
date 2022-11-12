# Doctor's Diary

Doctor's Diary is a CLI data automation program designed to run on a mock terminal in Heroku. The program is aimed at helping a small medical practice manage and keep track of patient appointments.

## Purpose

The purpose of this program is to make appointment booking and record tracking easier and faster for the user. It provides the ability to input data that has been validated and retrieve specific data upon request. It is intended to enable the user to easily create, delete and view specific records. 

This program is developed to demonstrate competency in python programming and is purely for educational purposes.

## User Experience

### Project Goals

As the site owner, I want the program to:
* provide information on how to use it.
* be easy to navigate.
* provide feedback or a response to the user when they perform a task or action.
* provide the user with the ability to perform tasks relative to the program's purpose.

### User Stories

NB - This app is intended to be used by an employee at a small medical practice. The idea is that the user will manage appointments based on requests from patients. An example is the case in which a patient phones the practice to either book or cancel an appointment and the user requests information from the patient to use in order to do so.

As a user, I want to be able to:
* view informational content on how to properly use the program.
* book a new appointment with valid details.
   * enter a detail and have it validated before moving onto the next one.
   * confirm all the details before making the booking.
* view all appointments booked for the current date.
* search for appointments under a specific name and view them.
* search for appointments pertaining to a specific date and view them.
* cancel a specific appointment.

### Program flowchart

During the planning stages, I created a basic flowchart of how I wanted the program to work and interact.
The flowchart was created using [Lucidchart](https://www.lucidchart.com/pages/).

During development, I discovered a few things that needed to be added. These were mostly minor changes, however, the main adjustments that were made that were different from the flow chart were as follows:

* I felt it would provide a better experience if a separate menu for search options was present.
   * This made the content less overwhelming and cluttered and created a more organised site.
   * After a search, the user can opt for the search menu again or for the main menu.
* Instead of asking the user to manually input a date to choose a cancelation option, I found it was better to provide a list of options to choose from.
   * This meant less input was required from the user making the process much faster.
   * If only one option is available, the selection process is skipped all together.

Although slight changes were made, the program generally follows the flow of the chart below and the purpose of the chart was to help me invision what I wanted to achieve and how I wanted to achieve it. It played a key role in planning and development overall.

![flowchart-screenshot](assets/readme-images/doctor-diary-flowchart.png)

## Features

### Existing Features

Doctor's Diary is designed with features that encorperate the purpose of the site. The design and display of the site is limitted by factors such as the terminal size and the fact that it is done primarily using python as a CLI app. If the site were to encorporate an interface other than the command line interface for user interaction, a few improvements could be made for a better user experience.

However, the following features outline how the site is best designed to fit needs in its current state.

NB - The app is intended for a single user or a small number of users performing the same job at a medical practice.

* #### The Main Menu
   * When the page is first loaded, the user is presented with a main menu containing options to select from depending on what they want to achieve.

   ![screenshot of the main menu](assets/readme-images/main-menu.png)

* #### The Search Menu
   * The search menu is displayed when the user chooses the option to search for appointments.
   * This presents the user with options to search for specific appointments.
      * The user can search for a specific name or a specific date.
      * The user may also select an option to return to the main menu.
   
   ![screenshot of the search menu](assets/readme-images/search-menu.png)

* #### The Search Results Display
   * Once the user has input a name or date for searching and if appointments are found for the search, the relevant appointments are displayed in a table to be viewed.
      * If the user is searching for a name, only the date and time records will be shown in the table.
      * If the user is searching for a date, only the time and name records will be shown in the table.
   * Images for both displays are shown below.

   ![screenshot of search results for date](assets/readme-images/date-search-appts-display.png)
   ![screenshot of search results for name](assets/readme-images/name-search-appts-display.png)

   * If no appointments are found for the date or name searched for by the user, they are informed that no appointments exist for the searched detail and are provided with options to return to the search menu to search again or return to the main menu.

   ![screenshot of empty date search result](assets/readme-images/empty-date-search-display.png)
   ![screenshot of empty name search result](assets/readme-images/empty-name-search-display.png)

* #### The Display for today's appointments
   * If the user selects the option in the main menu to view today's appointments, the same process is carried out as in the case of searching by date and the program uses the current date instead of an input date from the user.
   * The relevant responses are given for the result of the search as seen below.
      * If appointments are found for the current date, the records are displayed in a table.

      ![screenshot of display for todays appointments](assets/readme-images/today-appts-display.png)
      
      * If no appointments exist for the current date, the user is informed and given the option to return to the main menu or go to the search menu in case they would like to search for an appointment they expected to be on the current date.

      ![screenshot of empty result for todays appointments](assets/readme-images/empty-appts-today.png)

* #### The Date Input Prompt
   * This prompt is presented to the user whenever they select an option that requires them to input the date.
      * Date input is required for booking a new appointment and searching for appointments by date.
   * The prompt requests input from the user and informs them of the format they should use.

   ![screenshot of date input prompt](assets/readme-images/date-input-prompt.png)

* #### The Time Input Prompt
   * This prompt is presented to the user when they are booking a new appointment and need to select a time for the booking.
      * The user is presented with the times that are available for the date they input.
      * The times are presented in the form of a list from which the user can choose an option.
         * This way of presenting the times creates a better user experience as it removes the need to manually input a time and it keeps the same layout as choices shown in the main menu.

   ![screenshot of the time prompt](assets/readme-images/time-input-prompt.png)

* #### The Name Input Prompt
   * This prompt is presented to the user whenever they select an option that requires them to input a name and surname.
      * Name inputs are required for booking new appointments, searching appointments by name, and canceling an appointment.
   * The contents of the prompt changes depending on which part of the name is being input (first name or surname) as seen in the images below.

   ![screenshot of first name prompt](assets/readme-images/f-name-prompt.png)

   ![screenshot of surname prompt](assets/readme-images/surname-prompt.png)

* #### The Booking Confirmation
   * Once the user has entered the necessary details, the appointment details to be booked are displayed in a table and the user is asked to confirm the booking or cancel it.

   ![screenshot of booking confirmation](assets/readme-images/confirm-booking.png)

   * If the user confirms the booking, they are informed that the appointment has been booked successfully and are presented with options to book another appointment or return to the maion menu.

   ![screenshot of the prompt to book again](assets/readme-images/book-another-appt-prompt.png)

   * If the user cancels the booking in the confirmation prompt, they are presented with options to enter new details or return to the main menu.

   ![screenshot prompt to enter new details](assets/readme-images/enter-new-details-prompt.png)

* #### The Already Booked Display
   * If the user enters details to book an appointment but an appointment has already been booked for the name and date input, they are informed that they cannot book more than one appointment on the same day for one patient and are given options to enter new details or return to the main menu.
   * This prevents a single patient from having multiple unnecessary appointments on the same day, making them unavailable for other patients.

   ![screenshot of the message displayed when an appointment date and name is already booked](assets/readme-images/already-booked-message.png)

* #### The Cancelation Prompt
   * When the user selects the option in the main menu to cancel an appointment, they are prompted to enter a name to search for and are then presented with a prompt to confirm the cancelation.
      * If no appointments are found for the searched name, the user is informed and they can choose to search again or return to the menu.

      ![screenshot of no results for cancelation](assets/readme-images/no-cancel-results.png)

      * If one appointment is found for the searched name, The user is presented with the appointment in question and is asked to provide confirmation to cancel it. If the user decides not to cancel the appointment, the cancelation does not occur and they return to the main menu.

      ![screenshot of cancelation confirmation](assets/readme-images/cancel-confirmation.png)

      * If multiple appointments are found for the searched name, The user is presented with a list of the appointments and is asked to select one to cancel as seen in the image below.
      * Once the user inputs a choice, they are asked to confirm the cancelation as in the image above.

      ![screenshot of cancelation appointment options](assets/readme-images/cancel-appt-options.png)

* #### The confirmed Cancelation Display
   * If the user confirms a cancelation, they are informed that the cancelation was successful and are prompted to press "enter" to return to the main menu.

   ![screenshot of confirmed cancelation](assets/readme-images/confirmed-cancelation.png)

* #### The application Instructions Display
   * Instructions on how to use the application are provided for the user.
   * They can view these instuctions by selecting the option in the main menu to view application instructions.
   * This feature helps the user understand how to navigate the app and how to achieve their desired goals within the app.

   ![screenshot of application instructions](assets/readme-images/app-instructions.png)

* #### The Emergency Exit Option
   * This is an option provided for the user to be able to exit a booking process or cancelation process while entering details.
   * To stop the processes, the user can input "Exit" when asked for any detail.
   * If they do this, they automatically return to the main menu and the process is ended.
   * This creates a better user experience by providing a way to exit a booking or cancelation process at any stage instead of having to wait untill the end to cancel it.
   * The availability of this option is made clear in the application instructions display as seen above.
      * I did not include a print statement in every input prompt outlining the option to exit as it would create lengthy and repetitive messages for the user. I felt it was sufficient just to mention it in the application instructions especially as the site is only intended for a single user or a smaller number of users as mentioned at the beginning of the [features](#features) section. I felt this created a better user experience overall.


* #### Feedback For Invalid Inputs

   Every input the user enters is validated to ensure it meets the required standards for the app. If invalid input is entered, the user is notified that it is invalid, informed on the necessary requirements for the input and requested to input new valid data.

   * Feedback For Invalid Name Inputs
      * A valid name input must:
         * Contain only letters.
         * Contain at least two letters.
         * Contain no white space.
      * If invalid input is entered for either the first name or surname, the following message is displayed.

      ![screenshot of feedback for invalid first name](assets/readme-images/invalid-f-name-feedback.png)
      
      ![screenshot of feedback for invalid surname](assets/readme-images/invalid-l-name-feedback.png)

   * Feedback For Invalid Date Inputs
      * A valid date input must:
         * Be in the format of dd/mm/yyyy.
         * Contain realistic values for day, month, and year categories.
      * If invalid input is entered for a date, the following message is displayed.

      ![screenshot of feedback for invalid date](assets/readme-images/invalid-date-feedback.png)

      * If the date input is for the purpose of booking a new appointment, it must also be for a present or future date.
      * If the date is in the correct format but is a date of the past, the following message is displayed.

      ![screenshot of feedback for a past date input](assets/readme-images/past-date-feedback.png)
   
   * Feedback For Invalid Time input
      * The times are presented as a list of options to choose from.
      * If the user enters an option that is not in the list, the following message is displayed.
         * Note that the same validation process is carried out when a user needs to select an appointment to cancel from a list of options.

      ![screenshot of feedback for invalid time input](assets/readme-images/invalid-time-feedback.png)

* Feedback For Invalid Option Input
   * Throughout the site, the user is presented with options to choose from.
   * If the user inputs data that is not part of the available options, they are informed and asked to input an option within the given range.
   * An example of this is shown below for the main menu options.

   ![screenshot of feedback for invalid option input](assets/readme-images/invalid-option-feedback.png)

## Technologies used

* [Lucidchart](https://www.lucidchart.com/pages/).
   * Used to create a flowchart during the planning stage.
* [HTML5](https://html.spec.whatwg.org/)
   * Used to add structure and content for the site.
   * (provided in the [code institute template](https://github.com/Code-Institute-Org/python-essentials-template)).
* [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
   * Used to provide styling for the site.
   * (provided in the [code intitute template](https://github.com/Code-Institute-Org/python-essentials-template)).
* [Python](https://www.python.org/)
   * Used to provide functionality to the site.
* [Google Sheets](https://www.google.co.uk/sheets/about/)
   * Used to host application data.
* [Gitpod](https://www.gitpod.io/#get-started)
   * Used to create the code and content for the repository.
* [Github](https://github.com/)
   * Used to host the repository.

## Python Packages Used

* [GSpread](https://pypi.org/project/gspread/)
   * Used to manipulate data in google sheets.
* [Datetime](https://docs.python.org/3/library/datetime.html)
   * Used to manipulate dates and times.
* [OS](https://docs.python.org/3/library/os.html)
   * Used to clear the terminal.
* [Tabulate](https://pypi.org/project/tabulate/)
   * Used to present data in a table format.
* [PyInputPlus](https://pypi.org/project/PyInputPlus/)
   * Used to display input options as a menu and validate the selected choice.

## Testing

## Deployment and Development

* The project was developed using [Gitpod](https://www.gitpod.io/#get-started) to create the code and files required.
* The project files, code and information is hosted by [Github](https://github.com/).

### Deploying the App

The deployment of the project was done using [Heroku](https://www.heroku.com/) through the following steps.

1. Log in to Heroku or create an account if necessary.
2. Click on the button labeled "New" from the dashboard in the top right corner and select the "Create new app" option in the drop down menu.
3. Enter a unique name for the application and select the region you are in.
   * For this project, the unique name is "doctor-diary" and the region selected is Europe.
4. Click on "create app".
5. Navigate to the settings tab and locate the "Config Vars" section and click "Reveal config vars".
6. Add a config var (if project uses creds.json file.)
   * In the "KEY" field:
      * enter "CREDS" in capital letters.
   * In the "VALUE" field:
      * copy and paste the contents of your creds.json file and click "Add".
7. Add another config var.
   * In the "KEY" field:
      * enter PORT in all capital letters.
   * In the "VALUE" field:
      * enter 8000 and click "Add".
8. Scroll to the "Buildpacks" section and click "Add buildpack".
9. Select Python and save changes.
10. Add another buildpack and select Nodejs then save changes again.
11. Ensure that the python buildpack is above the Nodejs buildpack.
12. Navigate to the "Deploy" section by clicking the "Deploy" tab in the top navbar.
13. Select "GitHub" as the deployment method and click "Connect to github".
14. Search for the GitHub repository name in the search bar.
15. Click on "connect" to link the repository to heroku.
16. Scroll down and click on "Deploy Branch".
17. Once the app is deployed, heroku will notify you and provide a button to view the app.

NB - If you wish to rebuild the deployed app automatically everytime you push to github, you may click on "Enable Automatic Deploys".

### Forking the Repository

This can be done to create a copy of the repository. The copy can be viewed and editted without affecting the original repository.

To fork the repository through GitHub, take the following steps:
1. In the "the-everything-quiz" repository, click on the "fork" tab in the top right corner.
2. Click on "create fork" to fork the repository.

### Cloning the Repository

To clone the repository through GitHub:

1. In the repository, select the "code" tab located just above the list of files and next to the gitpod button.
2. Ensure HTTPS is selected in the dropdown menu.
3. Copy the URL under HTTPS.
4. Open Git Bash in your IDE of choice.
5. Change the current working directory to the location where you want the cloned directory to be created.
6. Type "git clone" and paste the URL that was copied from the repository.
7. Press the "enter" key to create the clone.
   
## Credits

## Acknowledgements