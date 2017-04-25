# -*- coding: utf-8 -*-
import sys
import glob
import urllib.parse

path = '/home/tengmo/workwithcrawler/2000file/*.arc'
#path = '/home/tengmo/workwithcrawler/store/*.arc'

files = glob.glob(path)
def Find_site(f):
    URL = ''
    Nb_point =0
    Nb_slash =0
    cnt = 0
    for line in f:
        cnt = 0
        for char in line:
            cnt +=1
            if char == ' ':
                break
            if char == '.':
                Nb_point +=1
            if char == '/':
                Nb_slash +=1
            if Nb_slash == 3:
                break
            if Nb_point == 2:
                break
            if cnt > 7:
                URL += char
        break
    #print (URL)
    if "www." in URL:
        cnt = 0
        new_URL =''
        for char in URL:
            cnt+=1
            if cnt >4:
                new_URL += char
    #    print (new_URL)
    else:
        new_URL =''
        for char in URL:
            if char == '.':
                break
            new_URL += char
        #print (new_URL)

    #URL = urllib.parse.unquote(URL)
    return new_URL
cnt = 0
my_dict = {}
for name in files:
    #try:
        with open(name) as f:
            cnt +=1
            URL = Find_site(f)
            print (URL)


            if URL in my_dict:
                my_dict[URL] += 1
            else:
                my_dict[URL] = 1
            #print(URL)




    #except IOError as exc:
    #    if exc.errno != errno.EISDIR:
    #        print('Yo!!')
    #        raise
print (str(my_dict))
with open('/home/tengmo/workwithcrawler/new_source_code/dict_site.txt' , 'w') as out:
    out.write("{")
    for k,v in my_dict.items():
        out.write("\"")
        out.write(str(k))
        out.write("\"")
        out.write(":")
        out.write(str(v))
        out.write(",")
        out.write('\n')
    out.write("}")
#for k,v in my_dict.items():
#    print (k, " : ",v)
