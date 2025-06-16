
from bs4 import BeautifulSoup
import requests
import random 
from random import randint
import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.edge.options import Options 
import csv
import pandas as pd

 
my_user_agent =["Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0", 
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0", 
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0", 
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0", 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0', 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'] 
 
 
edge_options = Options() 
edge_options.add_argument(f"--user-agent={my_user_agent[random.randint(0,17)]}") 
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(options=edge_options) 
page = driver.get("https://auto.drom.ru/all") 
time.sleep(random.randint(1,10)) 
headers=my_user_agent 
# soup = BeautifulSoup(driver.page_source, 'html.parser')

def try_catch(item,tag,clas): #проверка нахождения элементов на странице
    try:
        param=item.find(tag, class_=clas)
    except:
        param=-1
    return param



cars=[]
def get_pages_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('a',class_='_1j1e08n0')
	if pagination:                                       # закомменчено для парсинга только 1 страницы
		return int(pagination[-2].get_text())
	else:
		return 1


def gen(url):
    # 0 - 2 999 999
    for cost in range(0, 60):
        for dist in range(0, 100):
            yield url+'?minprice=%d&maxprice=%d&minprobeg=%d&maxprobeg=%d' % (
                cost * 50_000, (cost + 1) * 50_000 - 1, dist * 10_000, (dist + 1) * 10_000 - 1)
    # 3 000 000 - 5 999 999
    for cost in range(0, 30):
        yield url+'?minprice=%d&maxprice=%d' % (3_000_000 + cost * 100_000, 3_000_000 + (cost + 1) * 100_000 - 1)
    # over 6 000 000
    yield url+'?minprice=%d' % (6_000_000)


def get_content(arr):  
    for url in arr:
        date_p=full_name = comp=gen=trans = drv =b_t= clr=whl=mlg=city=price=name=model=year=power='NaN'
        driver.get(url) 
        soup = BeautifulSoup(driver.page_source, 'html.parser')   
        # try:   
        #     price=soup.find('div', class_='wb9m8q0').get_text()
        #     full_name =soup.find('h1', class_='css-1tjirrw e18vbajn0') # доп класс для заголовка с названием и годом, так как существует два таких класса
        #     name =full_name.find('span').get_text()
        # except :
        #     price='NaN'
        #     name='NaN'
        if(try_catch(soup,'div','wb9m8q0')!=-1 and try_catch(soup,'div','wb9m8q0')!=None):
            price=try_catch(soup,'div','wb9m8q0').get_text() 
        
        if(try_catch(soup,'h1','css-1tjirrw e18vbajn0')!=-1 and try_catch(soup,'h1','css-1tjirrw e18vbajn0')!=None):
            full_name=try_catch(soup,'h1','css-1tjirrw e18vbajn0')
            name =full_name.find('span').get_text()
       
        # город
        locations = soup.find_all('div', class_='css-inmjwf e162wx9x0')
        for location in locations:
            if ('Город' in location.find('span').get_text()):
                city = location.find(text=True, recursive=False).get_text()
            else:
                continue
        model = name[7:name.find(',')]
        year=name[name.find(',')+1:name.find('год')]
        items = soup.find_all('table',class_='css-xalqz7 eppj3wm0')
        for item in items:
            array = item.find_all('tr')
            for ar in array:
                if ar.find_all('th'):
                    if (ar.find('th').get_text()=='Коробка передач'):
                        trans=ar.find('td').get_text()
                    if (ar.find('th').get_text()=='Привод'):
                        drv=ar.find('td').get_text()
                    if (ar.find('th').get_text()=='Тип кузова'):
                        b_t=ar.find('td').get_text()
                    if (ar.find('th').get_text()=='Цвет'):
                        clr=ar.find('td').get_text()
                    if (ar.find('th').get_text()=='Руль'):
                        whl=ar.find('td').get_text()
                    if (ar.find('th').get_text()=='Поколение'):
                        gen=ar.find('td').get_text()
                    if (ar.find('th').get_text()=='Комплектация'):
                        comp=ar.find('td').get_text()
                else:
                    continue
            if(try_catch(item,'span','css-1jygg09 e162wx9x0')!=-1 and try_catch(item,'span','css-1jygg09 e162wx9x0')!=None):
                    engine=try_catch(item,'span','css-1jygg09 e162wx9x0').get_text()
            # engine=item.find('span',  class_='css-1jygg09 e162wx9x0').get_text()
            fuel=engine[:engine.find(',')+1]
            volume=engine[engine.find(',')+1:]
            # добавлено
            if item.find('span', class_='css-1osyw3j ei6iaw00'):
                mlg=item.find('span', class_='css-1osyw3j ei6iaw00').get_text()
            if(try_catch(item,'span','css-9g0qum e162wx9x0')!=-1 and try_catch(item,'span','css-9g0qum e162wx9x0')!=None):
                power=try_catch(item,'span','css-9g0qum e162wx9x0').get_text() 
            else:
                power='NaN'
            if(try_catch(soup,'div','css-pxeubi evnwjo70')!=-1 and try_catch(soup,'div','css-pxeubi evnwjo70')!=None):
                date_p=try_catch(soup,'div','css-pxeubi evnwjo70').get_text()
            else:
                date_p='NaN'
            # power= item.find('span', class_='css-9g0qum e162wx9x0').get_text()[:item.find(',')] # без налога но с вероятной ошибкой 'NoneType' object has no attribute 'get_text'
            # date_p =  soup.find('div', class_='css-pxeubi evnwjo70').get_text()
            cars.append({
            'model':model,
            'location': city,
            'year': year,
            'price':price[:price.find('₽')].replace('\xa0', ' ') if price!='NaN' else price,
            'fuel': fuel,
            'engine_volume':volume,
            'power':power[:power.find('л.')].replace('\xa0', ' ') if power!='NaN' else power,
            'transmission':trans,
            'drive':drv,
            'body_type':b_t,
            'color':clr,
            'milage':mlg[:mlg.find('к')].replace('\xa0', ' ') if mlg!='NaN' else mlg,
            'wheel':whl,
            'date_posted':date_p[date_p.find('от')+2:],
            'generation': gen,
            'complictation':comp,
            })
            # запись в файл каждого авто
        with open('drom.csv', "w") as csv_file:
            df = pd.DataFrame(cars)
            df.to_csv('drom.csv', index=False)
        
    return cars




def get_hrefs(html):
    hrefs=[]
    soup = BeautifulSoup(html, 'html.parser')
    links=soup.find_all('a',class_='g6gv8w4 g6gv8w8 _1ioeqy90')
    for link in links:
        hrefs.append(link.get('href'))
    return hrefs


url= 'https://auto.drom.ru/all'
# url = 'https://auto.drom.ru/all'  # Бyдем добавлять число в конец
# for i in range(1, get_pages_count(driver.page_source)+1):  # Сколько страниц столько и итераций цикла
#     r= driver.get(url + str(i))  # 
# arr = get_hrefs(driver.page_source)
    #для функции gen()
# start_urls = (link for link in gen(url))

for link in gen(url): 
    parsed_url = link.rsplit("all") #разбивка url по all
    new_url = "all/page/".join(parsed_url) #добавляем page и сразу 1, чтобы считал кол-во страниц по фильтрам правильно 
    driver.get(new_url.replace('page','page1'))
    for i in range(1, get_pages_count(driver.page_source)+1):  # Сколько страниц столько и итераций цикла
        # new = new_url.replace('page','page'+str(i))
        # driver.get(link + str(i)) 
        driver.get(new_url.replace('page','page'+str(i))) 
        arr = get_hrefs(driver.page_source)
        itog = get_content(arr)

 






