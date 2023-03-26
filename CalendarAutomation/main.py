from getpass import getpass
import read_calendar as rc
import auto_terminplanner as tp


def main():

    tp_username = input("Enter Terminplanner username: ")
    tp_password = getpass("Enter Terminplanner password: ")

    driver = tp.get_driver()
    driver.get("https://terminplaner6.dfn.de/")
    driver.maximize_window()


    login_page = tp.login(driver, tp_username, tp_password)
    tp.populate(login_page, rc.bookings())


if __name__ == '__main__':
    main()