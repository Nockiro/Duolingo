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
        response = DuoRequest.doRequest(login_url, self, data)
        attempt = response.json()

        if attempt.get('response') == 'OK':
            self.jwt = response.headers['jwt']
            return self

        raise Exception("Login failed")


if __name__ == '__main__':
    from pprint import pprint
    """ Sample Session Creation """
    pprint(DuoSession("DSA975012", "sprachassist"))
