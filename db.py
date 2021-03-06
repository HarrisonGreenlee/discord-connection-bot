import sqlite3
import ast
import math

SURVEY_LENGTH = 3

class User:
    def __init__(self, id):
        self.id = id
        
        database_cursor.execute("SELECT * FROM userdata WHERE id = :id", {'id': id})
        user_data = database_cursor.fetchone()
        
        if(user_data is not None):
            self.survey_data = ast.literal_eval(user_data[1])
        else:
            self.survey_data = []
            for _ in range(SURVEY_LENGTH):
                self.survey_data.append(None)
        
    def add_data(self, survey_num, survey_data):
        self.survey_data[survey_num] = survey_data
        
    def all_questions_are_answered(self):
        for i in range(SURVEY_LENGTH):
            if(self.survey_data[i] is None):
                return False
        return True
        
    def commit_to_database(self):
        if(not self.all_questions_are_answered()):
            return False
        
        with database_connection:
            database_cursor.execute("INSERT INTO userdata VALUES (:id, :surveydata)", {'id': self.id, 'surveydata': str(self.survey_data)})
            return True
        
        return False
    
    def similarity_index(self, other):
        if(self.all_questions_are_answered() and other.all_questions_are_answered()):
            components = [(x - y)**2 for x, y in zip(self.survey_data, other.survey_data)]
            return math.sqrt(sum(components))
        
        return -1
        
database_connection = sqlite3.connect("userdata.db")
database_cursor = database_connection.cursor()

# If the database table does not exist, create one.
# This is mostly just for testing purposes.
database_cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata'")
if database_cursor.fetchone()[0] != 1:
    database_cursor.execute("""CREATE TABLE userdata (
                                id integer,
                                surveydata string
                            )""")