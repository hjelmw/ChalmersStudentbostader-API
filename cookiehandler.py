import time

## This class handles cookies and automatically deletes old cookies if timer has expired.
## It's purpose is to circumvent poor cookie handling on CHS mina sidor. 
## 
## arguments:
##    cookies - dict of cookies to store
##    timer - duration in minutes of how long to store a cookie
## check_expired returns:
##    dict of cookies or empty dict if timer expired
class CookieHandler:
    cookies = dict()
    timer = 0
    start_time = 0


    # private, checks if cookie expired and if so, deletes it
    def __check_expired(self):
        curr_time = time.time()

        if(curr_time - self.start_time >= self.timer*60):
            # cookie expired
            self.cookies = {}
            self.timer = 0
            self.start_time = 0
            return {}
        else:
            return self.cookies


    def __init__(self, timer):
        self.timer = timer
        self.start_time = time.time()

    # adds cookie dict to cookies dict
    def add_cookie(self, cookie):
        self.cookies.update(cookie)


    def get_cookies(self):
        return self.__check_expired()
