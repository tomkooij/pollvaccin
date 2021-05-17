#
# Poll de GGD website "coronatest" om te kijken of ik al een afspraak kan maken
#
import requests
import time
import os
from requests.models import HTTPError

from Config import SENDER, RCPT
from delay import calc_delay   

def send_signal_msg(msg, sender=SENDER, rcpt=RCPT, debug=True):
    syscall = f'signal-cli -u {sender} send -m \"{msg}\" {rcpt}'
    if debug:
        print(syscall)
    #os.system(syscall)


def is_geboortejaar_aan_de_beurt(jaar):
    url = 'https://user-api.coronatest.nl/vaccinatie/programma/bepaalbaar/{geboortejaar}/NEE/NEE'

    try:
        r = requests.get(url.format(geboortejaar=str(jaar)))
        r.raise_for_status()
    except HTTPError as e:
        print(e)
        return None

    result = r.json()
    return result['success']


for geboortejaar in range(1961, 1980):
    print('We wachten op: ', geboortejaar)
    if os.path.exists(str(geboortejaar)):
        print('Dit jaar is al ontdekt. Skipping...')
        continue

    while True:
        print(time.ctime()+' *** ', end='')
        r = is_geboortejaar_aan_de_beurt(geboortejaar)
        if r is None:
            print('Network error, nog een keertje')
            time.sleep(60)
            continue
        if not r:
            print(f'{geboortejaar} is nog niet aan de beurt')
            delay = calc_delay(300)  # slaap 's nachts.
            print(f'Sleeping {delay} seconds.')
            time.sleep(delay)
            continue 
        print(f'{geboortejaar} is NU AAN DE BEURT!!!!')
        send_signal_msg(f'{time.ctime()} Jaargang {geboortejaar} kan nu een afspraak maken!')
        if geboortejaar == 1975:
            for delay in range(1, 10):
                # ALERT ALERT!
                send_signal_msg(f'{time.ctime()} {geboortejaar} is aan de beurt. MAAK NU EEN VACCINATIE AFSPRAAK!!')
                time.sleep(10*delay)
        with open(str(geboortejaar), 'a') as f:
            f.write(time.ctime())  # write flag
        break
