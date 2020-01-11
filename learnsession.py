import json
from duorequest import DuoRequest
from lschallenge import DuolingoLearnSessionChallenge
from collections import namedtuple
import datetime
import time

__DEBUG__ = False
learn_session_data_url = "https://www.duolingo.com/2017-06-30/sessions"
class DuolingoLearnSession(object):

    def __init__(self, session, jsonResponseData):

        self.session = session

        self.learn_session_data = jsonResponseData
        self.learn_session_metadata = self.learn_session_data["metadata"]
        self.learn_session_challenge_list = self.learn_session_data["challenges"]

        self.learn_session_id = self.learn_session_metadata['id']
        self.current_language = self.learn_session_metadata["language_string"]

    def fetch(session, data):      
        """ Set Debug to false to get real server data """
        if not __DEBUG__:
            learnRequest = DuoRequest.do_request(learn_session_data_url, session, data)
            print(learnRequest)
            jsonResponseData = learnRequest.json()
        else:
            jsonResponseData = __sampleData__

        return DuolingoLearnSession(session, jsonResponseData)

    def get_challenge(self, index):
        challenge = DuolingoLearnSessionChallenge(
            self.learn_session_challenge_list[index])
        return challenge

    def get_challenge_list(self):
        return self.learn_session_challenge_list

    def get_sessionid(self):
        return self.learn_session_id

    def get_learnsession_data(self):
        return self.learn_session_data

    def end_session(self, data):
        request = DuoRequest.do_request(learn_session_data_url + "/" + self.get_sessionid(), self.session, data, "PUT")
        return request
