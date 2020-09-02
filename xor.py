import numpy as np
import hashlib 
import DES
import image_processing as ip
import encryption_module as em


def main():
    key = '0e329232ea6d0d73'
    file_name =input("Enter Image file name : ")
    D = ip.image_to_blocks(file_name)
    tag, h = em.encrypt_message(key, D)
    print(tag,h)
    

if __name__ == "__main__":
    main()



