# Project2
My second school project
Using a Neural Network to clasify croppings of geographic data
Uses data from USGS

*Warning* 
dataset is large (>450GB) run dataset_downloader at your own risk
alternatively, change the input file to only be a select number of images

uses rasterio to read geotiff files
download intructions [here](https://rasterio.readthedocs.io/en/latest/installation.html)

other modules used that (can be installed with pip):
- numpy
- shapely
- os
- shutil
- pandas
- matplotlib (optional)
- more to be added in time

Note: Tensor Flow requires a version of numpy that breaks rasterio. upgrading numpy will fix this

state boundary information from [here](https://public.opendatasoft.com/explore/dataset/us-state-boundaries/information/)

i will think about caching and other optimizations at another time