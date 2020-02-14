from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup
import re
import codecs

pageUrl = 'https://djinni.co/developers/?title=Scala' + '&page='

uClient = uReq(pageUrl)
pageHtml = uClient.read()
uClient.close()
pageSoup = soup(pageHtml, 'html.parser')


def page_numbers(Url):
    '''Get total number of pages in direction. For example if in the directions are 123 profiles - total number of pages will 123/10+1=13'''
    pageSoup = soup(pageHtml, 'html.parser')
    numb=(pageSoup.find('div',{'class':'page-header'}).text)
    page_num=''

    for word in numb:
        if word.isdigit():
           page_num+=word
          
#    if int(page_num) % 10 !=0:
#        number_of_pages = int(page_num) // 10 + 1
#    else: 
#        number_of_pages = int(page_num) // 10
    
    return (int(page_num))


def get_profile_id(Start_url, profiles_num):
    '''Greate a list of profile id. For example https://djinni.co/q/1111xxxx11111/ id is '1111xxxx11111/' '''
    page_urls = [] 
    prof_url = []
    id_set=set()
    
    for i in range(1, profiles_num):
        Url=''        
        Url=pageUrl+str(i)
        pageSoup = soup(uReq(Url), 'html.parser')       
    
        for link in pageSoup.find_all('a'):
            page_urls.append(link.get('href'))
       
        
        for elem in page_urls: 
            if '/q/' in elem:
                prof_url.append(elem[3::])
            
        id_set = set(prof_url)
        id = list(id_set)
    return (id)
#
def profile_title (profile_id): 
    '''Get title from persons profile'''
    profileUrl = 'https://djinni.co/q/'+profile_id
    uClient = uReq(profileUrl)
    pageHtml = uClient.read()
    uClient.close()

    pageSoup = soup(pageHtml, 'html.parser')
    
    title = str(pageSoup.title)
    cv_title=[]
    title = title.split()
    title.pop(0)
    for _ in range ((len(title)-1), 0, -1): 
        if title[_]!='|': 
            title[_]=''
        else: 
            break
    for elem in title: 
        if len(elem)>0:
            cv_title.append(elem)
    cv_title.pop(-1)
    title_str=''.join(str(elem)+' ' for elem in cv_title)
    return (title_str) 


def location(profile_id): 
    '''Get location from persons profile'''
    profileUrl = 'https://djinni.co/q/'+profile_id
    uClient = uReq(profileUrl)
    pageHtml = uClient.read()
    uClient.close()
        
    pageSoup = soup(pageHtml, 'html.parser')
        
    location=(pageSoup.find('div',{'class':'main-profile-details'}).text)
    loc_t=''
    loc=''
    for _ in range (0, len(location)-1):
        if location[_]!='$':
            loc_t+=location[_]
        else: 
            break
       
    loc=re.sub('^\s+|\n|\r|\s|\t+$', '', loc_t)
        
    return (loc[0:len(loc)-1])

def salary(profile_id):
    '''Get salary expectations in $ from persons profile'''
    profileUrl = 'https://djinni.co/q/'+profile_id
    uClient = uReq(profileUrl)
    pageHtml = uClient.read()
    uClient.close()
        
    pageSoup = soup(pageHtml, 'html.parser')
        
    salary = (pageSoup.find('span',{'class':'profile-details-salary'}).text)
    return (salary) 


def experience (profile_id): # nedd to grab and 1,5 yeras
    '''Get experience in years from persons profile'''
    profileUrl = 'https://djinni.co/q/'+profile_id
    uClient = uReq(profileUrl)
    pageHtml = uClient.read()
    uClient.close()
    exp_y=''
        
    pageSoup = soup(pageHtml, 'html.parser')
            
    exp = (pageSoup.find('div',{'class':'col-sm-8'}))
    sk_l = (str(exp).split())
    for elem in sk_l: 
        if elem.isdigit(): 
            #exp_y.join(elem)
            exp_y+=(elem)
            break
    return (exp_y)



def english_level (profile_id):
    '''Get English level provided in the persons profile'''
    profileUrl = 'https://djinni.co/q/'+profile_id
    uClient = uReq(profileUrl)
    pageHtml = uClient.read()
    uClient.close()
        
    pageSoup = soup(pageHtml, 'html.parser')
    eng=[]
    
    english = (pageSoup.find('div',{'class':'col-sm-8'}).text)
    eng = english.split()
    for _ in range (0, len(eng)): 
        if eng[_]=='Англійська':
            eng_level=eng[_+1]
    return (re.sub('^\s+|\n|\r|\s|\t+$', '', eng_level)) 


def skills (profile_id):
    '''Get skills list from profile'''
    profileUrl = 'https://djinni.co/q/'+profile_id
    uClient = uReq(profileUrl)
    pageHtml = uClient.read()
    uClient.close()
    pageSoup = soup(pageHtml, 'html.parser')
    skill_set =[]    
       
    skills = (pageSoup.find('div',{'class':'col-sm-8'}).text.split())
       
    for _ in range (0, len(skills)-1): 
        if skills[_]!= 'Навички': 
            skills[_]=''
        else: 
            break 
    
    if ('Досягнення') in skills: 
        for _ in range ((len(skills)-1), 0, -1): 
            if skills[_]!=('Досягнення'): 
                skills[_]=''
            else: 
                break
            
    if ('Перевірений') in skills: 
        for _ in range ((len(skills)-1), 0, -1): 
            if skills[_]!=('Перевірений'): 
                skills[_]=''
            else: 
                break  
    if ('Очікування') in skills: 
        for _ in range ((len(skills)-1), 0, -1): 
            if skills[_]!=('Очікування'): 
                skills[_]=''
            else: 
                break
    if ('Запропонувати') in skills: 
        for _ in range ((len(skills)-1), 0, -1): 
            if skills[_]!=('Запропонувати'): 
                skills[_]=''
            else: 
                break
        

    for elem in skills: 
        if len(elem)!=0: 
            skill_set.append(elem)
    skill_set.pop(0)
    skill_set.pop(-1)
    skill_set_str = ''.join(str(elem) for elem in skill_set)
    
    return (skill_set_str)
###
    




n = page_numbers(pageUrl)
print('Total number of profiles in direction is: ' +str(n))


profiles_id = get_profile_id(pageUrl, n) # id list
print('List of profile id for collect: ' + (str(profiles_id)))
print(len(profiles_id)) # check if all profiles are collected
#

out_filename = 'profile.txt'

headers = 'Title'+ '\t'  +'Location'+ '\t'  +'Salary'+ '\t'  +'Experience'+ '\t'+'English'+ '\t'  + 'Skills'+ '\n'
f = open(out_filename, 'w', encoding='utf-8') 
f.write(headers)


print('===============')
title=''
for elem in profiles_id:
    title = (profile_title(elem))
    print (title)
    print(type(title))
    
    loc = (location(elem))
    print (loc)
    print(type(loc))
    
    salary_exp = (salary(elem))
    print(salary_exp)
    print(type(salary_exp))
    
    exp_y = experience(elem)
    print(exp_y)
    print(type(exp_y))
    
    eng_level = english_level(elem)
    print(eng_level)
    print(type(eng_level))
    
    skill_set = skills (elem)
    print(skill_set)
    print(type(skill_set))
    print('*****************************')



    f.write( title + '\t'  + loc + '\t'  + salary_exp + '\t'  +exp_y+ '\t' + eng_level +'\t'+ skill_set + '\n')

f.close()  # Close the file
    

