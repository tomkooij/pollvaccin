# coding: utf-8
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import datetime
import random
import zlib

from requests.models import HTTPError

from tools import calc_delay, send_telegram_msg

url = "https://www.wndconferentie.nl/conferentie-2021/inschrijving/"
sleep_delay = 300   # poll every xx seconds


def send_msg(msg):
    msg = msg.replace('_', '-')
    print('Sending telegram msg: ', msg)
    send_telegram_msg(f'{time.ctime()}: {msg}')

def poll_site():
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print (e.response.text)
        time.sleep(10)  # sleep to prevent hammering site
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def notify():
    for _ in range(2):
        send_msg('WND PAGE CHANGED!!! Schrijf je in!')
        time.sleep(5)


def main():
    last_hash = 4178438849
    last_n_urls = 45
    print('Start...')
    send_msg(f'poll_wnd started: polling every {sleep_delay} seconds.')
    while True:

        if random.randint(1, 50) == 42:
            # heartbeat
            send_msg('boem boem ... boem boem')
                
        soup = poll_site()
        if soup:
            hash = zlib.crc32(bytes(soup.text, 'utf8'))
            if hash != last_hash:
                last_hash = hash
                notify()
                continue
            n_urls = len(soup.findAll('a'))
            if n_urls != last_n_urls:
                last_n_urls = n_urls
                notify()
                continue
            print(f'{time.ctime()} No changes:  {last_hash} {last_n_urls}')
        else:
            send_msg('Error in scraping page...')
        delay = calc_delay(sleep_delay)
        time.sleep(delay)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('KeyboardInterrupt!')
    except Exception as e:
        send_msg('Pollwnd stopped!')
        print(str(e))
