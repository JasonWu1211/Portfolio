#analyzing tweet data
#44M tweet data in the following url
#http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt


import os


import re, sqlite3, json
import urllib.request as urllib
import sqlite3
import time

conn = sqlite3.connect('final_1d.db')

c = conn.cursor()



#4a.

geocontent = c.execute("SELECT * FROM geo;").fetchall()

output = open('text_4a.txt', 'w', encoding='utf-8')

lastrowid = 0

for row in geocontent:
    
    text=''
     
    for value in row:
        
        if isinstance(value, (float)):
            
            #round longitude and latitude to a maximum of 4 digits after the decimal
            text += str("{0:.4f}".format(value)) + ' | '
        
        elif isinstance(value, (int)):
            
            lastrowid = value
                
            text += str(value) + ' | '
                
        else: 
            
            text += "'" + str(value) + "'" + ' | '                    
      
    
    output.write(text)
    
    output.write("\n")

unknown_id = lastrowid +1

#create a single default entry for the ‘Unknown’ location
output.write( str(unknown_id) + ' | ' + "'" + str('unknown') + "'" + ' | ' + "'" + str('unknown') + "'" + ' | ' + "'" + str('unknown') + "'" + ' | ' )

output.close()



#4b.

tweetcontent = c.execute("SELECT * FROM tweet;").fetchall()

output = open('text_4b.txt', 'w', encoding='utf-8')

count_known = 0
count_unknown = 0
count_total =0

for row in tweetcontent:
    
    count_total += 1
    
    text=''
    
    valuelist=list(row)
    
    #replace NULLs by a reference to ‘Unknown’ entry 
    if valuelist[10] is None:
        
        count_unknown += 1
        
        valuelist[10] = unknown_id
        
    else:
         
        count_known += 1
    
    
    
    for value in valuelist:
        
        if value == None:
            
            text += 'NULL' + ' | ' 
        
        
        else:
            
            if isinstance(value, (int, float)):
                
                text += str(value) + ' | '
            
            else:
                
                text += "'" + str(value) + "'" + ' | '                    

    
     
    output.write(text)

    output.write("\n\n\n")

knownpercent= "{0:.4f}".format((count_known/count_total)*100)

#Report how many known/unknown locations there were in total 
print('{} known \n{} unknown  \n{}% locations are available'.format(count_known,count_unknown,knownpercent))

output.close()




#4c.

usercontent = c.execute("SELECT * FROM user;").fetchall()

output = open('text_4c.txt', 'w', encoding='utf-8')

for row in usercontent:
    
    text=''
    
    uservaluelist=list(row)
    
    
    for i in range(0,len(uservaluelist)):
        
        
        if uservaluelist[i] == None:
            
            uservaluelist[i] = 'NULL'
            
            text += 'NULL' + ' | '
        
        else:
            
            if isinstance(uservaluelist[i], (int, float)):
                
                text += str(uservaluelist[i]) + ' | '
            
            else:
                
                text += "'" + str(uservaluelist[i]) + "'" + ' | '
    
    
    screen_name = uservaluelist[2]
    
    description = uservaluelist[3]
    
    name = uservaluelist[1]
    
    #add a column (true/false)
    if name in screen_name or name in description:
            
        text+= ('true') + ' | '
        
    else:
            
        text+= ('false') +  ' | '
             
    output.write(text)            
    
    output.write("\n\n\n")  

output.close()


conn.commit()
conn.close()
