import message_formatter as mf
from db import SURVEY_LENGTH


# gets the questions from a text file
def get_questions():
    uncleaned_questions = open('Questions.txt').readlines()
    questions = []
    title = ''
    description = ''
    for question in uncleaned_questions:
        if question == '\n':
            questions.append(mf.create_question("Question {0}/{1}:".format(str(len(questions) + 1),
                                                                           str(SURVEY_LENGTH)), title, description))
            description = ''
        elif question.startswith('-'):
            description += question
        else:
            title = question

    return questions


# gets the introduction to our program
def get_intro():
    return open("Introduction.txt").read()
