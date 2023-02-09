import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

num_choices_date = 0
if len(sys.argv) < 2:
  raise Exception("Must provide at least one date parameter.")
elif len(sys.argv) == 2:
    begin_date = sys.argv[1]
    num_choices_date = 1
elif len(sys.argv) == 3:
    begin_date = sys.argv[1]
    num_choices_date = int(sys.argv[2])
else:
    raise Exception("Unknown error encountered.")

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://terminplaner6.dfn.de/")
driver.maximize_window()

login = driver.find_element(by=By.ID, value="block-block-9")
login.click()

# find links in the page
links = login.find_elements(by=By.TAG_NAME, value="a")
for link in links:
    # print(link.text)
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
    # print(link.get_attribute("innerHTML"))
    if "Buchungsliste" in link.get_attribute("innerHTML") or "meeting" in link.get_attribute("innerHTML"):
        link.click()
        # print(link.get_attribute("innerHTML"))
        break

time.sleep(1)   # allow the new page to load after clicking
new_page = driver.window_handles[0]
driver.switch_to.window(new_page)
meeting_title = "SampleMeeting1"
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

choice = 0
day = begin_date[ : begin_date.find('/')]
month = begin_date[begin_date.find('/') + 1 : begin_date.rfind('/')]
year = begin_date[begin_date.rfind('/') + 1 : ]
choice0_day = day
choice0_month = month
choice0_year = year

make_meeting_table_rows = driver.find_elements(By.XPATH,'//table[@id="poll-choice-table"]/tbody/tr')
for table_row in make_meeting_table_rows:
    choice_date = table_row.find_element(By.XPATH,".//td[@class='makemeeting-choice-date']")
    select_day = Select(choice_date.find_element(By.XPATH, ".//select[contains(@id, 'chdate-day')]"))
    select_month = Select(choice_date.find_element(By.XPATH, ".//select[contains(@id, 'chdate-month')]"))
    select_year = Select(choice_date.find_element(By.XPATH, ".//select[contains(@id, 'chdate-year')]"))
    select_day.select_by_value(choice0_day)
    select_month.select_by_value(choice0_month)
    select_year.select_by_value(choice0_year)

if num_choices_date > 1:
    for i in range(num_choices_date - 1):
        btn_more_choices = driver.find_element(By.XPATH,'//span[@class="mme-add-day"]/input')
        btn_more_choices.click()
        time.sleep(2)

participant_email_checkbox = driver.find_element(by=By.XPATH, value="//input[@type='checkbox' and @id='edit-field-require-email-und']")
participant_email_checkbox.click()
time.sleep(2)

edit_save_button = driver.find_element(by=By.XPATH, value="//input[@type='submit' and @id='edit-submit']")
edit_save_button.click()
time.sleep(2)
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

'''
sugg = 0
date1_slot1 = driver.find_element(by=By.ID, value = f"edit-field-mme-makemeeting-und-0-choices-new{choice}-chsuggestions-sugg{sugg}")
date1_slot1.send_keys(Keys.RETURN)
date1_slot1.send_keys("09001530")
time.sleep(2)
date1_slot1.send_keys(Keys.TAB)
'''
