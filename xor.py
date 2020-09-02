import skimage.io
from PIL import Image
import numpy as np
from Crypto.Hash import MD5
import hashlib 
import DES
import image_processing as ip

def randomize_blocks(D_is_array_64bits_blocks):
    R=[]
    for i in D_is_array_64bits_blocks:
        a = hashlib.md5(i.encode('utf-8'))
        b = a.hexdigest()
        as_int = int(b, 16)
        
        as_bin = bin(as_int)[2:66]   # taking a 64bit no. to randomize
        randomizer_number = int(as_bin, 2)
        #print(as_int,as_bin,randomizer_number)
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
    return int(result,16)


def encrypt_message(key_tag,D):
    R = randomize_blocks(D)
    #print("Okay R ",R, len(R))
    ### f1 chain and hash
    h=0
    #print("Hello hex R[1] ",hex(int(R[1],2))[2:])
    for i in range(len(R)-1):
    #    print("Okay ",i)
    #   print(len(R[1]))
        h=h^f1( hex(int(R[i],2))[2:] , R[i+1])
#        print(f1( hex(int(R[0],2))[2:] , R[1]))
        
    #print(h)
    tag = DES.encrypt_DES(key_tag,hex(h))
    return tag,hex(h)
    

#def incremental_update_image(tag_in_hex,indices_list_sorted,message_list):


def main():
    key = '0e329232ea6d0d73'
    file_name =input("Enter Image file name : ")
    D = ip.image_to_blocks(file_name)
    #print(len(D))
    tag, h = encrypt_message(key, D)
    print(tag,h)
    

if __name__ == "__main__":
    main()



