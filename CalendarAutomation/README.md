# Calendar Automation

Automate the process of extracting calendar bookings and organizing them into meeting invites.

## Description

All the meeting slots booked under a given name in the personal calendar are extracted. These bookings are automatically organized with proper date and timings into a meeting planner application such as ["Terminplanner"](https://terminplaner6.dfn.de/).

## Getting Started

### Dependencies

* OS: Windows, Linux, Mac
* Browser: Chrome, Firefox
* Python Libraries: exchangelib, selenium, webdriver_manager (only for Chrome)

### Installing

* Clone the repo on your local machine.
* Install the necessary Python Libraries mentioned above.

e.g.
```
pip install exchangelib

pip install selenium

pip install webdriver-manager
```

### Executing program

#### How to run the program
* cd into project home directory.
* Create a virtual environment for the project (Recommended).

e.g. (On Windows)
```
python -m venv venv
```
* Activate the virtual environment.

e.g. (On Windows)
```
venv\Scripts\activate
```
* Run the main program.
```
python main.py
```
* The program (during the execution) requests for several inputs, enter them correctly.

e.g. terminplanner username and password

## Help

Raise issues for any advice or common problems and issues.

## Author

Mandeep Khadka  
(mandeep.khadka@rwth-aachen.de)