import os
import cross_corr

def cam_csv( file_name ): #accepts bin file name and outputs a cam.csv file. Also returns list of times of cam messages
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
    print cam_times
    cross_corr.cross_correlation(cam_times)
    #return cam_times

def pos_csv( file_name ): #accepts bin file name and outputs a pos.csv file
    pos_obj=open("pos.csv", 'w')
    myFile = open(file_name)
    for line in myFile:
        if 'POS' in line:
            if 'PARM' in line:
                {}
            else:
                pos_obj.write(line)
    pos_obj.close()
    myFile.close()

def main():
    #path = raw_input("Please input the path where the .BIN file is present.\n")
    path=r"D:\NAS\Tata-Mines\F1\flight-2"
    #f_name=raw_input("Please input the file name.")
    f_name="45.log"
    os.chdir(path)
    cam_csv(f_name)
    pos_csv(f_name)

main()