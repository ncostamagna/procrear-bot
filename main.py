from bs4 import BeautifulSoup
import requests
import subprocess
import time
import alertzy.req as alertzy
import numpy as np

value_sent = np.array([])
while True:
    base = "https://www.argentina.gob.ar"
    url = "{}/habitat/procrear/desarrollosurbanisticos".format(base)
    cabecera = {'User-Agent':'Firefox'}
    peticion = requests.get(url=url,headers=cabecera)
    soup = BeautifulSoup(peticion.text,'html5lib')
    word = 'INSCRIPCIÓN CERRADA'
    v = soup.find('div',{'id': 'listado-desarrollos'})

    alez = alertzy.New("zanov1i1fulmr56")
    
    for a in v.find_all('div', {'class':'col-sm-3'}):

        
        if a.find('strong').get_text() != word:   
            link = a.find('a')
            print(link['href'] in value_sent)
            
            if not link['href'] in value_sent:
                value_sent = np.append(value_sent, link['href'])
                print(value_sent)

                value = link['href'].split("/")
                value = value[len(value) - 1]

                alez.Send("Nuevo procrear",value.replace("-", " "), "procrear", link="{}{}".format(base, link['href']))
                break
    time.sleep(60*10)
