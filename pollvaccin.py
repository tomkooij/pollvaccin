# coding: utf-8
from bs4 import BeautifulSoup
import requests
import re
import time


url = "https://www.prullenbakvaccin.nl/"


def poll_site(location="gouda"):
    """poll site for location and return list of locations"""
    
    try:
        r = requests.get(url + location)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse_priklocatie(s):
    """
    Locatie #95 (17.99 km)   Heeft geen vaccins
    
    return id, dist (hele km)
    """
    m = re.match(r".*#(\d+).*\((\d+).\d+ km\)", s)
    if m:
        id, dist = map(int, m.groups())
    return id, dist


priklocatie_status = {}

#while True:
for _ in range(10):
    print('.', end='')

    soup = poll_site("gouda")
    if soup:
        priklocaties = soup.find_all("div", {"class": "card-body"})

        for priklocatie in priklocaties:
            priklocatie = priklocatie.text.replace('\n', ' ')
            id, dist = parse_priklocatie(priklocatie)
            if dist < 5:
                hash = priklocatie.replace(' ', '')
                status = priklocatie_status.get(id, None)
                if status is None:
                    print('Nieuwe locatie binnen fietsafstand.', id, dist)
                    print(priklocatie)
                elif status == hash:
                    continue
                priklocatie_status[id] = hash 
                print('Locatie status is veranderd!', id, priklocatie)
                    
    print('.', end='')
    time.sleep(5)



    
