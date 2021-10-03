import datetime
import os
import requests

from Config import SENDER, RCPT, DEBUG, BOT_TOKEN, RCPT_USER_ID


def send_telegram_msg(msg, rcpt_user_id=RCPT_USER_ID, bot_token=BOT_TOKEN):
    
    # fix special characters
    # Error: Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 30
    msg = msg.replace('_', '-')
    msg = msg.replace('*', '0')

    api_call = f'https://api.telegram.org/bot{bot_token}' + \
               f'/sendMessage?chat_id={rcpt_user_id}' + \
               f'&parse_mode=Markdown&text={msg}'

    r = requests.get(api_call)
    if r.status_code != 200:
        print('Telegram API returned: ', r.status_code)
        print(r.text)
    return r


def send_signal_msg(msg, sender=SENDER, rcpt=RCPT, debug=DEBUG):
    syscall = f'signal-cli -u {sender} send -m \"{msg}\" {rcpt}'
    print(syscall)
    if not debug:  
        os.system(syscall)


def seconds_until(year, month, day, hour):
    t = datetime.datetime(year, month, day, hour)
    tnow = datetime.datetime.today()
    return max(1, int((t - tnow).total_seconds()))


def calc_delay(delay, start_from=7, end_at=22):
    t = datetime.datetime.today()
    tnext = t + datetime.timedelta(days=1)
    if t.hour >= end_at:
        return seconds_until(tnext.year, tnext.month, tnext.day, start_from)
    elif t.hour < start_from:
        return seconds_until(t.year, t.month, t.day, start_from)
    else:
        return delay


if __name__ == '__main__':
    #dt = datetime.datetime.today()
    #print(dt)
    #print(seconds_until(2021, 5, 18, 7))
    #print(calc_delay(42, start_from=5, end_at=7))
    #send_telegram_msg('Foobar was here!')
    send_telegram_msg('Are you _listening_ ? ***')

