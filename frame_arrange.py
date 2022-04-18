import glob
import os
import pandas as pd
import math
from sys import exit
from exif import Image
import time
import platform

path = r"C:\Users\tedlasai\OneDrive - York University\School\York\Lab\ExposureData\FlashingLight"

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

stackSize = 28

folder_iterations = math.ceil(len(df) / stackSize)
start = 0
for i in range(0, folder_iterations):

    frameNum = "{:0>2d}".format(i+1)

    while start < (i + 1) * stackSize:

        try:
            sorted_file_path = path + joinPathChar + df.iloc[start][0]
        except:
            exit()

        with open(sorted_file_path, 'rb') as img_file:
            img = Image(img_file)

        index = img.list_all().index('exposure_time')
        exp_time = round(float(img.get(img.list_all()[index])), 5)

        exp_time = "{:08.5f}".format(exp_time)

        new_file_path = path + joinPathChar + 'Frame_' + frameNum + '_Shutter_Value_' + str(exp_time) + '.jpg'
        os.rename(sorted_file_path, new_file_path)

        file_name = df.iloc[start][0][:-4]
        cr2_file = path + joinPathChar + file_name + '.CR2'
        new_cr2_file_path = path + joinPathChar + 'Frame_' + frameNum + '_Shutter_Value_' + str(exp_time) + '.CR2'
        os.rename(cr2_file, new_cr2_file_path)

        start = start + 1

    if start == len(df):
        print("break")
        break
