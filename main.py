import duolingo
from lschallenge import DuolingoLearnSessionChallenge
from pprint import pprint

#lingo  = duolingo.Duolingo('Robin143310')

if __name__ == "__main__":    
    lingo = duolingo.Duolingo('DSA975012', password='sprachassist') # E-mail - d21292@urhen.com

    ls = None

    current_language = lingo.get_current_language_abbr()

    # print(lingo.get_learned_skills(current_language))

    for topic in lingo.get_learned_skills(current_language):
        if lingo.get_skills_in_progress(current_language)[0] in topic.values():
            ls = lingo.get_current_learnsession(topic)



    for challenge in ls.getChallengeList():
        exercise = DuolingoLearnSessionChallenge(challenge)
        target_lang = challenge['metadata']['target_language_name']
        print(exercise.getSourcePrompt(target_lang))