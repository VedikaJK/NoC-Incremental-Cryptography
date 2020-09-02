import skimage.io
from PIL import Image
import numpy as np
from Crypto.Hash import MD5
import hashlib 
import DES
  
def read_image_convert_to_1D_pixel_array(file_name):
    ## THIS FUNCTION RETURNS ARRAY OF THE FORM [0 128 128 155 0 128 50 10 120 .. ] I.E. LENGTH = PIXELS * 3
    a = skimage.io.imread(fname=file_name) # read image
    a=a.flatten(order='C') #flattened pixel array
    return a

def int_array_to_binary(arr):
    binary_arr = []
    for i in range(len(arr)):
        binary_arr.append(bin(int(arr[i]))[2:].zfill(8))
    return binary_arr

def binary_pixels_to_blocks(pixels_bin):
    # 64 BIT BLOCKS
    t=''
    D=[]
    for i in range(len(pixels_bin)):
        if(i%8==0):
            t = pixels_bin[i]
        else:
            t+=pixels_bin[i]
            if((i+1)%8==0):
                D.append(t)
            elif(i==len(pixels_bin)-1):
                D.append(t)
    ### if len(D[len(D)-1])<64 then ... padding
    ### INCOMPLETE
    return D

def image_to_blocks(file_name):
    arr1 = read_image_convert_to_1D_pixel_array(file_name)
    arr2 = int_array_to_binary(arr1)
    D = binary_pixels_to_blocks(arr2)
    return D

def convert_array_to_image(arr_1D,name_for_image, h,w):
    data = np.zeros((h, w, 3), dtype=np.uint8)
    #code to conert 1D array to 3d array for image
    # data[i,j] = [x,y,z]
    #for i in range(len(B)):
    #x,y,z = B[i][0:8],B[i][8:16],B[i][16:24]
    #arr_np[i,]= list([int(x,base=2),int(y,base=2),int(z,base=2)])

    img = Image.fromarray(data, 'RGB')
    img.save(name_for_image)
    return img
