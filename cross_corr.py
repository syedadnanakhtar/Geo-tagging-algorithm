# Cross correlation function- this function inputs two lists, cam message time list containing gps seconds and the image time
# list containing the time of the images. this function returns the shift that maximises the time difference cross correlation
#if output is -6, that means 6 cam messages need to be shifted up.



def cross_correlation(cam_time):
    cam_length=len(cam_time)
    cam_time_diff = [0]
    for i in range(1, cam_length - 1):
        d=(cam_time[i] - cam_time[i - 1])/1000.0
        cam_time_diff.append(d)
        i = i + 1
    print "Camera time difference array is \n",cam_time_diff

    # image_length=len(image_time)
    # image_time_diff=[0]
    # i=1
    # for i in range(0,image_length-1):
    #     image_time_diff.append(image_time[i]-image_time[i-1])
    #     i=i+1
    # print '\n'
    # print image_time_diff


