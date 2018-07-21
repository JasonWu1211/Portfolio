#analyzing tweet data
#44M tweet data in the following url
#http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt

import os


import re, sqlite3, json
import urllib.request as urllib
import sqlite3
import time



#1a.

geotable = '''

CREATE TABLE geo (

id INTEGER PRIMARY KEY AUTOINCREMENT,
  
type VARCHAR(10),
  
longitude number,
  
latitude  number,
 
unique(type,longitude,latitude)
 
);

'''

usertable='''

create table user (

id     number(50),

name     varchar(60), 
 
screen_name     varchar(60), 

description     varchar(200),
 
friends_count     NUMBER(10), 

CONSTRAINT user_PK PRIMARY KEY (id)

);

'''

tweettable='''

create table tweet (

created_at     date,

id_str     VARCHAR(50), 

text     varchar(200), 

source     varchar(200) DEFAULT NULL,
 
in_reply_to_user_id     number(20), 

in_reply_to_screen_name     varchar(60), 

in_reply_to_status_id     number(20),
 
retweet_count     NUMBER(10), 

contributors     VARCHAR(200),

user_id         number(50),

geo_id          integer,

CONSTRAINT TWEET_PK PRIMARY KEY (id_str),

CONSTRAINT TWEET_FK1 FOREIGN KEY (user_id) REFERENCES user(id),

CONSTRAINT TWEET_FK2 FOREIGN KEY (geo_id) REFERENCES geo(id)

);

'''


conn = sqlite3.connect('final_1c.db')

c = conn.cursor()
c.execute('pragma foreign_keys=ON')

c.execute('DROP TABLE IF EXISTS tweet')
c.execute('DROP TABLE IF EXISTS user')
c.execute('DROP TABLE IF EXISTS geo')

c.execute(geotable)
c.execute(usertable)
c.execute(tweettable)



#1b.

start = time.time()

response = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")

fd = open('text_1b.txt', 'wb')

for i in range(500000):
    str_response = response.readline()
    fd.write(str_response)

fd.close    

end = time.time()


#execution time
print("1b time : ", end-start)





#1c.

start = time.time()

response = urllib.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt")

#populate the 3-table schema 
for i in range(500000):
    
    str_response = response.readline().decode("utf8")
    
         
    try:
        
        tDict = json.loads(str_response)
        
        
        if tDict['geo'] is not None:
            
            longitude = tDict['geo']['coordinates'][0]
            latitude = tDict['geo']['coordinates'][1]
            #print(longitude)
            #print(latitude)
            
            geovalues=[
                tDict['geo']['type'],
                longitude,
                latitude
                    ]
            
           
            c.execute("INSERT or IGNORE INTO geo(type, longitude, latitude) Values(?,?,?)", geovalues)
            

            geo_id = c.execute("select id from geo where type = ? and longitude = ? and latitude = ?;", (tDict['geo']['type'],longitude,latitude)).fetchall()[0][0]
            
            
            #print(geo_id)
            
        
        else:
            
            geo_id = None
            #print(geo_id)





        uservalues=[
            tDict['user']['id'],
            tDict['user']['name'],
            tDict['user']['screen_name'],
            tDict['user']['description'],
            tDict['user']['friends_count']
                ]
                
                
        c.execute("INSERT or IGNORE INTO  user VALUES(?,?,?,?,?);",uservalues)
        
        
        
        if 'retweeted_status' in tDict.keys():
            
            retweetcount = tDict['retweeted_status']['retweet_count']
        
    
        
        else:
            
            retweetcount = tDict['retweet_count']
            

        

        
        tweetvalues =[
            tDict['created_at'],
            tDict['id_str'],
            tDict['text'],
            tDict['source'],
            tDict['in_reply_to_user_id'],
            tDict['in_reply_to_screen_name'],
            tDict['in_reply_to_status_id'],
            retweetcount,
            tDict['contributors'],
            tDict['user']['id'],
            geo_id
                ]
                  
        
        
                  
        c.execute("INSERT  or IGNORE INTO  tweet VALUES(?,?,?,?,?,?,?,?,?,?,?);",tweetvalues)
    


    
    except(ValueError):
        
        continue
    
end = time.time()


#execution time
print("1c time : ", end-start)



