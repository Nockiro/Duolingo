import duolingo
from lschallenge import DuolingoLearnSessionChallenge
from pprint import pprint
import json
import requests
import time
import datetime

#lingo  = duolingo.Duolingo('Robin143310')

if __name__ == "__main__":
    lingo = duolingo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com

    ls = None

    current_language = lingo.get_current_language_abbr()

    # print(lingo.get_active_skills(current_language)[0]['locked'])

    for topic in lingo.get_active_skills(current_language):
        if lingo.get_skills_in_progress(current_language)[0] in topic.values():
            # TODO Infrequent Server Response 500 - what to do when this appears
            # Possibly send new request after a time interval
            ls = lingo.get_current_learnsession(topic)
            print(ls.getSessionID())


    challengeList = ls.getChallengeList()
    while challengeList:
        notFinished = challengeList
        for challenge in notFinished:
            exercise = DuolingoLearnSessionChallenge(challenge)
            target_lang = challenge['metadata']['target_language_name']
            print(exercise.getSourcePrompt(target_lang))
            print(exercise.getCorrectSolutions())
            user_input = input()
            if exercise.getAnswerCheck(user_input):
                print("Correct")
                challengeList.remove(challenge)
            else:
                print("Incorrect")
            print()


    if not challengeList:
        data = ls.getLearnSessionData()
        data['failed'] = False

        sessions_end = lingo.end_session(data)
        print(sessions_end)

