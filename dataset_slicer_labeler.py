import numpy as np
import rasterio as rio
from dataset_downloader import get_path
from os.path import exists
class ImageSet:
    """
    this class will hold onto a set of images

    """
    def __init__(self,sliceSize, sliceStep):
        # this array holds our numpy arrays of the images
        self._images = [[None,None,None],
                        [None,None,None],
                        [None,None,None]]
        
        # this array holds our rasterio objects
        self._names = [ [None,None,None],
                        [None,None,None],
                        [None,None,None]]
        
        # our internal offset for position
        # used as our center
        # technically stored as pixel location, but this is easy to convert to geo-coordinates
        self._xOffset = 0
        self._yOffset = 0

        # the size of (one side of) our square slices (should be in pixels)
        self._sliceSize = sliceSize

        # how many pixels we move in each step
        self._sliceStep = sliceStep

        # our polygon lookup dict
        # used for labeling points
        self._labels={}
    
    def loadGroup(self,name):
        """
        takes the name and loads it and the images next to it spatially
        If the image name is already in our names list, we will shift their references
        this would recenter our focused name and put Nones in the unloaded images' spaces
        if the name is not in our names set, it will reload the entire array of images

        name will be just the name as it appears in our names.txt
        """
        if self._names[1][1] is not None:
            # when we already have loaded some info

            # check to see if we already loaded the image
            shift = None
            for x in [-1,0,1]:
                brk = False
                for y in [-1,0,1]:
                    if name in self._names[y+1][x+1].name:
                        brk = True
                        shift = (x,y)
                        break
                if brk:
                    break
            # now that we have our offset, time to fix our arrays
            if shift is not None:
                # if we find that we already loaded the image we want

                if shift == (0,0):
                    # in the odd case where we are trying to load the image that is already centered
                    return
                
                # move the arrays over to temp holders (as python is a referential language)
                tempnames = self._names
                tempimages= self._images
                # prep our new empty arrays
                self._names= [[None,None,None],
                              [None,None,None],
                              [None,None,None]]
                self._images= [[None,None,None],
                              [None,None,None],
                              [None,None,None]]
                # a range for easy checking
                t = range(3)
                for x in t:
                    for y in t:
                        # get our destination according to the shift
                        destX = x+shift[0]
                        destY = y+shift[1]
                        # check if we want to move to the destination
                        if destY in t and destX in t:
                            # copying the element reference from the original array to the new array in its new position
                            self._names[destY][destX] = tempnames[y][x]
                            self._images[destY][destX] = tempimages[y][x]
                # after all that, we are have properly prepared the array for the next step
        else:
            # this is the first array time loading the data
            self._names[1][1] = rio.open(get_path(name))

        # here is where we open the neighbors that can and need to be loaded
        cx = int(name[4:7])
        cy = int(name[1:3])
        for x in range(3):
            for y in range(3):
                if self._names[y][x] is None:
                    # only when we have not found this neighbor
                    # for x
                    xdir = name[3] # the 'e' or 'w'
                    xoff = x-1 # the base offset
                    xoff = xoff * ((xdir=='e')*2 + 1) # inverting our offset if we have 'w'
                    xlab = xoff + cx # getting the new x
                    # for y
                    ydir = name[0] # the 'n' or 's'
                    yoff = (y-1)
                    yoff = yoff * ((ydir=='s')*2 + 1) # inverting our offset if we have 'e'
                    ylab = yoff + cy # getting the new y
                    # after that math, we build our new name, formatted like
                    nname = ydir + str(ylab).zfill(2) + xdir + str(xlab).zfill(3)
                    # getting the relative path
                    pname = get_path(nname)
                    # only try to open the file if it exists
                    if exists(pname):
                        self._names[y][x] = rio.open(pname)

        # here is where we open the images
        for x in range(3):
            for y in range(3):
                if (self._names[y][x] is not None) and (self._images[y][x] is None):
                    # we only want to try to lead images that exist and are not already loaded
                    self._images[y][x] = self._names[y][x].read(1)

        # reset our offsets
        # this weird term means that only when there is nothing to the left or top of the image do we offset
        """ i.e.
        [[None,None,None],    xOffset = 0               [[Some,Some,None],    xOffset = 0
         [Some,Some,Some], => |                     and  [Some,Some,None], => |
         [Some,Some,Some]]    yOffset = sliceSize/2      [None,None,None]]    yOffset = 0
        """
        self._xOffset = self._sliceSize//2 * (self._names[1][0] is None or self._names[0][0] is None)
        self._yOffset = self._sliceSize//2 * (self._names[0][1] is None or self._names[0][0] is None)
    
    def getNextSlice(self):
        """
        returns a slice and label of our loaded images
        the slice will be an array of the size decided upon init
        the label will be one of two things:
            - the label for the center point if it is within one of our label polygons
            - None for anything outside
        after getting the slice, it will itterate the offset(s)
        it will avoid corners/edges with missing peices
        all slices will be centered within the cCenter image
        will return None,None when it cannot get any more new slices
        """

    def getCurrentOffset(self):
        return self._xOffset,self._yOffset
    
    def addLabel(self,name,polygon):
        """
        add a labeling polygon to the labels dictionary
        this will be used for labeling points
        enforcing strict tying for both parameters:
            - name is str
            - polygon must be a polygon-like
        """
        if (type(name) is str) and (type(polygon) is list):
            # TODO: look into a dedicated polygon class which will determine point containment
            self._labels[name]=polygon
        else:
            raise TypeError

if __name__ == "__main__":
    print("\n\n")
    m=ImageSet(100,33)
    m.loadGroup("n23w160")
    for y in range(3):
        for x in range(3):
            if m._names[y][x] is not None:
                print("m_{x},{y}:".format(x=x,y=y)+m._names[y][x].name, end="\t")
            else:
                print("m_{x},{y}:".format(x=x,y=y)+str(m._names[y][x]), end="\t\t\t")
        print()
        