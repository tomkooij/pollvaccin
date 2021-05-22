import datetime
import os

from Config import SENDER, RCPT, DEBUG


def send_signal_msg(msg, sender=SENDER, rcpt=RCPT, debug=DEBUG):
    syscall = f'signal-cli -u {sender} send -m \"{msg}\" {rcpt}'
    print(syscall)
    if not debug:  
        os.system(syscall)


def seconds_until(year, month, day, hour):
    t = datetime.datetime(year, month, day, hour)
    tnow = datetime.datetime.today()
    print(f'{tnow} until ')
    return int((t - tnow).total_seconds())


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
    dt = datetime.datetime.today()
    print(dt)
    print(seconds_until(2021, 5, 18, 7))
    print(calc_delay(42, start_from=5, end_at=7))
