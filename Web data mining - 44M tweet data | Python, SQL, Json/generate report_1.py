#analyzing tweet data
#44M tweet data in the following url
#http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt


import os


import re, sqlite3, json
import urllib.request as urllib
import sqlite3
import time




#3a.

import uuid

conn = sqlite3.connect('final_1d.db')

c = conn.cursor()

start = time.time()

output = open('text_3a.txt', 'w', encoding='utf-8')

usercontent = c.execute('SELECT * FROM user;').fetchall() 

for rows in usercontent:
            
    #add a unique ID column which has to be a string
    unique_ID  = str(uuid.uuid1())
    
    #a sequence of INSERT statements
    insert = 'insert into user values( ' + "'" + unique_ID + "'" + ', '
    
    for tup in rows:
        
        # Convert None to NULL
        if tup == None:
            
            insert = insert + 'NULL' + ', '
        
        else:
            
            if isinstance(tup, (int, float)):
                
                value = str(tup)
                            
            else:
                
                # Escape all single quotes in the string
                value = "'" + str(tup).replace("'", "''") + "'"
                                       
                
            insert = insert + value + ', '
            
    insert = insert[:-2] + '); \n\n'
    
    #Export to a file
    output.write(insert)
    
output.close()
               
end = time.time()

#runtime
print("3a time : ", end-start)

conn.commit()
conn.close()




#3b.

import uuid

start = time.time()

fd = open('text_1b.txt', 'r', encoding = 'utf-8')

output = open('text_3b.txt', 'w', encoding='utf-8')


for i in range(500000):
    
    Line = fd.readline()
    
    try:
        
        tDict = json.loads(Line)
                        
        #add a unique ID column which has to be a string
        unique_ID  = str(uuid.uuid1())
        
        uservalues=[
            unique_ID,
            tDict['user']['id'],
            tDict['user']['name'],
            tDict['user']['screen_name'],
            tDict['user']['description'],
            tDict['user']['friends_count']
                ]
        # Convert None to NULL
        for j in range(0, len(uservalues)):
            
            if uservalues[j] == None:
                uservalues[j] = 'Null'
            else:
                if isinstance(uservalues[j], (int, float)):
                    
                    uservalues[j] = str(uservalues[j])
                    
                else:
                # Escape all single quotes in the string
                    uservalues[j] = "'" + str(uservalues[j]).replace("'", "''") + "'"
                
               
        #a sequence of INSERT statements
        insert = "INSERT or IGNORE INTO  user VALUES({},{},{},{},{},{}); \n\n".format(uservalues[0],uservalues[1],uservalues[2],uservalues[3],uservalues[4],uservalues[5])
        
        #Export to a file
        output.write(insert)
            
    
    except(ValueError):
        
        continue
    

output.close()
end = time.time()

#runtime
print("3b time : ", end-start)















