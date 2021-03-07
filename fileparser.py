import message_formatter as mf


# gets the questions from a text file
def get_questions(avatar):
    uncleaned_questions = open('Questions.txt').readlines()
    questions = []
    title = ''
    description = ''
    for question in uncleaned_questions:
        if question == '\n':
            questions.append(mf.create_question(title, description, avatar))
            description = ''
        elif question.startswith('-'):
            description += question
        else:
            title = question

    return questions


# gets the introduction to our program
def get_intro():
    return open("Introduction.txt").read()
