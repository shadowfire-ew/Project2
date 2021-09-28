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
    # just the names of the data files
    names = []

    # our failed gets
    misses=[]

    # using this dict allows for some elegant solutions later
    catches=defaultdict(lambda:'')

    with open("names.txt",'r') as f:
        # this is just our file with the names as they appear in the folder list
        names = f.read().split('\n')

    with open("catches.txt",'r') as f:
        # these are the files we missed the first time
        # it is a copy of the first misses file, but with the date added to the end
        # this is because the dataset only has these squares in the date-labeled format
        temp = f.read().split('\n')
        for part in temp:
            # because I used spaces between the name and date
            a = part.split(' ')
            # adding our date to the dict under the filename
            catches[a[0]]='_'+a[1]

    for name in names:
        # where we want to save the file
        destination = folder+name+".tif"
        # these destinations ignore the date from the files which had a date in their name from the source

        if exists(destination):
            # in case we already downloaded the file
            print(destination,"already exists")
            # just ignore this name
            pass
        else:
            # the url to retrieve from
            url = base_link.format(fname=name,time=catches[name])
            # a progress print
            print("retrieving",name,"from",url)
            # our get request. stream = true to allow us to stream the data (its large)
            req = requests.get(url,stream=True)

            if req.status_code == 200:
                # if we get the file
                # another progress print
                print("saving to",destination)
                # start decoding the raw data
                req.raw.decode_content = True

                # start writing the data to a file
                with open(destination,'wb') as f:
                    shutil.copyfileobj(req.raw,f)
                
                # last progress print per file
                print("finished saving to",destination)
            
            else:
                # when there is an error with the get request
                print("could not retrieve from",url)
                # save this name for later amelioration
                misses.append(name)
    
    with open("misses.txt",'w') as f:
        # writing our misses to a file, for inspection and amelioration
        for miss in misses:
            f.write(miss+'\n')
