from bs4 import BeautifulSoup
import requests
import subprocess
import time
import alertzy.req as alertzy
import numpy as np
import pickle
from os.path import exists

db = np.array([])
sent = False

if exists('db.dat'):
    dbfile = open('db.dat', 'rb') 
    db = pickle.load(dbfile)
    dbfile.close()

print(db)

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
        print(link['href'] in db)
        
        if not link['href'] in db:
            sent = True
            db = np.append(db, link['href'])
            print(db)

            value = link['href'].split("/")
            value = value[len(value) - 1]

            alez.Send("Nuevo procrear",value.replace("-", " "), "procrear", link="{}{}".format(base, link['href']))


if sent:
    print(db)
    dbfile = open('db.dat', 'wb')
    pickle.dump(db, dbfile) 
    dbfile.close()
