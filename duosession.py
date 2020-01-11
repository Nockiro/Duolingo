from requests import Session


class DuoSession():
    def __init__(self, username: str, password: str):
        self.session: Session = Session()
        self.session.verify = False

        self.jwt = None
        self._initialize(username, password)

    def _initialize(self, username: str, password: str):
        """
        Authenticate through ``https://www.duolingo.com/login``.
        """

        """ Deferred import to avoid circular dependency """
        from duorequest import DuoRequest

        login_url = "https://www.duolingo.com/login"
        data = {"login": username, "password": password}
        response = DuoRequest.do_request(login_url, self, data)

        attempt = response.json()

        if attempt.get('response') == 'OK':
            self.jwt = response.headers['jwt']
            self.username = attempt.get("username")
            self.user_id = attempt.get("user_id")
            return self

        raise Exception("Login failed: " + attempt.get("failure"))


if __name__ == '__main__':
    from pprint import pprint
    """ Sample Session Creation """
    pprint(DuoSession("DSA975012", "sprachassist"))
