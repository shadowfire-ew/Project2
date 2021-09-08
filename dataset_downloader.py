# imports
import requests
import shutil
from os.path import exists

#the base format for links that download the tiff files
base_link = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/{fname}/USGS_13_{fname}.tif"

#the folder directory where our images will go
folder = "rawdata/"

if __name__ == "__main__":
    names = []

    with open("names.txt",'r') as f:
        names = f.read().split('\n')

    for name in names:
        destination = folder+name+".tif"
        if exists(destination):
            print(destination,"already exists")
        else:
            url = base_link.format(fname=name)
            print("retrieving",name,"from",url)
            req = requests.get(url,stream=True)

            if req.status_code == 200:
                print("saving to",destination)
                req.raw.decode_content = True

                with open(destination,'wb') as f:
                    shutil.copyfileobj(req.raw,f)
                
                print("finished saving to",destination)
            
            else:
                print("could not retrieve from",destination)
    input()
