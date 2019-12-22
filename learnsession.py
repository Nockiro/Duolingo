import json
from lschallenge import DuolingoLearnSessionChallenge
from collections import namedtuple

class DuolingoLearnSession(object):
    def __init__(self, jsonResponseData):
        self.learnSessionData = jsonResponseData
        self.learnSessionMetaData = self.learnSessionData["metadata"]
        self.learnSessionChallengeList = self.learnSessionData["challenges"]
        self.learnSessionID = self.learnSessionData["id"]

        self.currentLanguage = self.learnSessionMetaData["language_string"]

    def getChallenge(self, index):
        challenge = DuolingoLearnSessionChallenge(self.learnSessionChallengeList[0])
        return challenge

    def getChallengeList(self):
        return self.learnSessionChallengeList

    def getSessionID(self):
        return self.learnSessionID