#report row counts for each of the 3 tables
counttweetrow = 0
for row in c.execute("SELECT * FROM tweet;"):
    counttweetrow += 1
    #print(row)

countuserrow = 0
for row in c.execute("SELECT * FROM user;"):
    countuserrow += 1

countgeorow = 0
for row in c.execute("SELECT * FROM geo;"):
    countgeorow += 1

  
print('tweet_rows: %s \nuser_rows: %s \ngeo_rows: %s ' %(counttweetrow,countuserrow,countgeorow))

conn.commit()
conn.close()


#1d.

conn = sqlite3.connect('final_1d.db')

c = conn.cursor()
c.execute('pragma foreign_keys=ON')

c.execute('DROP TABLE IF EXISTS tweet')
c.execute('DROP TABLE IF EXISTS user')
c.execute('DROP TABLE IF EXISTS geo')

c.execute(geotable)
c.execute(usertable)
c.execute(tweettable)


start = time.time()

fd = open('text_1b.txt', 'r', encoding = 'utf-8')

#populate the 3-table schema 
for i in range(500000):
    
    Line = fd.readline()
    
    try:
        
        tDict = json.loads(Line)
        
        
        if tDict['geo'] is not None:
            
            longitude = tDict['geo']['coordinates'][0]
            latitude = tDict['geo']['coordinates'][1]
            #print(longitude)
            #print(latitude)
            
            geovalues=[
                tDict['geo']['type'],
                longitude,
                latitude
                    ]
            
           
            c.execute("INSERT or IGNORE INTO geo(type, longitude, latitude) Values(?,?,?)", geovalues)
            

            geo_id = c.execute("select id from geo where type = ? and longitude = ? and latitude = ?;", (tDict['geo']['type'],longitude,latitude)).fetchall()[0][0]
            
            
            #print(geo_id)
            
        
        else:
            
            geo_id = None
            #print(geo_id)





        uservalues=[
            tDict['user']['id'],
            tDict['user']['name'],
            tDict['user']['screen_name'],
            tDict['user']['description'],
            tDict['user']['friends_count']
                ]
                
                
        c.execute("INSERT or IGNORE INTO  user VALUES(?,?,?,?,?);",uservalues)
        
        
        
        if 'retweeted_status' in tDict.keys():
            
            retweetcount = tDict['retweeted_status']['retweet_count']
        
    
        
        else:
            
            retweetcount = tDict['retweet_count']
            

        

        
        tweetvalues =[
            tDict['created_at'],
            tDict['id_str'],
            tDict['text'],
            tDict['source'],
            tDict['in_reply_to_user_id'],
            tDict['in_reply_to_screen_name'],
            tDict['in_reply_to_status_id'],
            retweetcount,
            tDict['contributors'],
            tDict['user']['id'],
            geo_id
                ]
                  
        
        
                  
        c.execute("INSERT  or IGNORE INTO  tweet VALUES(?,?,?,?,?,?,?,?,?,?,?);",tweetvalues)
    


    
    except(ValueError):
        
        continue
    


end = time.time()


#execution time
print("1d time : ", end-start)

#report row counts for each of the 3 tables
counttweetrow = 0
for row in c.execute("SELECT * FROM tweet;"):
    counttweetrow += 1
    #print(row)

countuserrow = 0
for row in c.execute("SELECT * FROM user;"):
    countuserrow += 1

countgeorow = 0
for row in c.execute("SELECT * FROM geo;"):
    countgeorow += 1

  
print('tweet_rows: %s \nuser_rows: %s \ngeo_rows: %s ' %(counttweetrow,countuserrow,countgeorow))

conn.commit()
conn.close()



#1e.

conn = sqlite3.connect('final_1e.db')

c = conn.cursor()
c.execute('pragma foreign_keys=ON')

c.execute('DROP TABLE IF EXISTS tweet')
c.execute('DROP TABLE IF EXISTS user')
c.execute('DROP TABLE IF EXISTS geo')

c.execute(geotable)
c.execute(usertable)
c.execute(tweettable)



