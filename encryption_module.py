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
#    print("Type R[0] ",type(R[0]))
    h=0
    l = len(R)
    for i in range(l-1):
        h=h^f1( hex(int(R[i],2))[2:] , R[i+1])
    h=h^f1( hex(int(R[l-1],2))[2:] , R[0])
#    print("Line 47 h without 0 and 1 ",h^f1( hex(int(R[0],2))[2:] , R[1]))
#    print("Line 48 h without 0 and 1 ",h^f1( hex(int(R[0],2))[2:] , R[1]))
    tag = DES.encrypt_DES(key_tag,hex(h))
    return tag,hex(h)

def incremental_update_genrate_hash(key_tag,tag,indices_to_update_list_sorted,original_message_list,updated_messages_list_ac_indices):
    ### TAG IS OF STR TYPE
    ### 2nd argument should be str type
    h = DES.decrypt_DES(key_tag,tag)
    #print("From em module line 56 h we have decrypted",h)
    h=int(h,16)
    #print("From em module line 58 h we have decrypted",h)
    #print(h,type(h))
    to_remove = 0
    R = randomize_blocks(original_message_list)
    #print(R)
    ### str type
    N = len(R)
    nb = len(indices_to_update_list_sorted)
    #print(N,nb)
    for i in range(nb) :
        if ((indices_to_update_list_sorted[i]!= N-1)&(indices_to_update_list_sorted[i]!= 0)):
            to_remove=to_remove^f1( hex(int(R[i],2))[2:] , R[i+1])^f1( hex(int(R[i-1],2))[2:] , R[i])   
        elif (indices_to_update_list_sorted[i]==N-1):
            to_remove=to_remove^f1( hex(int(R[N-1],2))[2:] , R[0])^f1( hex(int(R[N-2],2))[2:] , R[N-1])
        elif (indices_to_update_list_sorted[i]==0):            
            to_remove=to_remove^f1( hex(int(R[N-1],2))[2:] , R[0])^f1( hex(int(R[0],2))[2:] , R[1])
    #print("f1 line 72 ",f1( hex(int(R[i],2))[2:] , R[i+1]))
    #print(to_remove)
    #print("line 74 em ", h^to_remove)
    to_add = 0
    R_new = randomize_blocks(updated_messages_list_ac_indices)
    #print("R_new", R_new)
    for i in range(nb):
        R[indices_to_update_list_sorted[i]] = R_new[i]
    for i in range(nb) :
        if ((indices_to_update_list_sorted[i]!= N-1)&(indices_to_update_list_sorted[i]!= 0)):
            to_add=to_add^f1( hex(int(R[i],2))[2:] , R[i+1])^f1( hex(int(R[i-1],2))[2:] , R[i])   
        elif (indices_to_update_list_sorted[i]==N-1):
            to_add=to_add^f1( hex(int(R[N-1],2))[2:] , R[0])^f1( hex(int(R[N-2],2))[2:] , R[N-1])
        elif (indices_to_update_list_sorted[i]==0):            
            to_add=to_add^f1( hex(int(R[N-1],2))[2:] , R[0])^f1( hex(int(R[0],2))[2:] , R[1])

    h=h^to_remove^to_add
    #print("line 82 h ", h, type(h))
    tag_updated = DES.encrypt_DES(key_tag,hex(h))
    return tag_updated, hex(h)

