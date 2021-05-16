# coding: utf-8
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import datetime
from requests.models import HTTPError


from Config import SENDER, RCPT

url = "https://www.prullenbakvaccin.nl/"


def daytime():
    now = datetime.datetime.now()
    now_time = now.time()
    return now_time < datetime.time(20,00) and now_time >= datetime.time(7,00) 
    

def send_signal_msg(msg, sender=SENDER, rcpt=RCPT, debug=True):
    syscall = f'signal-cli -u {sender} send -m \"{msg}\" {rcpt}'
    if debug:
        print(syscall)
    #os.system(syscall)


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

print('Start...')
while True:

    if not daytime():
        print('geen vaccins in de nacht... morgen weer verder!')
        time.sleep(3600)
        continue

    soup = poll_site("gouda")
    if soup:
        priklocaties = soup.find_all("div", {"class": "card-body"})

        for priklocatie in priklocaties:
            priklocatie = priklocatie.text.replace('\n', ' ')
            priklocatie = priklocatie.replace('Gegevens pas beschikbaar tijdens prikmoment.', '')

            id, dist = parse_priklocatie(priklocatie)
            if dist < 5:
                hash = priklocatie.replace(' ', '')
                status = priklocatie_status.get(id, None)
                if status is None:
                    print('Nieuwe locatie binnen fietsafstand.', id, dist)
                    send_signal_msg('Nieuwe locatie: '+priklocatie)
                elif status == hash:
                    continue
                priklocatie_status[id] = hash 
                print('Locatie status is veranderd!', id, priklocatie)
                send_signal_msg(time.ctime()+priklocatie)

    print('We volgen %d priklocaties in de buurt...' % len(priklocatie_status))    
    time.sleep(300)



    
