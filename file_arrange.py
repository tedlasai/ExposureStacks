import glob
import os
import pandas as pd
import math
from sys import exit
from exif import Image
import time
import platform

path = r"C:\Users\tedlasai\OneDrive - York University\School\York\Lab\ExposureData\100EOS5D"

path = "F:\\DCIM\\101EOS5D"

# path = r"C:\Users\tedlasai\PycharmProjects\ExposureStacks\Exposures\Images_Scene_1_HML"

joinPathChar = "/"
if(platform.system() == "Windows"):
    joinPathChar = "\\"


os.chdir(path)
my_files = glob.glob('*.JPG') #i changed this to JPG for mac, it might need to be changed back to jpg for windows

print(my_files)
tsp = []
for i in range(0, len(my_files)):
    join = path + joinPathChar + my_files[i]
    with open(join, 'rb') as img_file:
        img = Image(img_file)
        index = img.list_all().index('datetime_digitized')

        time_list = img.get(img.list_all()[index]).split(" ")
        time_tsp = ' '.join(time_list)
        tsp.append(time.mktime(time.strptime(time_tsp, "%Y:%m:%d %H:%M:%S")))

dict = {'file': my_files, 'timestamp': tsp}
df = pd.DataFrame(dict)
df = df.sort_values(by=['timestamp'])

stackSize = 100


start = 0
for i in range(0, len(my_files)):

    frameNum = "{:0>4d}".format(i+1)
    try:
        sorted_file_path = path + joinPathChar + df.iloc[start][0]
    except:
        exit()


    new_file_path = path + joinPathChar + '1P0X' + frameNum + '.jpg'
    os.rename(sorted_file_path, new_file_path)

    file_name = df.iloc[start][0][:-4]
    cr2_file = path + joinPathChar + file_name + '.CR2'
    new_cr2_file_path = path + joinPathChar + '1P0X' + frameNum + '.CR2'
    os.rename(cr2_file, new_cr2_file_path)

    start = start + 1

    if start == len(df):
        print("break")
        break
