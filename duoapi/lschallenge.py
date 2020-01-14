import json
from .user_answer_check import UserAnswerCheck

class DuolingoLearnSessionChallenge(object):
    def __init__(self, challengeJsonObject):
        self.challenge = challengeJsonObject
        self.type = challengeJsonObject["metadata"]["type"]
        self.targetLang = self.challenge['metadata']['target_language_name']

    def get_answer_language(self):
        """ Returns the language in which the question should be answered"""
        return self.targetLang

    def get_source(self):
        """
        Word of origin
        """
        if self.challenge["metadata"]["specific_type"] == "name_example": 
            """name_example = Welches davon ist? Mit Bild """
            return self.challenge["metadata"]["hint"]
        elif self.challenge["type"] == "judge" or self.challenge["type"] == "translate" or self.challenge["type"] == "name":
            return self.challenge["prompt"]
        elif self.challenge["type"] == "speak":
            return self.challenge["metadata"]["text"]
        else:
            return self.challenge["solutionTranslation"]

    def get_source_prompt(self):
        """
            Actual question
            judge = Such aus den drei das richtige raus
            speak = Lies diesen Satz vor 
            translate: Schreibe dies in X
            name: Schreibe X in Franzoesisch (vorgegebene Artikel) 
            form: Wähle das fehlende Wort (bspw: Est-... chez elle) Notiz: ggf. ignorieren
            Auch möglich: Et surtout, je dois X quand (War hier savoir, Antwortmöglichkeiten stehen in choices
        """
        if self.challenge["metadata"]["specific_type"] == "name_example": 
            """name_example = Welches davon ist? Mit Bild """
            """choice[x]["image"] würde den Bildpfad ergeben"""
            choiceCount = len(self.challenge["choices"])
            choiceWordList = [self.challenge["choices"][i]["phrase"] for i in range(0, choiceCount)]
            
            question = "Welches der folgenden ist " + self.get_source() + "? " + ', '.join(choiceWordList)

            """ Replacing last "," with "oder" """
            question_spl = question.rsplit(",", 1)
            question = " oder".join(question_spl) + "?"
            return question
        elif self.challenge["type"] == "judge":
            choiceCount = len(self.challenge["choices"])
            choiceList = [str(i + 1) + ".: " + self.challenge["choices"][i] for i in range(0, choiceCount)]
            
            question = "Welche der folgenden Antworten ist richtig? Der Satz lautet: " + self.get_source()
            question += "\nDie Antwortmöglichkeiten lauten wie folgt: " + '\n'.join(choiceList)
            """ Replacing last "," with "oder" """
            question_spl = question.rsplit("\n", 1)
            question = " oder\n".join(question_spl)
            return question
        elif self.challenge["type"] == "speak":
            """ In challenge["metadata"]["non_character_tts"]['normal'] steht eine URL zu einer Vorlesedatei! """
            return "Bitte lies diesen Satz vor: " + self.get_source()
        elif self.challenge["type"] == "translate":
            return "Übersetze folgendes nach {}: ".format(self.targetLang) + self.get_source()
        elif self.challenge["type"] == "name":
            return "Wie übersetzt man \"" + self.get_source() + "\"?"
        elif self.challenge["type"] == "form":            
            question = "Wähle das fehlende Wort: " + \
            self.challenge["promptPieces"][0] + ", Lücke, " +  \
            (self.challenge["promptPieces"][1] if self.challenge["promptPieces"][1] != "." else "")
            choiceCount = len(self.challenge["choices"])
            choiceList  = [str(i + 1) + ".: " + self.challenge["choices"][i] for i in range(0, choiceCount)]

            question += "\nZur Auswahl stehen: "+ '\n'.join(choiceList)
            """ Replacing last "," with "und" """
            question_spl = question.rsplit("\n", 1)
            question = " oder\n".join(question_spl)
            return question
        else:
            return self.challenge["solutionTranslation"]

    def get_correct_solutions(self):
        """
        Note: Antworten können auch freiwillige Angaben nach Schema "Er [muss/soll][/ sich] baden." enthalten
        """
        if self.type == "speak":
            return self.challenge["solutionTranslation"]
        elif self.type == "translate":
            return self.challenge["compactTranslations"]
        elif self.type == "select":            
            return self.challenge["metadata"]["correct_solutions"]
        elif self.type == "judge":          
            correctChoiceIndex = self.challenge["metadata"]["correct_solutions"][0]
            return self.challenge["metadata"]["options"][correctChoiceIndex]["sentence"]
        elif self.type == "form":            
            return self.challenge["metadata"]["correct_solutions"]
        elif self.type == "name":  
            return self.challenge["metadata"]["correct_solutions"]
        else:
            return self.challenge["compactSolutions"]

    def check_answer(self, user_input):
        solution_response = UserAnswerCheck(user_input).checkAnswer(self.get_correct_solutions())
        return solution_response


if __name__ == '__main__':
    from pprint import pprint
    """ Sample Data """
    with open('sampleLearnSession.json', 'r') as f:
        __sampleData__ = json.load(f)

        for x in range(0, 20):
            ls = DuolingoLearnSessionChallenge(__sampleData__["challenges"][x])
            pprint(ls.get_source_prompt())
            pprint(ls.get_correct_solutions())
