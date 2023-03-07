import os
import io
import hashlib
def md5sum(src, length=io.DEFAULT_BUFFER_SIZE):
    calculated = 0
    md5 = hashlib.md5()
    with io.open(src, mode="rb") as fd:
        for chunk in iter(lambda: fd.read(length), b''):
            md5.update(chunk)
            calculated += len(chunk)
            #callback(calculated)
            #print("amount calculated",calculated)
    #print(md5)
    return md5


#src1="F:/VTechbags/P00023-tarred/P00023_MarekP_MarekP_v01_20171117.tar"
#x=md5sum(src1).hexdigest()
#print(x)
#src2="G:/Shared drives/CurationServicesGoogleDriveArchive/BAGS/Completed_BAGS/P00023_bagged/P00023-tarred/P00023_MarekP_MarekP_v01_20171117.tar"
#y=md5sum(src2).hexdigest()
