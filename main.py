from message_processing import db_connection
import re
import os
import os.path


pattern1 = r'[А-ЯЁ].+'
pattern2 = r'[а-яё].+'

for current_dir, dirs, files in os.walk('Subtitles'):
    for fileName in files:
        if '.srt' in fileName:
            print('Working with ' + current_dir + '/' + fileName)
            with open(current_dir + '/' + fileName, 'r') as file:
                lineB = 'Системная строка'
                lineH = ''
                for line in file:
                    if len(re.findall(pattern1, line)) > 0:
                        #print(lineB)
                        #print(lineH)
                        #print()
                        db_connection(textH=lineH, textB=lineB, incert_in=True)
                        lineB = lineH
                        lineH = re.findall(pattern1, line)[0].strip()
                    elif len(re.findall(pattern2, line)) > 0:
                        lineH += ' ' + re.findall(pattern2, line)[0].strip()
            print('Done')
