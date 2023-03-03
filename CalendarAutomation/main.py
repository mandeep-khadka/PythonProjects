import sys
import time
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

### user-defined modules ###
import read_calendar as owa

email = input("Enter your full email address: ")            # e.g. "mandeep.khadka@rwth-aachen.de"
userID = input("Enter your User ID: ")                      # e.g. "bk******"
password = getpass("Enter your password: ")

account = owa.UserAccount(email, userID, password)
time.sleep(2)
is_account_valid = account.verify_account()
if is_account_valid:
    print("Congratulations! The connection to mail server is successful!!")
    time.sleep(1)
    booking_name = input("Enter given name of your booking: ")  # e.g. "SampleMeeting"
    bookings = account.get_calendar_named_bookings(booking_name)
    print(bookings)
num_choices_date = len(bookings['date'])

### By default the webpage closes after the execution finishes ###
### The experimental option "detach" passed to the chrome browser keeps the browser open ###
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://terminplaner6.dfn.de/")
driver.maximize_window()    # maximize the webpage to the screen window

### Login to terminplanner ###
login_btn = driver.find_element(by=By.ID, value="block-block-9")
login_btn.click()
links = login_btn.find_elements(by=By.TAG_NAME, value="a")
for link in links:
    if "LOGIN" in link.text.upper():
        link.click()
        break

input_username = driver.find_element(by=By.ID, value="edit-name")
input_username.send_keys("mandeepkhadka")

input_password = driver.find_element(by=By.ID, value="edit-pass")
input_password.send_keys("Tplanner1013!")

login_button = driver.find_element(by=By.ID, value="edit-submit")
login_button.click()

links = driver.find_elements(by="xpath", value="//a[@href]")
for link in links:
    if "Buchungsliste" in link.get_attribute("innerHTML") or "meeting" in link.get_attribute("innerHTML"):
        link.click()
        break

time.sleep(1)   # allow the new page to load after clicking
current_window = driver.window_handles[0]  #store the current window
driver.switch_to.window(current_window)    #switch to the current window

meeting_title = bookings['subject'][0]
meeting_location = "CT's office"
meeting_description_opt = "Lorem Ipsum"

title_element = driver.find_element(by=By.ID, value="edit-title")
location_element = driver.find_element(by=By.ID, value="edit-field-mme-location-und-0-value")
notify_checkbox = driver.find_element(by=By.XPATH, value="//input[@type='checkbox' and @id='edit-field-notify-on-answers-und']")
meeting_desc_element = driver.find_element(by=By.ID, value="edit-body-und-0-value")

title_element.send_keys(meeting_title)
location_element.send_keys(meeting_location)
meeting_desc_element.send_keys(meeting_description_opt)
notify_checkbox.click()

value_default_days = "Remove this day"
default_suggested_days = driver.find_elements(By.XPATH, value="//input[@value='" + value_default_days + "']")
no_of_default_days = len(default_suggested_days)
if no_of_default_days == 0:
    print("Input element with value '" + value_default_days + "' not found.")
else:
    for i in range(no_of_default_days - 1):
        default_day = driver.find_element(By.XPATH, value="//input[@value='" + value_default_days + "']")
        default_day.click()
        time.sleep(2)

print("length of dic: ", len(bookings['date']))
if num_choices_date > 1:
    for i in range(num_choices_date - 1):
        btn_more_choices = driver.find_element(By.XPATH,'//span[@class="mme-add-day"]/input')
        btn_more_choices.click()
        time.sleep(2)

idx = num_choices_date - 1
make_meeting_table_rows = driver.find_elements(By.XPATH,'//table[@id="poll-choice-table"]/tbody/tr')
for table_row in make_meeting_table_rows:
    
    datestr = bookings['date'][idx]
    day = datestr[ : datestr.find('/')]
    if day.find('0') == 0:
        day = day[1:]
    month = datestr[datestr.find('/') + 2 : datestr.rfind('/')]
    year = datestr[datestr.rfind('/') + 1 : ]

    date_el = table_row.find_element(By.XPATH,".//td[@class='makemeeting-choice-date']")
    day_el = Select(date_el.find_element(By.XPATH, ".//select[contains(@id, 'chdate-day')]"))
    month_el = Select(date_el.find_element(By.XPATH, ".//select[contains(@id, 'chdate-month')]"))
    year_el = Select(date_el.find_element(By.XPATH, ".//select[contains(@id, 'chdate-year')]"))
    day_el.select_by_value(day)
    month_el.select_by_value(month)
    year_el.select_by_value(year)

    sugg = table_row.find_element(By.XPATH, ".//input[contains(@id, 'chsuggestions-sugg')]")
    sugg.send_keys(Keys.RETURN)
    timestr = bookings['start_time'][idx] + bookings['end_time'][idx]
    sugg.send_keys(timestr)
    sugg.send_keys(Keys.TAB)

    idx -= 1

participant_email_checkbox = driver.find_element(by=By.XPATH, value="//input[@type='checkbox' and @id='edit-field-require-email-und']")
participant_email_checkbox.click()
time.sleep(2)

edit_save_button = driver.find_element(by=By.XPATH, value="//input[@type='submit' and @id='edit-submit']")
edit_save_button.click()
time.sleep(2)
"""
new_page = driver.window_handles[0]
driver.switch_to.window(new_page)

link_invite_participants = driver.find_element(by=By.XPATH, value="//a[text()='Invite participants']")
link_invite_participants.click()

add_participants = driver.find_element(by=By.XPATH, value="//textarea[@id='edit-recipients']")
add_participants.send_keys("m.khadka69@gmail.com")
add_participants.send_keys(Keys.RETURN)
add_participants.send_keys("m.khadka515@gmail.com")
add_participants.send_keys(Keys.TAB)

add_personal_msg = driver.find_element(by=By.XPATH, value="//textarea[@id='edit-message--2']")
add_personal_msg.send_keys("Please select the date that suits you!")
add_personal_msg.send_keys(Keys.TAB)

send_msg_button = driver.find_element(by=By.XPATH, value="//input[@type='submit' and @id='edit-submit--2']")
send_msg_button.click()
time.sleep(2)
submit_button = driver.find_element(by=By.XPATH, value="//input[@type='submit' and @id='edit-submit']")
submit_button.click()
"""