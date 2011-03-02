from datetime import date, timedelta
#from time import strptime

def weekBoundaries(year, week):
    """http://bytes.com/topic/python/answers/499819-getting-start-end-dates-given-week-number"""
    startOfYear = date(year, 1, 1)
    now = startOfYear + timedelta(weeks=week)
    # isoweekday() % 7 returns Sun=0 ... Sat=6
    sun = now - timedelta(days=now.isoweekday() % 7)
    sat = sun + timedelta(days=6)
    #if DEBUG:
    #    print "DEBUG: now = %s/%s" % (now, now.strftime("%a"))
    #    print "DEBUG: sun = %s/%s" % (sun, sun.strftime("%a"))
    #    print "DEBUG: sat = %s/%s" % (sat, sat.strftime("%a"))
    return sun, sat
