#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


#takes one image file per iteration and feeds it to resize_and_gray, intensity_diff, difference_score 
#functions, returns ds_dict dictionary which contains file names and processed data from these files, 
#also return empty list duplicates needed in final_result function
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


# In[ ]:


#puts resize_and_gray and intensity_diff functions together. Returns 1-d array of ones and zeros.
def difference_score(image, height = 30, width = 30):
    row_res, col_res =  resize_and_gray(image, height, width)
    difference = intensity_diff(row_res, col_res)
    return difference


# In[ ]:


#calculates intensity difference, creating a boolean type array representing the 'footprint'
#of what was the image file before. Returns 1-d array of ones and zeros.
def intensity_diff(row_res, col_res):
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()


# In[ ]:


#opens image file, turns it to gray scale and flattens column-vise and row-vise, returns two 1-d arrays 
def resize_and_gray(image, height=30, width=30):
    a = np.average(Image.open(image), weights=[0.299, 0.587, 0.114], axis=2)
    a.resize(height, width)
    row_res = a.flatten()
    col_res = a.flatten('F')
    return row_res, col_res


# In[ ]:


#calculates the hamming distance between given pair of arrays, returns a float number from 0.0 to 1.0, 
#representing how similar these array are
def hamming_distance(image, image2):
    u_ne_v = image != image2
    return np.average(u_ne_v)


# In[32]:


#puts everything together and prints out the result
def final_result(image_files):
    duplicates, ds_dict =difference_score_dict(image_files)
    print(duplicates)
    n = 0
    for k1,k2 in itertools.combinations(ds_dict, 2):
        n+=1
        print(n, hamming_distance(ds_dict[k1], ds_dict[k2]))
        print(k1, k2)
        print(ds_dict[k1])
    #if hamming_distance(ds_dict[k1], ds_dict[k2])< .0482:
        if hamming_distance(ds_dict[k1], ds_dict[k2])< .333:
            duplicates.append((k1,k2))
    for i in duplicates:
        print(i[1],i[0])


# In[ ]:


#IMAGE_DIR = 'C:\\Users\\Max\\Downloads\\dev_dataset\\dev_dataset'
#bunch of if statements handling startup arguments
if len(sys.argv) == 1:
    print('error: the following arguments are required: --path')
    sys.exit()
elif sys.argv[1] == '--help' ot '-h':
    print('''optional arguments:
    -h, --help            show this help message and exit
    --path PATH           folder with images''')
    sys.exit()
else:
    IMAGE_DIR = sys.argv[1][2:]
    os.chdir(IMAGE_DIR)
    print(os.getcwd())
    image_files = os.listdir()
    print(len(image_files))
    final_result(image_files)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




