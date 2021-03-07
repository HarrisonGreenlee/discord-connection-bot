def get_questions():
    uncleaned_questions = open('Questions.txt').readlines()
    questions = []
    arr = '```diff\n'
    for question in uncleaned_questions:
        if question == '\n':
            questions.append(arr + '```')
            arr = '```diff\n'
        else:
            arr = arr + question

    return questions


# gets the introduction to our program
def get_intro():
    return open("Introduction.txt").read()
