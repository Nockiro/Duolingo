from duoapi.ls_user import User
from duoapi.lschallenge import DuolingoLearnSessionChallenge
from duoapi.learnsession import DuolingoLearnSession
from pprint import pprint
from time import sleep
import json
import requests
import time
import datetime

#lingo  = duolingo.Duolingo('Robin143310')

if __name__ == "__main__":
    user = User("DSA975012", "sprachassist")  # E-mail - d21292@urhen.com
    lb = user.get_current_active_leaderboard()
    pprint(user.get_available_languages())
    pprint(user.get_working_language(False))
    pprint(user.get_settings())
    pprint(user.get_profile_info().get_friendlist_leaderbord("week"))
    pprint(user.get_profile_info().get_activity())
    pprint(user.get_profile_info().get_friends())
    #pprint(user.get_voice_stuff().get_audio_url("hello", "en"))
    pprint(lb.isLeagueActive())
    pprint(lb.getRank())
    pprint(lb.getScore())
    pprint(lb.getTierAsWord())
    pprint(user.get_full_user_info()["monthlyXp"])
    ls : DuolingoLearnSession = None

    # print(user.get_active_skills(current_language)[0]['locked'])

    # for topic in user.get_active_skills(user.get_working_language(True)):
    #     if user.get_skills_in_progress(user.get_working_language(True))[0] in topic.values():
    #         # TODO There were infrequent Server Response 500, check if they are gone
    #         ls = user.get_current_learnsession(topic)
    #         print(ls.get_sessionid())
    #         sleep(0.1)  # Add a bit of delay to not flood the duolingo backend

    ls = user.get_global_practice_learnsession(user.get_working_language(True))

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
