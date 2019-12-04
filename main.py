import duolingo
from lschallenge import DuolingoLearnSessionChallenge
from pprint import pprint

#lingo  = duolingo.Duolingo('Robin143310')

if __name__ == "__main__":    
    lingo = duolingo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com
    ls = None

    print(lingo.get_learned_skills('en'))

    for topic in lingo.get_learned_skills('en'):
            if "Grundl. 1" in topic.values():

                ls = lingo.get_current_learnsession(topic)



    for challenge in ls.getChallengeList():
        exercise = DuolingoLearnSessionChallenge(challenge)
        target_lang = challenge['metadata']['target_language_name']
        print(exercise.getSourcePrompt(target_lang))