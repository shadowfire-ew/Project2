# imports
import requests
import shutil

#the base format for links that download the tiff files
base_link = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/{northsouthdegree}{eastwestdegree}/USGS_1_{northsouthdegree}{eastwestdegree}.tif"
