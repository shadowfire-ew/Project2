# imports
import requests
import shutil
from os.path import exists

#the base format for links that download the tiff files
base_link = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/{name}/USGS_13_{name}.tif"

#the folder directory where our images will go
folder = "rawdata/"

