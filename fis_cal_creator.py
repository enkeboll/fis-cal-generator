import datetime
from operator import attrgetter

from ics import Calendar, Event

BREAK_BEGIN = datetime.date(2019, 12, 23)

def runs_over_break(start_date):
    if (BREAK_BEGIN > start_date and
        BREAK_BEGIN < start_date + datetime.timedelta(weeks=15, days=5)):
        return True
    return False


def create_cal(filename, start_date):
    with open(filename, 'r') as f:
        c = Calendar(f.read())
    sorted_events = sorted(filter(lambda e: e.all_day, c.events),
                           key=attrgetter('_begin'))
    day_diff = (start_date - sorted_events[0].begin.date()).days

    needs_offset = runs_over_break(start_date)
    for e in sorted_events:
        e.end = e.end.shift(days=day_diff - 1)
        e.begin = e.begin.shift(days=day_diff)
        if needs_offset:
            if e.begin.date() >= BREAK_BEGIN:
                e.end = e.end.shift(weeks=1)
                e.begin = e.begin.shift(weeks=1)
        e.make_all_day()
        e.alarms = []

    c.events = set(sorted_events)
    return c


if __name__ == '__main__':
    filename = '/Users/enkeboll/Downloads/DC-DS-082619_flatironschool.com_7f8u2ulitiktbjns0nnja9d8hg@group.calendar.google.com.ics'
    start_date = datetime.date(2019, 11, 18)
    new_cal = create_cal(filename, start_date)

    with open('/Users/enkeboll/Downloads/newcal.ics', 'w') as f:
        f.write(str(new_cal))