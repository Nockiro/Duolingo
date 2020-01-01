import json
from lschallenge import DuolingoLearnSessionChallenge
from collections import namedtuple
import datetime
import time


class DuolingoLearnSession(object):
    def __init__(self, jsonResponseData):
        self.learnSessionData = jsonResponseData
        self.learnSessionMetaData = self.learnSessionData["metadata"]
        self.learnSessionChallengeList = self.learnSessionData["challenges"]

        self.learnSessionID = self.learnSessionMetaData['id']
        self.currentLanguage = self.learnSessionMetaData["language_string"]

        self.learn_session_data_url = "https://www.duolingo.com/2017-06-30/sessions"

    def getChallenge(self, index):
        challenge = DuolingoLearnSessionChallenge(
            self.learnSessionChallengeList[0])
        return challenge

    def getChallengeList(self):
        return self.learnSessionChallengeList

    def getSessionID(self):
        return self.learnSessionID

    def getLearnSessionData(self):
        return self.learnSessionData

    def end_session(self, data):
        request = self._make_req(
            "PUT", self.learn_session_data_url + "/" + self.session_id, data=data)
        return request
