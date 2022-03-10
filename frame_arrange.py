import glob
import os
import pandas as pd
import math
from sys import exit
from exif import Image
import time

path = r"D:\Movies\IMG6"

os.chdir(path)
my_files = glob.glob('*.jpg')
print(my_files)
tsp = []
for i in range(0, len(my_files)):
    join = path + '\\' + my_files[i]
    with open(join, 'rb') as img_file:
        img = Image(img_file)
        index = img.list_all().index('datetime_digitized')

        time_list = img.get(img.list_all()[index]).split(" ")
        time_tsp = ' '.join(time_list)
        tsp.append(time.mktime(time.strptime(time_tsp, "%Y:%m:%d %H:%M:%S")))

dict = {'file': my_files, 'timestamp': tsp}
df = pd.DataFrame(dict)
df = df.sort_values(by=['timestamp'])

folder_iterations = math.ceil(len(df) / 12)
start = 0
for i in range(0, folder_iterations):

    fold_path = path + '\\' + 'Frame ' + str(i + 1)
    os.makedirs(fold_path)

    while start < (i + 1) * 12:

        try:
            sorted_file_path = path + '\\' + df.iloc[start][0]
        except:
            exit()

        with open(sorted_file_path, 'rb') as img_file:
            img = Image(img_file)

        index = img.list_all().index('exposure_time')
        exp_time = str(round(float(img.get(img.list_all()[index])), 3))

        new_file_path = fold_path + '\\' + 'Frame ' + str(i + 1) + ' Shutter Value ' + str(exp_time) + '.jpg'
        os.rename(sorted_file_path, new_file_path)

        file_name = df.iloc[start][0][:-4]
        cr2_file = path + '\\' + file_name + '.CR2'
        new_cr2_file_path = fold_path + '\\' + 'Frame ' + str(i + 1) + ' Shutter Value ' + str(exp_time) + '.CR2'
        os.rename(cr2_file, new_cr2_file_path)

        start = start + 1

    if start == len(df):
        print("break")
        break
