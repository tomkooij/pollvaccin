# coding: utf-8
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import datetime
import random
from requests.models import HTTPError

from delay import calc_delay
from Config import SENDER, RCPT, DEBUG


url = "https://www.prullenbakvaccin.nl/"


def send_signal_msg(msg, sender=SENDER, rcpt=RCPT, debug=DEBUG):
    syscall = f'signal-cli -u {sender} send -m \"{msg}\" {rcpt}'
    print(syscall)
    if not debug:  
        os.system(syscall)


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
    Locatie #95   Heeft geen vaccins
    
    return id 
    """
    m = re.match(r".*#(\d+)", s)
    if m:
        return int(m.groups()[0])
    return -999


def main():
    priklocatie_status = {}
    last_msg = '' 

    print('Start...')
    while True:

        if random.randint(1, 250) == 42:
            # heartbeat
            send_signal_msg(time.ctime()+'We volgen %d priklocaties in de buurt...' % len(priklocatie_status))
                
        soup = poll_site("gouda")
        if soup:
            
            priklocaties = soup.find_all("div", {"class": "card-body"})

            for priklocatie in priklocaties:
                # verwijder <span style='display:none'>scrapen heeft geen zin</span>
                for decoy in priklocatie.find_all('span', style="display:none"):
                    decoy.decompose()
                priklocatie = priklocatie.text.replace('\n', ' ')
                priklocatie = priklocatie.replace('Gegevens pas beschikbaar tijdens prikmoment.', '')

                id = parse_priklocatie(priklocatie)
                hash = priklocatie.replace(' ', '')[:20]
                
                if id == -999: # geen locatie id, dus hoogstwaarschijnlijk vaccin
                    if last_msg == hash:
                        print('Bericht al gestuurd...')
                        continue
                    last_msg = hash
            
                status = priklocatie_status.get(id, None)
                if status is None:
                    print('Nieuwe locatie', id)
                    send_signal_msg('Nieuwe locatie: '+priklocatie)
                elif status == hash:
                    continue
                priklocatie_status[id] = hash 
                print('Locatie status is veranderd!', id, priklocatie)
                send_signal_msg(time.ctime()+priklocatie)

            print('We volgen %d priklocaties in de buurt...' % len(priklocatie_status))
            print(priklocatie_status)    
            delay = calc_delay(60)
            time.sleep(delay)


if __name__=='__main__':
    try:
        main()
    except Exception as e:
        send_signal_msg('Pollvaccin stopped!')

