import numpy as np
import hashlib 
import DES
import image_processing as ip
import encryption_module as em


def main():
    key = '0e329232ea6d0d73'
    #file_name =input("Enter Image file name : ")
    #file_name = 'pic1.jpg'
    #D = ip.image_to_blocks(file_name)
    #tag, h = em.encrypt_message(key, D)   
    ### TAG IS OF TYPE STR
    #print("Tag : ",tag,"\n h : ",h,"\n")
    #file_name2 = 'pic2.jpg'
    #D2 = ip.image_to_blocks(file_name2)
    #tag2, h2 = em.encrypt_message(key, D2)
    #print("Tag2 : ",tag2,"\n h2 : ",h2,"\n")
    
    D = ['1101'*16,'1010'*16,'0011'*16,'0000'*16]
    tag, h = em.encrypt_message(key, D)   
    print("Tag : ",tag,"\n h : ",h,"\n")
    
    D2 = ['1001'*16,'1010'*16,'0011'*16,'0000'*16]
    tag2, h2= em.encrypt_message(key, D2)   
    print("Tag : ",tag2,"\n h : ",h2,"\n")
    
    indices, update_list = ip.test_run_incremental()
    
    tag_updated, h1 = em.incremental_update_genrate_hash(key,tag,indices,D,update_list)   
    print("\nTag_updated : ",tag_updated,"\n h1 : ",h1,"\n")

# To do
# compare size of hash vs file size, 
# take input from a file, see how the size of file impacts the time of the program
# form a simple counter mode encryption for complete file all bits which can be decrypted at the other end    

if __name__ == "__main__":
    main()



