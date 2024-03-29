from exchangelib import Account, Configuration, Credentials, DELEGATE, EWSTimeZone
from getpass import getpass

tz_info = EWSTimeZone.localzone() # EWSTimeZone('Europe/Berlin')
class UserAccount:
    domain = "mail.rwth-aachen.de"
    def __init__(self, email, user, password) -> None:
        self.email = email
        self.user = user
        self.password = password
    
    def verify_account(self) -> bool:
        """
        validate user account credentials and return the OWA user account
        """
        username = self.user + UserAccount.domain.replace("mail.", "@")
        is_valid = True
        try:
            credentials = Credentials(username=username, password=self.password)
            config = Configuration(server=UserAccount.domain, credentials=credentials)
            self.account = Account(primary_smtp_address=self.email, config=config, autodiscover=False, access_type=DELEGATE)
        except:
            is_valid = False
            raise Exception("Invalid Password! Try Again!!")
    
        return is_valid
     
    def get_calendar_named_bookings(self, name):
        """
        retrieve all the bookings by a given name
        """
        account = self.account
        calendar_items = account.calendar.filter(subject=name) #(start__range=(start, end))
        events = {"subject" : [], "date" : [], "start_time" : [], "end_time" : []}
        for item in calendar_items:
            events["subject"].append(item.subject)
            start_time = item.start.astimezone(tz_info).strftime('%H:%M')
            end_time = item.end.astimezone(tz_info).strftime('%H:%M')
            events["date"].append(item.start.strftime('%d/%m/%Y'))
            events["start_time"].append(start_time) #(item.start.strftime('%H:%M'))
            events["end_time"].append(end_time) # (item.end.strftime('%H:%M'))
    
        return events

def bookings() -> dict:
    email = input("Enter your full email address (RWTH): ")     # e.g. "john.doe@rwth-aachen.de"
    password = getpass("Enter your password: ")                 # e.g. "TopSecret123"
    userID = input("Enter your RWTH user id: ")                 # e.g. "ab123456"

    account = UserAccount(email, userID, password)
    is_account_valid = account.verify_account()
    if is_account_valid:
        booking_name = input("Enter given name of your booking: ")
        bookings = account.get_calendar_named_bookings(booking_name)
        print(bookings)
    
    return bookings

if __name__ == '__main__':
    bookings()