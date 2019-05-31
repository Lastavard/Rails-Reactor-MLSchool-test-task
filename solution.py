#!/usr/bin/env python
# coding: utf-8



# Based on https://github.com/moondra2017/Computer-Vision
# Key differences:
# - works on standard Python libraries, NumPy and Pillow
# - modified to meet the requirements of Rails Reactor MLSchool test task
# More information in documentation.ipynb
import numpy as np
from PIL import Image
import itertools
import os
import sys




#takes one image file per iteration and feeds it to resize_and_gray(), intensity_diff(), difference_score() 
#functions, returns ds_dict dictionary which contains file names and processed data from these files, 
#also return empty list duplicates needed in final_result() function
def difference_score_dict(image_list):
    ds_dict = {}
    duplicates = []
    for image in image_list:
        ds = difference_score(image)
        
        if image not in ds_dict:
            ds_dict[image] = ds
        else:
            duplicates.append((image, ds_dict[image]) )
    
    return  duplicates, ds_dict




#puts resize_and_gray and intensity_diff functions together. Returns 1-d array of ones and zeros.
def difference_score(image, height = 10, width = 15):
    row_res, col_res =  resize_and_gray(image, height, width)
    difference = intensity_diff(row_res, col_res)
    return difference




#calculates intensity difference, creating a boolean type array representing the 'footprint'
#of what was the image file before. Returns 1-d array of ones and zeros.
def intensity_diff(row_res, col_res):
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()




#opens image file, turns it to gray scale and flattens column-vise and row-vise, returns two 1-d arrays 
def resize_and_gray(image, height=10, width=15):
    a = np.average(Image.open(image).resize((height, width), resample = 2), weights=[0.299, 0.587, 0.114], axis=2)
    row_res = a.flatten()
    col_res = a.flatten('F')
    return row_res, col_res



#calculates the hamming distance between given pair of arrays, returns a float number from 0.0 to 1.0, 
#representing how similar these array are
def hamming_distance(image, image2):
    u_ne_v = image != image2
    return np.average(u_ne_v)



#puts everything together and prints out the result
def final_result(image_files):
    duplicates, ds_dict = difference_score_dict(image_files)
    for k1,k2 in itertools.combinations(ds_dict, 2):
        if hamming_distance(ds_dict[k1], ds_dict[k2])< .28:
            duplicates.append((k1,k2))
    for i in duplicates:
        print(i[1],i[0])



#bunch of if statements handling startup arguments
if len(sys.argv) == 1:
    print('usage: solution.py [-h] --path PATH')
    print('error: the following arguments are required: --path')
    sys.exit()
elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print('''usage: solution.py [-h] --path PATH

First test task on images similarity.

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           folder with images

''')
    sys.exit()
elif '--path' in sys.argv:
    try:
        if os.path.exists(sys.argv[sys.argv.index('--path') + 1]):
            IMAGE_DIR = sys.argv[sys.argv.index('--path') + 1]
            os.chdir(IMAGE_DIR)
            image_files = os.listdir()
            if os.listdir():
                final_result(image_files)
            else:
                print('No files in the folder')
                sys.exit()
        else:
            print('Folder does not exist')
    except IndexError:
        print('usage: solution.py [-h] --path PATH')
        print('error: the following arguments are required: --path')
        
else:
    print('usage: solution.py [-h] --path PATH')
    print('error: the following arguments are required: --path')