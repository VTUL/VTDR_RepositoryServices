from test_md5 import md5sum
import os
path="C:/Users/padma/.dart/bags/VTDR_P00099_Mc"



#path="F:\P00079_KuehlR_KuehlR_v01_20200213\data\P00079_KuehlR_KuehlR_v01_20200213"
path="F:\P00079_KuehlR_KuehlR_v01_20200213\data\P00079_KuehlR_KuehlR_v01_20200213"
payload=os.listdir(path)
print("payload", payload)
#md5_returned=md5sum(path).hexdigest()
#print("File's md5 checksum is ",md5_returned)

for root, dirs, files in os.walk(path):
    #print("root is",root)
    #print("dir is", dirs)
    #print("files are", files)
    for filename in files:
        print("root is",root)
        print("dir is", dirs)
        print("files are", files)
        print("FILENAME is ",filename)
        print("absolute path? ",os.path.join(os.path.abspath(root),filename))
        filewithpath=os.path.join(os.path.abspath(root),filename)
        md5_returned=md5sum(filewithpath).hexdigest()
        #print("destination path? ", os.path.join(destndir,filename))
        #md5_returned=md5sum(filename).hexdigest()
        print("File's md5 checksum is ",md5_returned)
