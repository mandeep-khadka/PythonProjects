from exchangelib import Account, Configuration, Credentials, DELEGATE
from getpass import getpass

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
            events["date"].append(item.start.strftime('%d/%m/%Y'))
            events["start_time"].append(item.start.strftime('%H:%M'))
            events["end_time"].append(item.end.strftime('%H:%M'))
    
        return events

def main():
    email = input("Enter your full email address: ")        # e.g. "mandeep.khadka@rwth-aachen.de"
    userID = input("Enter your User ID: ")                  # e.g. "bk******"
    password = getpass("Enter your password: ")             # e.g. "top_secret_123"

    account = UserAccount(email, userID, password)
    is_account_valid = account.verify_account()
    if is_account_valid:
        bookings = account.get_calendar_named_bookings("SampleBlockedSlot")
        print(bookings)

if __name__ == '__main__':
    main()