from bs4 import BeautifulSoup
import sys
import glob
import os
import csv
import time

##########-SET_PATH###########
path = '/home/tengmo/workwithcrawler/2000file/*.arc'
#path = '/home/tengmo/workwithcrawler/store/*.arc'

files = glob.glob(path)
dict_site = eval(open("/home/tengmo/workwithcrawler/source_code/dict_site.txt").read())

HAVE_TITLE = 0
NO_TITLE = 0
TH = 0
ENG = 0
OTHER = 0
NO_CONTENT =0

text_html = 0
text_plain = 0
text_Not_itdentified = 0
text_other = 0
start_time = time.time()


################################################################################
def Find_title_def(html_content):
    global HAVE_TITLE
    global NO_TITLE
    soup = BeautifulSoup(html_content, 'lxml')
    soup.find_all('a')
    try:
        if (soup.title.string) == None:
            NO_TITLE += 1
            return "No_title"

        else:
            HAVE_TITLE += 1
            return (soup.title.string)
    except AttributeError:
        NO_TITLE +=1
        return ("No_title")

################################################################################
def Find_URL(line_1):
    URL = ''
    Nb_point =0
    Nb_slash =0
    cnt = 0
    for char in line_1:
        cnt +=1
        if char == ' ':
            break
        URL += char

    return URL
################################################################################
def Find_binary_domain(URL):
    Domain_name = ''
    for char in URL[7:]:
        if(char == '/'):
            break
        Domain_name += char
    #print(Domain_name)

    list_string = ['.com', '.edu', '.gov', '.org', '.net', '.mil', '.co.th', '.in.th', '.ac.th']
    list_domain = [0,0,0,0,0,0,0,0,0,0]
    for x in range(0,9):
        if(find_str(Domain_name, list_string[x])):
            list_domain[x] += 1
    count = 0
    for x in range(0,9):
        if(list_domain[x] == 0):
            count +=1
    if count == 9:
        list_domain[9] +=1

    string =''
    for x in list_domain:
        string += str(x)
    return string

#    com = 0
#    edu = 0
#    gov = 0
#    org = 0
#    net = 0
#    mil = 0
#    co_th = 0
#    in_th = 0
#    ac_th = 0
#    other = 0

################################################################################
def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return True

            index += 1

    return False

################################################################################
def Find_site(line_1):
    site = ''
    Nb_point =0
    Nb_slash =0
    cnt = 0
    index =0
    for word in line_1.split():
        index+=1
        if index == 1:

            cnt =0
            for char in word:
                cnt +=1
                if char == '.':
                    Nb_point +=1
                if char == '/':
                    Nb_slash +=1
                if Nb_slash == 3:
                    break
                if Nb_point == 2:
                    break
                if cnt > 7:
                    site += char

    if "www." in site:
        cnt = 0
        new_site =''
        for char in site:
            cnt+=1
            if cnt >4:
                new_site += char
    else:
        new_site =''
        for char in site:
            if char == '.':
                break
            new_site += char

    return new_site

################################################################################
def Find_Nb_link_pic_table(html_content):

    soup = BeautifulSoup(html_content, 'lxml')
    soup.find_all('a')

    list_link = (soup.find_all('a'))
    list_table = (soup.find_all('table'))
    list_picture = (soup.find_all('img'))

    yield len(list_link)
    yield len(list_table)
    yield len(list_picture)
################################################################################
def Find_content(html_content):
    content = get_content_total(html_content)
    return content

