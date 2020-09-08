import numpy as np
import hashlib 
import DES
import image_processing as ip
import encryption_module as em


def main():
    key = '0e329232ea6d0d73'
    
    D1 = ip.image_to_blocks('pic1.png')
    tag1, h1 = em.encrypt_message(key, D1)   
    print("Tag1 : ",tag1,"\n h1 : ",h1,"\n")
    
    D2 = ip.image_to_blocks('pic2.png')
    tag2, h2= em.encrypt_message(key, D2)   
    print("Tag2 : ",tag2,"\n h2 : ",h2,"\n")
    
    indices , update_list = ip.difference_between_2_arrays(D1,D2)
    print(indices,update_list)
    tag_updated, h1 = em.incremental_update_genrate_hash(key,tag1,indices,D1,update_list)   
    print("\nTag_updated : ",tag_updated,"\n h1 : ",h1,"\n")

# To do
# compare size of hash vs file size, 
# take input from a file, see how the size of file impacts the time of the program
# form a simple counter mode encryption for complete file all bits which can be decrypted at the other end    

if __name__ == "__main__":
    main()



