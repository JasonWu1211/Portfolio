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



#2a.

#i.

start = time.time()
query2ai = c.execute("select text FROM tweet Where id_str like '%44%' or id_str like '%77%' ;").fetchall()
end = time.time()
print("2a_i time : ", end-start)
#count = c.execute("select count(id_str) FROM tweet Where id_str like '%44%' or id_str like '%77%' ;").fetchall()

#ii.

start = time.time()
query2aii = c.execute("select count(distinct in_reply_to_user_id) FROM tweet;").fetchall()
end = time.time()
print("2a_ii time : ", end-start)

#iii.

start = time.time()
query2aiii = c.execute("SELECT text FROM tweet where length(text) = (select max(length(text)) from tweet);").fetchall()
end = time.time()
print("2a_iii time : ", end-start)
#maxlen = c.execute('select max(length(text)) from tweet;').fetchall()

#iv.

start = time.time()
query2aiv = c.execute("select u.name, avg(longitude), avg(latitude) from tweet t, geo g, user u where t.geo_id = g.id and t.user_id = u.id group by u.name;").fetchall()
end = time.time()
print("2a_iv time : ", end-start)
count =c.execute("select count(distinct u.name) from tweet t, geo g, user u where t.geo_id = g.id and t.user_id = u.id;").fetchall()

#v.

start = time.time()
for i in range(10):
    query2aiv = c.execute("select u.name, avg(longitude), avg(latitude) from tweet t, geo g, user u where t.geo_id = g.id and t.user_id = u.id group by u.name;").fetchall()
end = time.time()
print("2a_v 10times running time : ", end-start)

begin = time.time()
for i in range(100):
    query2aiv = c.execute("select u.name, avg(longitude), avg(latitude) from tweet t, geo g, user u where t.geo_id = g.id and t.user_id = u.id group by u.name;").fetchall()
end = time.time()
print("2a_v 100times running time : ", end-start)


#2b.

#2b_i.

fd = open('text_1b.txt', 'r', encoding = 'utf-8')

start = time.time()

tweet_dic = {}

for i in range(500000):
    
    Line = fd.readline()
    
    try:
        tDict = json.loads(Line)
        
        if '44' in tDict['id_str'] or '77' in tDict['id_str']:
            
            tweet_dic.setdefault(tDict['id_str'], []).append(tDict['text'])
                                       
    
    except(ValueError):
        
        continue


tweet_Keys = tweet_dic.keys()
tweet_Vals = tweet_dic.values()
#print(len(tweet_Keys))
print(len(tweet_Vals))

end = time.time()

print("2b_i time : ", end-start)


#2b_ii.

fd = open('text_1b.txt', 'r', encoding = 'utf-8')

start = time.time()

distinct_in_reply_to_user_id =[]

for i in range(500000):
    
    Line = fd.readline()
    
    try:
        tDict = json.loads(Line)
        if tDict['in_reply_to_user_id'] is not None:
            
            if tDict['in_reply_to_user_id'] not in distinct_in_reply_to_user_id:
                
                distinct_in_reply_to_user_id.append(tDict['in_reply_to_user_id'])
           
    
    
    
    except(ValueError):
        
        continue
    
print(len(distinct_in_reply_to_user_id))

end = time.time()

print("2b_ii time : ", end-start)




#2c.
#extra-credit


fd = open('text_1b.txt', 'r', encoding = 'utf-8')

start = time.time()
maxlen = 0

for i in range(500000):
    
    Line = fd.readline()
    
    try:
        tDict = json.loads(Line)
        
        if len(tDict['text']) > maxlen:
            
            maxlen = len(tDict['text'])
            
           
    
    
    
    except(ValueError):
        
        continue

    
fd = open('text_1b.txt', 'r', encoding = 'utf-8')

max_len_text_lst=[]

for i in range(500000):
    
    Line = fd.readline()
    
    try:
        tDict = json.loads(Line)
        
        if len(tDict['text']) == maxlen:
            
            max_len_text_lst.append(tDict['text'])
            
           
    
    
    
    except(ValueError):
        
        continue
    
print('max_len: %s' %(maxlen))
print(max_len_text_lst)

end = time.time()

print("2c time : ", end-start)




#2d.
#extra-credit

fd = open('text_1b.txt', 'r', encoding = 'utf-8')

start = time.time()

lon_dic={}
lat_dic={}

for i in range(500000):
    
    Line = fd.readline()
    
    try:
        tDict = json.loads(Line)
        
        if tDict['geo'] is not None:
            
            longitude = tDict['geo']['coordinates'][0]
            latitude = tDict['geo']['coordinates'][1]
            
            lon_dic.setdefault(tDict['user']['name'], []).append(longitude) 
            lat_dic.setdefault(tDict['user']['name'], []).append(latitude)
           
    
    
    
    except(ValueError):
        
        continue

#find average;
avg = lambda lst: float(sum(lst))/len(lst)
ave_longitude = {item: avg(values) for item, values in lon_dic.items()}
ave_latitude = {item: avg(values) for item, values in lat_dic.items()}

#merge two dic;
merge = {}

for d in (lon_dic,lat_dic):
    for key, value in d.items():
       merge.setdefault(key, []).append(value)

print(merge)

end = time.time()

print("2d time : ", end-start)




conn.commit()
conn.close()
