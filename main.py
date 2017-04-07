from message_processing import text_processing
import re
import os.path
import sqlite3


DATABASE_NAME = 'Data/new_database.sqlite'


def db_connection():
    """

    Create the tables needed by the program

    """

    global cursor

    # create the tables needed by the program
    try:
        # create the table containing the words
        cursor.execute('''
                CREATE TABLE words (
                    word TEXT UNIQUE
                )
            ''')
        # create the table containing the sentences
        cursor.execute('''
                CREATE TABLE sentences (
                    sentence TEXT UNIQUE,
                    used INT NOT NULL DEFAULT 0
                )''')
        # create association between weighted words and the next sentence
        cursor.execute('''
                CREATE TABLE associations (
                    word_id INT NOT NULL,
                    sentence_id INT NOT NULL,
                    weight REAL NOT NULL)
            ''')
        cursor.execute('''
                CREATE TABLE last_messages (
                    chat_id INT NOT NULL,
                    last_message TEXT UNIQUE)
            ''')
    except:
        pass


#main function

pattern1 = r'[А-ЯЁ].+'
pattern2 = r'[а-яё].+'

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()
db_connection()

for current_dir, dirs, files in os.walk('Subtitles'):
    for fileName in files:
        if '.srt' in fileName:
            print('Working with ' + current_dir + '/' + fileName)
            with open(current_dir + '/' + fileName, 'r') as file:
                lineB = 'Абракадабра'
                lineH = 'Абракадабра'
                for line in file:
                    line.replace('<i>', '')
                    line.replace('</i>', '')
                    if len(re.findall(pattern1, line)) > 0:
                        #print(lineB)
                        #print(lineH)
                        #print()
                        cursor = text_processing(lineH, lineB, connection, cursor, incert_in=True)
                        lineB = lineH
                        lineH = re.findall(pattern1, line)[0].strip()
                    elif len(re.findall(pattern2, line)) > 0:
                        lineH += ' ' + re.findall(pattern2, line)[0].strip()
            print('Done')

connection.close()


