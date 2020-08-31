import skimage.io
from Crypto.Hash import MD5
import hashlib 
  
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


#def incremental_update_image(hash_bin,hash_md5,index_to_update,new_value):


def main():
    file_name =input("Enter Image file name : ")
    block_size_in_bytes =int(input("Enter block_size in bytes : "))
    IV =int(input("Enter Initialization Vector IV : "))
    counter = int(input("Enter counter start value : "))
    bin_hash, md5_hash = encrypt_image(file_name,block_size_in_bytes,IV,counter)
    print("Binary value of hash : ",bin_hash,"\n","MD5 hash for the image file : ",md5_hash)

if __name__ == "__main__":
    main()


