import os
import shutil

folder = r"C:/Users/padma/anaconda3/envs/curation/MissedGoogleDriveBags"
subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

for sub in subfolders:
    for f in os.listdir(sub):
        src = os.path.join(sub, f)
        dst = os.path.join(folder, f)
        shutil.move(src, dst)