import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(browser = "firefox"):

    if browser == "chrome":
        """
        by default the webpage closes after the execution finishes
        "detach" option keeps the browser open
        """
        chrome_options = ChromeOptions.Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver = webdriver.Firefox()

    return driver


def login(driver, tp_username, tp_password):
    """
    login to terminplanner website
    """
    login_dd = driver.find_element(by=By.ID, value="block-block-9")
    login_dd.click()
    links = login_dd.find_elements(by=By.TAG_NAME, value="a")
    for link in links:
        if "LOGIN" in link.text.upper():
            link.click()
            break

    username = driver.find_element(by=By.ID, value="edit-name")
    username.send_keys(tp_username)

    password = driver.find_element(by=By.ID, value="edit-pass")
    password.send_keys(tp_password)

    login_btn = driver.find_element(by=By.ID, value="edit-submit")
    login_btn.click()
    # Wait for the login process to complete and check for an error message
    try:
        error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='messages error']")))
        if error_message:
            raise Exception("Username/Password Error - " + error_message.text)
    except TimeoutException:
        print("Login successful")

    current_window = driver.window_handles[0]
    driver.switch_to.window(current_window)

    return driver

def populate(driver, bookings):
    """
    fill up the terminplanner with scheduled booking slots
    """
    div_element = driver.find_element(by=By.ID, value="block-menu-menu-header-menu")
    anchor_element = div_element.find_element(by=By.CSS_SELECTOR, value="a")
    anchor_element.click()

    meeting_title = bookings['subject'][0]
    meeting_location = "CT's office"
    meeting_description_opt = "You can edit the description later"

    title = driver.find_element(by=By.ID, value="edit-title")
    title.send_keys(meeting_title)
    location = driver.find_element(by=By.ID, value="edit-field-mme-location-und-0-value")
    location.send_keys(meeting_location)
    meeting_desc = driver.find_element(by=By.ID, value="edit-body-und-0-value")
    meeting_desc.send_keys(meeting_description_opt)
    notify_checkbox = driver.find_element(by=By.XPATH, value="//input[@type='checkbox' and @id='edit-field-notify-on-answers-und']")
    notify_checkbox.click()

    value_default_days = "Remove this day"
    def_sugg_days = driver.find_elements(By.XPATH, value="//input[@value='" + value_default_days + "']")
    if len(def_sugg_days) == 0:
        print("Input element with value '" + value_default_days + "' not found.")
    else:
        for i in range(len(def_sugg_days) - 1):
            default_day = driver.find_element(By.XPATH, value="//input[@value='" + value_default_days + "']")
            default_day.click()
            time.sleep(2)

    no_choices_date = len(bookings['date'])
    if no_choices_date > 1:
        for i in range(no_choices_date - 1):
            btn_more_choices = driver.find_element(By.XPATH,'//span[@class="mme-add-day"]/input')
            btn_more_choices.click()
            time.sleep(2)

    idx = no_choices_date - 1
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

    edit_save_button = driver.find_element(by=By.XPATH, value="//input[@type='submit' and @id='edit-submit']")
    edit_save_button.click()

"""
current_window = driver.window_handles[0]  #store the current window
driver.switch_to.window(current_window)    #switch to the current window

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