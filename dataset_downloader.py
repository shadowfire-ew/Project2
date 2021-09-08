# imports
import requests
import shutil
from os.path import exists
from collections import defaultdict

#the base format for links that download the tiff files
base_link = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/{fname}/USGS_13_{fname}{time}.tif"

#the folder directory where our images will go
folder = "rawdata/"

if __name__ == "__main__":
    names = []

    misses=[]

    catches=defaultdict(lambda:'')

    with open("names.txt",'r') as f:
        names = f.read().split('\n')

    with open("catches.txt",'r') as f:
        temp = f.read().split('\n')
        for part in temp:
            a = part.split(' ')
            catches[a[0]]='_'+a[1]

    for name in names:
        destination = folder+name+".tif"
        if exists(destination):
            print(destination,"already exists")
            pass
        else:
            url = base_link.format(fname=name,time=catches[name])
            print("retrieving",name,"from",url)
            req = requests.get(url,stream=True)

            if req.status_code == 200:
                print("saving to",destination)
                req.raw.decode_content = True

                with open(destination,'wb') as f:
                    shutil.copyfileobj(req.raw,f)
                
                print("finished saving to",destination)
            
            else:
                print("could not retrieve from",url)
                misses.append(name)
    
    with open("misses.txt",'w') as f:
        for miss in misses:
            f.write(miss+'\n')
