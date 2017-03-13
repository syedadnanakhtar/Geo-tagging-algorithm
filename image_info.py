import os
import piexif
import time_date

def image_csv(path):#input image folder path outputs a csv with image name and date time. also returns list of image times
    file_list = list_files(path)
    image_times=[]
    os.chdir(path)
    image_obj = open("image.csv", 'w')
    for i in range(0, len(file_list)):
        if file_list[i][(file_list[i].index('.') + 1):] == "JPG":
            exif_dict = piexif.load(file_list[i])
            image_obj.write(file_list[i] + "," + exif_dict['Exif'][36867] +"," +str(time_date.get_gps_time(exif_dict['Exif'][36867])['seconds'])+"\n")
            image_times.append(time_date.get_gps_time(exif_dict['Exif'][36867])['seconds'])
        i = i + 1
    image_obj.close()
    return image_times


def list_files(path):  # accepts path as a string and returns all list of files
    file_list = os.listdir(path)
    return file_list

def main():
    path = r"D:\NAS\Tata-Mines\F1\flight-2\Geotagged-Images"
    print image_csv(path)

main()