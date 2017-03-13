from astropy.time import Time
import time
from datetime import datetime, timedelta

def main():
    print get_gps_time('2017:01:25 12:48:07' )

def get_gps_time(t_gmt): #accepts GMT +5:30 time and returns gps week no, gps seconds as a dictionary. Format is YYYY:MM:DD HH:MM:SS
    #t_gmt = '2017:01:25 12:48:07'  # Time in GMT +5:30
    mytime = datetime.strptime(t_gmt, "%Y:%m:%d %H:%M:%S")
    mytime -= timedelta(minutes=330)
    t_utc = mytime.strftime("%Y-%m-%dT%H:%M:%S")  # Time in UTC
    t_gps = Time(t_utc, format='isot', scale='utc')
    t_gps.format = 'gps'  #
    week = t_gps.gps // 604800
    sec = t_gps.gps % 604800
    gps_time = {'week': week, 'seconds': sec}
    # print 'UTC time is ', t_utc
    # print 'reading of the GPS is ', t_gps
    # print 'the week number is ', gps_time['week']
    # print 'the number of sec is', gps_time['seconds']
    return gps_time

main()