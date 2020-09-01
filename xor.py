import skimage.io
from PIL import Image
import numpy as np
from Crypto.Hash import MD5
import hashlib 
import DES
  
def read_image_convert_to_1D_pixel_array(file_name):
    ## THIS FUNCTION RETURNS ARRAY OF THE FORM [0 128 128 155 0 128 50 10 120 .. ] I.E. LENGTH = PIXELS * 3
    a = skimage.io.imread(fname="pic1.jpg") # read image
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

def randomize_blocks(D_is_array_64bits_blocks):
    R=[]
    for i in D_is_array_64bits_blocks:
        a = hashlib.md5(i.encode('utf-8'))
        b = a.hexdigest()
        as_int = int(b, 16)
        
        as_bin = bin(as_int)[2:66]   # taking a 64bit no. to randomize
        randomizer_number = int(as_bin, 2)
        print(as_int,as_bin,randomizer_number)
        R.append(bin(randomizer_number*int(i,2)%9223372036854775808)[2:].zfill(64))   # 2 to the power 63
    return R

def f1(key_in_hex,text_in_bin):
    key=key_in_hex
    hash = MD5.new()
    message=text_in_bin.encode('utf-8')
    hash.update(message)
    hash_md5 = hash.hexdigest()
    ### hash_md5 be like 3c1898a00cc4579728e1268191a64bc6 
    hash_bin=bin(int(hash_md5,16))[2:].zfill(128)
    ### hash_bin be like 00111100000110001001100010100000000011001...., type = str
    first_half = int(hash_bin[:64],2)
    second_half = int(hash_bin[64:],2)

    inner_des = DES.encrypt_DES(key, hex(first_half)[2:])   ### hex value
    final_input = int(inner_des,16)^second_half    
    result = DES.encrypt_DES(key,hex(final_input)[2:])

def encrypt_message(D):
    R = randomize_blocks(D)
    ### f1 chain and hash
    

    hash = MD5.new()
    message='abc'.encode('utf-8')
    hash.update(message)
    final_hash_md5 = hash.hexdigest()
    
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

#def incremental_update_image(hash_bin,hash_md5,index_to_update,new_value):


def main():
    #file_name =input("Enter Image file name : ")
    #block_size_in_bytes =int(input("Enter block_size in bytes : "))
    #IV =int(input("Enter Initialization Vector IV : "))
    #counter = int(input("Enter counter start value : "))
    #bin_hash, md5_hash = encrypt_image(file_name,block_size_in_bytes,IV,counter)
    #print("Binary value of hash : ",bin_hash,"\n","MD5 hash for the image file : ",md5_hash)
    key = '0E329232EA6D0D73'
    pt ='596F7572206C6970'
    f1(key,'1101'*16)
    #print(DES.encrypt_DES(key,pt))
    #print(DES.decrypt_DES(key,DES.encrypt_DES(key,pt)))

if __name__ == "__main__":
    main()



