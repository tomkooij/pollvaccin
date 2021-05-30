#
# Poll de GGD website "coronatest" om te kijken of ik al een afspraak kan maken
#
import requests
import time
import os
from requests.models import HTTPError

from tools import calc_delay, send_signal_msg, send_telegram_msg


def send_msg(msg):
    send_telegram_msg(f'{time.ctime()}: {msg}')


def get_semaphore_fn(geboortejaar):
    return 'cohorten/' + str(geboortejaar)


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


def main():
    for geboortejaar in range(1961, 1980):
        print('We wachten op: ', geboortejaar)
        if os.path.exists(get_semaphore_fn(geboortejaar)):
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
            send_msg(f'Jaargang {geboortejaar} kan nu een afspraak maken!')
            
            with open(get_semaphore_fn(geboortejaar), 'a') as f:
                f.write(time.ctime())  # write flag
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('KeyboardInterrupt!')
    except Exception as e:
        send_msg('Pollggd stopped!')
        print(str(e))
