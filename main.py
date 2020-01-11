from ls_user import User
from lschallenge import DuolingoLearnSessionChallenge
from pprint import pprint
from time import sleep
import json
import requests
import time
import datetime

#lingo  = duolingo.Duolingo('Robin143310')

if __name__ == "__main__":
    user = User("DSA975012", "sprachassist"); # E-mail - d21292@urhen.com
    ls = None

    # print(user.get_active_skills(current_language)[0]['locked'])

    for topic in user.get_active_skills(user.get_working_language(True)):
        if user.get_skills_in_progress(user.get_working_language(True))[0] in topic.values():
            # TODO There were infrequent Server Response 500, check if they are gone
            ls = user.get_current_learnsession(topic)
            print(ls.get_sessionid())
            sleep(0.1); # Add a bit of delay to not flood the duolingo backend


    challengeList = ls.get_challenge_list()
    while challengeList:
        notFinished = challengeList
        for challenge in notFinished:
            exercise = DuolingoLearnSessionChallenge(challenge)
            print(exercise.get_source_prompt())
            print(exercise.get_correct_solutions())
            user_input = input()
            if exercise.check_answer(user_input):
                print("Correct")
                challengeList.remove(challenge)
            else:
                print("Incorrect")
            print()


    if not challengeList:
        data = ls.get_learnsession_data()
        data['failed'] = False

        sessions_end = ls.end_session(data)
        print(sessions_end)

