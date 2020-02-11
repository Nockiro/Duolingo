import json
from .duorequest import DuoRequest
from .lschallenge import DuolingoLearnSessionChallenge
from .duosession import DuoSession
from collections import namedtuple
import pickle
import datetime
import time

__DEBUG__ = False
leaderboard_url = "https://duolingo-leaderboards-prod.duolingo.com/leaderboards/7d9f5dd1-8423-491a-91f2-2532052038ce/users/%s"
class DuolingoLeaderBoard(object):

    def __init__(self, session : DuoSession, jsonResponseData):
        """Initialization with session and response data"""

        if session != None:
            self.session = session
            self.learn_session_data = jsonResponseData


            self.cohortsize = self.learn_session_data["leaderboard"]["ruleset"]["cohort_size"]
            """ is true if the current user has an active ligue """
            self.leagueActive = 'active' in self.learn_session_data

            if self.leagueActive:
                self.activeBoard = self.learn_session_data["active"]
                self.score = self.activeBoard["score"]

                """ contains contest_end, contest_start, contest_state"""
                self.contest = self.activeBoard["contest"]
                self.tier = self.activeBoard["cohort"]["tier"]
                
                print(self.session.user_id)
                for x in range(0, len(self.activeBoard["cohort"]["rankings"]) - 1):
                    if str(self.activeBoard["cohort"]["rankings"][x]["user_id"]) == str(self.session.user_id):  
                        self.rank = x + 1
                        break

    def fetch(session : DuoSession):      
        """ Set Debug to false to get real server data """
        if not __DEBUG__:
            leaderboardRequest = DuoRequest.do_request(leaderboard_url % session.user_id, session)
            jsonResponseData = leaderboardRequest.json()
        else:
            jsonResponseData = __sampleData__

        return DuolingoLeaderBoard(session, jsonResponseData)

    def getRank(self):
        """ Returns rank or 0 if not on the top list """
        try:
            return self.rank
        except AttributeError:
            return 0
    def getTierAsWord(self):
        tiers = {
            0: "Bronze",
            1: "Silber",
            2: "Gold",
            3: "Saphir",
            4: "Rubin",
            5: "Amethyst",
            6: "Perle",
            7: "Obsidian",
            8: "Diamant"
        }
        return tiers.get(self.tier, "Unbekannt")
    def getCurrentContestData(self):
        return self.contest
    def getScore(self):
        return self.score
    def isLeagueActive(self):
        return self.leagueActive