def loadtables(lines):
    
    try:
        
        batchRows = 500
        batchedInserts_geo = []
        batchedInserts_user = []
        

        while len(lines) > 0:
            
            line = lines.pop(0)
            
            tDict = json.loads(line)
            
            newRow_geo=[]
            
            
            if tDict['geo'] is not None:
                
                geovalues=[tDict['geo']['type'],tDict['geo']['coordinates'][0],tDict['geo']['coordinates'][1]]
            
                for value in geovalues:
                    
                                                   
                    # Treat '', [] and 'null' as NULL
                    if value in ['',[],'null']:
                    
                        newRow_geo.append(None)
                    
                    else:
                    
                    
                        newRow_geo.append(value)


                batchedInserts_geo.append(newRow_geo)

                                    
            newRow_user = []                    
            uservalues=[
                tDict['user']['id'],
                tDict['user']['name'],
                tDict['user']['screen_name'],
                tDict['user']['description'],
                tDict['user']['friends_count']
                        ]
                        
            for value in uservalues:
                
            
                
                # Treat '', [] and 'null' as NULL
                if value in ['',[],'null']:
                
                    newRow_user.append(None)
            
                else:
                    
                    newRow_user.append(value)

             
            batchedInserts_user.append(newRow_user)
                        

            if min(len(batchedInserts_user),len(batchedInserts_user)) >= batchRows or len(lines) == 0:
                
                                    
                c.executemany("INSERT or IGNORE INTO geo(type, longitude, latitude) Values(?,?,?)", batchedInserts_geo)
                    
                batchedInserts_geo = []
                    
                c.executemany("INSERT or IGNORE INTO  user VALUES(?,?,?,?,?);", batchedInserts_user)
                 
                batchedInserts_user = []
                
    except(ValueError):        
                
        pass
        

def loadtweet(lines):
    
    try:
        batchRows = 500    
        
        batchedInserts_tweet = []
                                  
        while len(lines) > 0:
            
            line = lines.pop(0)
            
            tDict = json.loads(line)
            
            newRow_tweet = []
                    
            if 'retweeted_status' in tDict.keys():
                            
                retweetcount = tDict['retweeted_status']['retweet_count']
                    
            else:
                           
                retweetcount = tDict['retweet_count']

                        
            if tDict['geo'] is not None:
                            
                geo_type = tDict['geo']['type']
                longitude = tDict['geo']['coordinates'][0]
                latitude = tDict['geo']['coordinates'][1]
                geo_id = c.execute("select id from geo where type = ? and longitude = ? and latitude = ?;", (geo_type,longitude,latitude)).fetchall()[0][0]
        
            else:

                geo_id = None
                
                
                
            tweetvalues =[
                tDict['created_at'],
                tDict['id_str'],
                tDict['text'],
                tDict['source'],
                tDict['in_reply_to_user_id'],
                tDict['in_reply_to_screen_name'],
                tDict['in_reply_to_status_id'],
                retweetcount,
                tDict['contributors'],
                tDict['user']['id'],
                geo_id
                        ]
                        
            for value in tweetvalues:
            
                
                # Treat '', [] and 'null' as NULL
                if value in ['',[],'null']:
                    
                    newRow_tweet.append(None)
                
                else:
                
                    
                    newRow_tweet.append(value)

             
            batchedInserts_tweet.append(newRow_tweet)

             
            if len(batchedInserts_tweet) >= batchRows or len(lines) == 0:
                
                
                c.executemany('INSERT or ignore INTO tweet VALUES(?,?,?,?,?,?,?,?,?,?,?)', batchedInserts_tweet)
                 
                batchedInserts_tweet = []
    
    except(ValueError):
                
        pass




start = time.time()

fd = open('text_1b.txt', 'r', encoding = 'utf-8')
lines = fd.readlines()
loadtables(lines)
fd = open('text_1b.txt', 'r', encoding = 'utf-8')
lines = fd.readlines()
loadtweet(lines)
    
end = time.time()


#execution time
print("1e time : ", end-start)

#report row counts for each of the 3 tables
print ("tweet Loaded ", c.execute('SELECT COUNT(*) FROM tweet').fetchall()[0][0], " rows")
print ("user Loaded ", c.execute('SELECT COUNT(*) FROM user').fetchall()[0][0], " rows")
print ("geo Loaded ", c.execute('SELECT COUNT(*) FROM geo').fetchall()[0][0], " rows")

conn.commit()
conn.close()





