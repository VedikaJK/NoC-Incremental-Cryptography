import skimage.io
from PIL import Image
import numpy as np
from Crypto.Hash import MD5
import hashlib 
import DES
  
def read_image_convert_to_array(file_name):
    a = skimage.io.imread(fname="pic1.jpg") # read image
    a=a.flatten(order='C') #flattened pixel array
    return a

def int_array_to_binary(arr):
    binary_arr = []
    for i in range(len(arr)):
        binary_arr.append(bin(int(arr[i]))[2:].zfill(8))
    return binary_arr

def binary_pixels_to_blocks(pixels_bin, block_size_in_bytes):
    B=[]
    n = len(pixels_bin)//block_size_in_bytes
    for i in range(n):
        temp = pixels_bin[3*i:3*(i+1)]
        B.append(''.join(temp)) 
    return B
    # 64 BIT BLOCKS
    #t=''
    #for i in range(len(b)):
    #    if(i%8==0):
    #        t = b[i]
        
    #    else:
    #        t+=b[i]
    #        if((i+1)%8==0):
    #            D.append(t)
    #        elif(i==len(b)-1):
    #            D.append(t)
    # if len(D[len(D)-1])<64 then ... padding

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

def encrypt_image(file_name, block_size_in_bytes, IV, counter):
    arr = read_image_convert_to_array(file_name)
    arr =int_array_to_binary(arr)
    arr = binary_pixels_to_blocks(arr,block_size_in_bytes)
    list_blocks_int = []
    blocks_cipher_list = []
    for i in range(len(arr)):
        x= (int(arr[i], base=2))
        c= x^counter^IV
        counter+=1
        #final_hash_int^=c
        list_blocks_int.append(x)
        blocks_cipher_list.append(c)
    #final_hash_int = ''.join(blocks_cipher_list)
    temp=[]
    for i in range(len(blocks_cipher_list)):
        temp.append(bin(int(blocks_cipher_list[i]))[2:].zfill(8))
    final_hash_str = ''.join(temp)
    
    hash = MD5.new()
    message=str(final_hash_str).encode('utf-8')
    hash.update(message)
    final_hash_md5 = hash.hexdigest()
    return final_hash_str, final_hash_md5

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
    print(DES.encrypt_DES(key,pt))
    print(DES.decrypt_DES(key,DES.encrypt_DES(key,pt)))

if __name__ == "__main__":
    main()



