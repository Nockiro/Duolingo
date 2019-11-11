import duolingo as duo

#lingo = duo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com


class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.lingo = duo.Duolingo(username, password=self.password)

    def getLanguage(self):
        return self.lingo._is_current_language
