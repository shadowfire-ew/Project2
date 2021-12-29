import numpy as np
import rasterio as rio
import shapely.geometry as geo
from dataset_downloader import get_path
from os.path import exists
import labels
class ImageSet:
    """
    this class will hold onto a set of images
    """
    def __init__(self,sliceSize, sliceStep):
        # the numpy array of the image data
        self._image=None
        
        # the rasterio object associated with the object
        self._data=None
        
        # our internal offset for position
        # used as our top-left
        # technically stored as pixel location, but this is easy to convert to geo-coordinates
        self._rowOffset = 0
        self._colOffset = 0

        # the size of (one side of) our square slices (should be in pixels)
        self._sliceSize = sliceSize

        # how many pixels we move in each step
        self._sliceStep = sliceStep

        # our polygon lookup dict
        # used for labeling points
        self._labels={}

        # our col traverse direction
        # turns negative every time we hit the edge
        self._coldir = 1
    
    def loadImage(self,name):
        pname = get_path(name)
        if not exists(pname):
            print(pname,"does not exist")
            return
        self._data = rio.open(pname)
        print("loading",self._data.name)
        self._image = self._data.read(1)
        self._rowOffset = 0
        self._colOffset = 0
    
    def getNextSlice(self):
        """
        returns a slice and label of our loaded images \n
        the slice will be an array of the size decided upon init \n
        the label will be one of two things:
            - the label for the center point if it is within one of our label polygons
            - None for anything outside \n
        after getting the slice, it will itterate the offset(s) \n
        it will avoid corners/edges with missing peices \n
        all slices will be centered within the cCenter image \n
        will return None,None when it cannot get any more new slices \n
        """
        pos, label = self.getNextLabel()
        if pos is None:
            return None, None
        part = self._image[pos[0]:pos[0]+self._sliceSize,pos[1]:pos[1]+self._sliceSize]
        return part.flatten(), label
        
    
    def getNextLabel(self):
        """
        this function iterates our internal offsets
        it returns 2 things:
            - the internal offsets as a tuple (before itteration)
            - the label for those offsets
        
        this function can also be called externally of getNextSlice
        this will skip the slice for now
        """
        # get the matrix location
        rtuple = (self._rowOffset,self._colOffset)
        # get the geopos location of our offset
        x = self._rowOffset + self._sliceSize//2
        y = self._colOffset + self._sliceSize//2
        centercoords = self._data.xy(x,y)
        # translate that to the label
        rlabel = None 
        # iterate through labeling shapes
        for dlabel in self._labels.keys():
            centerpoint = geo.Point(centercoords)
            if (centerpoint.within(self._labels[dlabel])):
                rlabel = dlabel
                break
        # if the loop goes all the way through, we do not have a label for the geopos

        # change the position
        # tranlsate x by step
        self._colOffset += self._sliceStep*self._coldir
        # check the edges
        tocheck = self._image.shape[1]
        dist = tocheck-self._colOffset
        tonextrow = False
        # if we are too close to the edge of the matrix
        if (dist < (self._sliceSize+self._sliceStep+1)):
            tonextrow = True
            self._coldir = -1
        elif (self._colOffset <= 0):
            self._colOffset = 0
            tonextrow = True
            self._coldir = 1
        if tonextrow:
            # itterate y
            self._rowOffset += self._sliceStep
            # if the new y is over the limit, we exit
            tocheck = self._image.shape[0]
            dist = tocheck-self._rowOffset
            if dist < (self._sliceSize+self._sliceStep+1):
                return None,None
        return rtuple, rlabel

    def getCurrentOffset(self):
        return self._rowOffset,self._colOffset
    
    def addLabel(self,name,polygon):
        """
        add a labeling polygon to the labels dictionary
        this will be used for labeling points
        enforcing strict tying for both parameters:
            - name is str
            - polygon must be a polygon-like
        """
        if (type(polygon) is geo.Polygon):
            self._labels[name]=polygon
        else:
            raise TypeError
    

if __name__ == "__main__":
    m=ImageSet(50,33)
    print("adding pa label")
    pashape = labels.FindStateBoundaries("Pennsylvania")
    m.addLabel("pa",pashape)
    print("pa label done\nloading first image")
    m.loadImage("n41w077")
    print(m._data.name)
    pos,lab = m.getNextLabel()
    print(pos,lab)
    arr,lab2 = m.getNextSlice()
    print(arr,lab2)
