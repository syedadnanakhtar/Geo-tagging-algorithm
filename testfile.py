import csv
import os

def get_pos(t_ph):
    delay_ms = 250
    t_ph = t_ph + delay_ms * 1000
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
    path_log = r"D:\NAS\Tata-Mines\F1\flight-2"
    os.chdir(path_log)
    print get_pos(580305754)

main()