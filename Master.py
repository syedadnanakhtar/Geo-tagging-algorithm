import os
import piexif
from astropy.time import Time
from datetime import datetime, timedelta
import csv


# input image folder path outputs a csv with image name and date time. also returns list of image times in gps seconds
def image_csv(path):
    file_list = list_files(path)
    image_times=[]  # list to store the time of images (GPS time)
    os.chdir(path)
    image_obj = open("image.csv", 'w')
    for i in range(0, len(file_list)):
        if file_list[i][(file_list[i].index('.') + 1):] == "JPG":
            exif_dict = piexif.load(file_list[i])
            image_obj.write(file_list[i] + "," + exif_dict['Exif'][36867] +"," +str(get_gps_time(exif_dict['Exif'][36867])['seconds'])+"\n")
            image_times.append(get_gps_time(exif_dict['Exif'][36867])['seconds'])
        i = i + 1
    image_obj.close()
    return image_times

# accepts path as a string and returns all list of files
def list_files(path):
    file_list = os.listdir(path)
    return file_list

# accepts GMT +5:30 time and returns gps week no, gps seconds as a dictionary. Format is YYYY:MM:DD HH:MM:SS
def get_gps_time(t_gmt):
    #t_gmt = '2017:01:25 12:48:07'  # Time in GMT +5:30
    mytime = datetime.strptime(t_gmt, "%Y:%m:%d %H:%M:%S")
    mytime -= timedelta(minutes=330)
    t_utc = mytime.strftime("%Y-%m-%dT%H:%M:%S")  # Time in UTC
    t_gps = Time(t_utc, format='isot', scale='utc')
    t_gps.format = 'gps'
    print t_gps.gps
    week = t_gps.gps // 604800
    sec =int(t_gps.gps % 604800)
    gps_time = {'week': week, 'seconds': sec}
    # print 'UTC time is ', t_utc
    # print 'reading of the GPS is ', t_gps
    # print 'the week number is ', gps_time['week']
    #print 'the number of week and sec is', gps_time
    return gps_time

# accepts bin file name and outputs a cam.csv file. Also returns list of times of cam messages
def cam_csv( file_name ):
    cam_obj=open("cam.csv", 'w')
    cam_times=[]
    myFile = open(file_name)
    for line in myFile:
        if 'CAM' in line:
            if 'PARM' in line or 'FMT' in line:
                {}
            else:
                cam_obj.write(line)
                k=[pos for pos, char in enumerate(line) if char == ',']
                t=line[k[1]+2:k[2]]
                cam_times.append(int(t))
    cam_obj.close()
    myFile.close()
    #print cam_times
    #cross_corr.cross_correlation(cam_times)
    return cam_times

# accepts bin file name and outputs a pos.csv file
def pos_csv( file_name ):
    pos_obj=open("pos.csv", 'w')
    myFile = open(file_name)
    for line in myFile:
        if 'POS' in line:
            if 'PARM' in line or 'FMT' in line:
                {}
            else:
                pos_obj.write(line)
    pos_obj.close()
    myFile.close()

# function to convert gps time to pixhawk time in microseconds. it accepts an argument 'gps_ms' which is gps time in milli-seconds and
# returns pixhawk time in micro seconds
def gps_to_pixhawk_time(gps_ms):
    cam_obj=open("cam.csv",'r')
    csv_obj = csv.reader(cam_obj, delimiter=',')
    str=csv_obj.next()
    t_ph=int(str[1]) # time pixhawk microseconds
    t_gps=int(str[2])
    offset=t_ph-t_gps*1000 # offset in micro seconds
    t_ph = gps_ms*1000 + offset
    cam_obj.close()
    return t_ph


# accepts photo time in pixhawk time (us) and returns nearest match of
# position available as a list (lat, long, alt, rel alt)
def get_pos(t_ph):
    delay_ms=230
    t_ph=t_ph+delay_ms*1000
    pos_obj=open("pos.csv",'r')
    csv_obj=csv.reader(pos_obj,delimiter=',')
    offset=1000000 #offset is initialised to 1 second
    for row in csv_obj:
        t=int(row[1])
        if (abs(t-t_ph) < offset):
            offset=abs(t-t_ph)
            location=row[2:]
    return location


def main():
    path_images = r"D:\NAS\Tata-Mines\F1\flight-2\Geotagged-Images" #path where images are stored
    path_log=r"D:\NAS\Tata-Mines\F1\flight-2"                       #path where log is stored
    log_name = "45.log"                                             #name of the log file

    # write image date and time in a csv file. Store the image GPS time in a 'image_time_list'
    image_time_list=image_csv(path_images)                          #list that contains all image GPS time

    os.chdir(path_log)
    cam_time_list=cam_csv(log_name)
    pos_csv(log_name)
    


main()