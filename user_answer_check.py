import re

class UserAnswerCheck():
    def __init__(self, user_input):
        self.user_input = user_input.lower().split()

        self.choices_regex = re.compile("\[(.*?)\]")
        self.punct_regex = re.compile("[\.\?\!\,]")

    def checkAnswer(self, solutions):
        for possible_solution in solutions:
            possible_solution = re.sub(self.punct_regex, "", possible_solution).lower()
            choices = re.findall(self.choices_regex, possible_solution)
            
            answer, temp_choice = [], []
            position = 0
            correct_answer_flag = False
    
            for choicePoisition in range(len(choices)):
                possible_solution = re.sub(self.choices_regex, str(choicePoisition), possible_solution, 1)
            possible_solution = possible_solution.split()
            
            for word in possible_solution:
                if word.isdigit():
                    for choice in choices[int(word)].split("/"):
                        words_in_choice = choice.split()
                        correct_choice_flag = True
                        correct_answer_flag = True

                        for word_in_choice in words_in_choice:
                            try:
                                if word_in_choice == self.user_input[position+words_in_choice.index(word_in_choice)] or word_in_choice == "":
                                    temp_choice.append(word_in_choice)
                                else:
                                    temp_choice = []
                                    correct_choice_flag = False
                            except IndexError:
                                correct_answer_flag = False
                        if correct_choice_flag:
                            answer.extend(temp_choice)
                            position += len(temp_choice)
                            temp_choice = []
                            break
                        else:
                            correct_answer_flag = False
                else:

                    try:
                        if word == self.user_input[position]:
                            answer.append(word)
                            position += 1
                            correct_answer_flag = True
                        else:
                            correct_answer_flag = False
                    except IndexError:
                        correct_answer_flag = False
            if correct_answer_flag:
                return True
        return False