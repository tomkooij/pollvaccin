import datetime


def seconds_until(year, month, day, hour):
    t = datetime.datetime(year, month, day, hour)
    tnow = datetime.datetime.today()
    print(f'{tnow} until ')
    return int((t - tnow).total_seconds())


def calc_delay(delay, start_from=7, end_at=22):
    t = datetime.datetime.today()
    tnext = t + datetime.timedelta(days=1)
    if t.hour >= end_at:
        return seconds_until(tnext.year, tnext.month, tnext.day, t.hour)
    elif t.hour < start_from:
        return seconds_until(t.year, t.month, t.day, start_from)
    else:
        return delay


if __name__ == '__main__':
    dt = datetime.datetime.today()
    print(dt)
    print(seconds_until(2021, 5, 18, 7))
    print(calc_delay(42, start_from=5, end_at=7))