###############################################################################
def get_content_total(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    text = soup.get_text()
    return text

###############################################################################
def Wordcount(content, title, charset):
    global ENG
    global NO_CONTENT
    global OTHER
    global TH

    if (charset == "Thai"):
        #content = Convert_to_Thai(content)
        newtitle = "".join(title.split())
        count_title = Wordcount_Thai(title)
        if title == "No_title":
            count_title =  0
        count_content = Wordcount_Thai(content)
        count_content -= count_title
        TH += 1
        yield count_title
        yield count_content

    elif (charset == "Eng"):
        #content = Convert_to_Eng(content)
        #title = Convert_to_Eng(title)
        count = Wordcount_Eng(content)
        count_title = Wordcount_Eng(title)
        if title == "No_title":
            count_title = 0
        count_content = count - count_title
        #print ("title :", title)

        if count_title == 0 and count_content == 0:
            NO_CONTENT += 1
        else:
            ENG += 1
        yield count_title
        yield count_content

    elif (charset == "Other"):
        OTHER  +=1
        yield -1
        yield -1

################################################################################
def Wordcount_Thai(text):
    global error
    count_word = 0
    stopword =  ["กล่าว","กว่า","กัน","กับ","การ","ก็","ก่อน","ขณะ","ขอ","ของ","ขึ้น","คง","ครั้ง","ความ",
            "คือ","จะ","จัด","จาก","จึง","ช่วง","ซึ่ง","ดัง","ด้วย","ด้าน","ตั้ง","ตั้งแต่","ตาม","ต่อ","ต่าง",
            "ต่างๆ","ต้อง","ถึง","ถูก","ถ้า","ทั้ง","ทั้งนี้","ทาง","ที่","ที่สุด","ทุก","ทํา","ทําให้","นอกจาก","นัก",
            "นั้น","นี้","น่า","นํา","บาง","ผล","ผ่าน","พบ","พร้อม","มา","มาก","มี","ยัง","รวม","ระหว่าง",
            "รับ","ราย","ร่วม","ลง","วัน","ว่า","สุด","ส่ง","ส่วน","สําหรับ","หนึ่ง","หรือ","หลัง","หลังจาก",
            "หลาย","หาก","อยาก","อยู่","อย่าง","ออก","อะไร","อาจ","อีก","เขา","เข้า","เคย","เฉพาะ","เช่น",
            "เดียว","เดียวกัน","เนื่องจาก","เปิด","เปิดเผย","เป็น","เป็นการ","เพราะ","เพื่อ","เมื่อ","เรา","เริ่ม",
            "เลย","เห็น","เอง","แต่","แบบ","แรก","และ","แล้ว","แห่ง","โดย","ใน","ให้","ได้","ไป","ไม่",
			"ไว้","ก","ข","ฃ","ค","ฅ","ฆ","ง","จ","ฉ","ช","ซ","ฌ","ญ","ฎ","ฏ","ฐ","ฑ","ฒ",
			"ณ","ด","ต","ถ","ท","ธ","น","บ","ป","ผ","ฝ","พ","ฟ","ภ","ล","ว","ศ",
            "ษ","ห","ฬ","อ","ฮ", "จาก", "ๆ", "นะ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

    with open('/home/tengmo/workwithcrawler/output_thai/cutword/input.txt' , 'w') as out:
        out.write(text)
    command= os.popen("bash cat_input.bash")
    datainput = command.read()
    #print(datainput)
    command= os.popen("bash runjava.bash")
    datainput = command.read()
    #print(datainput)
    with open('/home/tengmo/workwithcrawler/output_thai/cutword/output.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                if row['word'] not in stopword:
                    count_word += 1
        except csv.Error:
            error += 1
            return 0
    return count_word

###############################################################################
def Wordcount_Eng(text):
    stopword = ['all', "she'll", 'just', "don't", 'being', 'over', 'through',
    		   'yourselves', 'its', 'before', "he's", "when's", "we've", 'had',
    			'should', "he'd", 'to', 'only', "there's", 'those', 'under',
    			'ours', 'has', "haven't", 'do', 'them', 'his', "they'll", 'get',
    			'very', "who's", "they'd", 'cannot', "you've", 'they', 'not',
    			'during', 'yourself', 'him', 'nor', "we'll", 'like', 'did',
    			"they've", 'this', 'she', 'each', "won't", 'where', "mustn't",
    			"isn't", "i'll", "why's", 'www', 'because', "you'd", 'doing',
    			'some', 'up', 'are', 'further', 'ourselves', 'out', 'what',
    			'for', 'while', "wasn't", 'does', "shouldn't", 'above', 'between',
    			'ever', 'ought', 'be', 'we', 'who', "you're", 'were', 'here',
    			'hers', "aren't", 'by', 'both', 'about', 'would', 'of', 'could',
    			'against', "i'd", "weren't", "i'm", 'com', 'or', "can't", 'own',
    			'into', 'whom', 'down', "hadn't", "couldn't", "wouldn't", 'your',
    			"doesn't", 'from', "how's", 'her', 'their', "it's", 'there',
    			'been', 'why', 'few', 'too', 'themselves', 'was', 'until', 'more',
    			'himself', "where's", "i've", 'with', "didn't", "what's", 'but',
    			'else', 'herself', 'than', "here's", 'he', 'me', "they're",
    			'myself', 'these', "hasn't", 'below', 'r', 'can', 'theirs', 'my',
    			'k', "we'd", 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself',
    	     	'at', 'have', 'in', 'any', 'if', 'again', 'no', 'that', 'when',
    			'same', 'how', 'other', 'which', 'you', "shan't", 'http', 'shall',
    			'our', 'after', "let's", 'most', 'such', 'on', "he'll", 'a', 'off',
    			'i', "she'd", 'yours', "you'll", 'so', "we're", "she's", 'the',
    			"that's", 'having', 'once','.']

    wordcount = {}
    count= 0
    for word in text.split():
        if word.lower() not in stopword:
            count += 1
    return count

################################################################################
def check_charset(title):
    cnt = 0
    template = 'a'
    for x in title:
        template = x;
        break
    char = template
    if(ord(char) >= 3584 and ord(char) <= 3711):
        return "Thai"
    if ((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >=97 and ord(char) <=122) or ord(char)==40 or ord(char) ==10 or ord(char)==32) or (ord(char) >= 45 and ord(char) <= 60):
        return "Eng"
    else:
        return "Other"

################################################################################
def Find_type_of_text(line_5):
    global text_html
    global text_plain
    global text_Not_itdentified
    global text_other
    cnt = 0
    new_word = ''
    index = 0
    for word in line_5.split():
        index+=1
        if index == 2:
            #print (word)
            for char in word:
                if char == ';':
                    break
                new_word += char

    if new_word == '' or new_word == 'Last-modified:':
        new_word = "Not_Identified"
    if new_word == "text/html":
        text_html += 1
        return "1"
    if new_word == "text/plain":
        text_plain += 1
        return "2"
    if new_word == "Not_Identified":
        text_Not_itdentified += 1
        return "3"
    else:
        text_other += 1
        return "-1"

################################################################################
def Find_content_length(line_6):
    cnt = 0
    new_word = ''
    index = 0
    for word in line_6.split():
        index+=1
        if index == 2:
            #print (word)
            for char in word:
                if char == ';':
                    break
                new_word += char


    try:
        content_length = (int(new_word))
    except ValueError:
        content_length = -1
    return (content_length)

################################################################################
def Find_URL_NB_Slash_LenURL(line_1):
    #print (INPUT_URL)
    URL = ''
    Nb_slash = 0
    before = ''
    for char in line_1:
        if char == '/':
            Nb_slash +=1
        if char  == ' ':
            break
#        if before == '/':
#            Nb_slash -=1
        URL += char
#        before = char

    Nb_slash = Nb_slash - 2

    cnt = 0
    check = False
    for char in URL:
        cnt+=1
        if cnt > len(URL) -6:
            if char == '.':
                check = True

    if Nb_slash >0 and check:
        Nb_slash -=1

    if URL[len(URL)-1] == "/":
        Nb_slash -= 1

    yield URL
    yield Nb_slash
    yield len(URL)- 7 - Nb_slash

################################################################################
def Find_Nb_Word_In_URL(URL):
    cnt =0
    Nb_spacial_char = 0
    for char in URL:
        cnt +=1
        if cnt > 7:
            if ((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >=97 and ord(char) <=122) or (ord(char) >= 3584 and ord(char) <= 3711) or (ord(char)>= 48 and ord(char) <= 57)):
                Nb_spacial_char +=0
            else:
                if (ord(char) == ord('%')):
                    Nb_spacial_char +=0
                else:
                    Nb_spacial_char +=1
    if (URL[len(URL)-1]) == '/':
        Nb_spacial_char -=1
    return Nb_spacial_char+1


################################-MAIN_LOOP_#####################################
cnt = 0
for name in files:
    with open(name) as f:
        cnt +=1
        print(name ,' ',cnt)

########-find_main_attribute
        line_1 = ''
        line_2 = ''
        line_3 = ''
        line_4 = ''
        line_5 = ''
        line_6 = ''
        html_content = ''
        index = 0
        for line in f:
            index += 1
            if index == 1:
                line_1 = line
            if index == 2:
                line_2 = line
            if index == 3:
                line_3 = line
            if index == 4:
                line_4 = line
            if index == 5:
                line_5 = line
            if index == 6:
                line_6 = line
            if index > 7:
                html_content += line
 ########-find_main_attribute


        #title = Find_title_def(html_content)
        URL =Find_URL(line_1)
        Nb_word_in_URL = Find_Nb_Word_In_URL(URL)

        print (URL)
        print (Nb_word_in_URL)
        #title = title.strip()
        #URL, Nb_slash, len_URL = Find_URL_NB_Slash_LenURL(line_1)
        #link, table , picture = Find_Nb_link_pic_table(html_content)
        #site = Find_site(line_1)
        #print ("Nb_link : ",link)
        #print ("Nb_table",table)
        #print ("Nb_picture",picture)

        #binary_domain = Find_binary_domain(URL)
        #print (binary_domain)
        #print (URL)
        #print (Nb_slash)
        #print (len_URL)
        #text_type = Find_type_of_text(line_5)
        #print ("text_type : ",text_type)
        #content_length = Find_content_length(line_6)
        #print ("content_length : ",content_length)
        #content = Find_content(html_content)
        #count_title, count_content = Wordcount(content, title, check_charset(title))
        #print (title, " : ", count_title)
        #print ("content", " : ", count_content)
        #print ("Numer_of_webpage_in_the_same_site : ", dict_site[site])
        print ("Number_of_word_in_URL : ")
        print ("\n")

################################################################################
print ("SUMARY")
print ("- HAVE_TITLE : " , HAVE_TITLE)
print ("- NO_TITLE   : ", NO_TITLE)
print ("TH : ", TH)
print ("ENG : ", ENG)
print ("OTHER LANGUAGE : ", OTHER)
print ("NO_CONTENT : ", NO_CONTENT)
print ("\nType_text")
print ("text/html : ", text_html)
print ("text/plain: ", text_plain)
print ("text/Not_Identified : ", text_Not_itdentified)
print ("text/other : ", text_other)
print("EXECUTE TIME  --- %s seconds ---" % (time.time() - start_time))
