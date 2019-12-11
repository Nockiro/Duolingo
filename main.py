import duolingo
from lschallenge import DuolingoLearnSessionChallenge
from pprint import pprint
import json

#lingo  = duolingo.Duolingo('Robin143310')

if __name__ == "__main__":    
    lingo = duolingo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com
    lingo = duolingo.Duolingo('Dreamingdust', password='9ymnaczuf46jat3') # E-mail - d21292@urhen.com

    ls = None

    current_language = lingo.get_current_language_abbr()

    # print(lingo.get_active_skills(current_language)[0]['locked'])

    for topic in lingo.get_active_skills(current_language):
        if lingo.get_skills_in_progress(current_language)[0] in topic.values():
            ls = lingo.get_current_learnsession(topic)



    # for challenge in ls.getChallengeList():
    #     exercise = DuolingoLearnSessionChallenge(challenge)
    #     target_lang = challenge['metadata']['target_language_name']
    #     print(exercise.getSourcePrompt(target_lang))
    #     print(exercise.getCorrectSolutions())
    #     print()