import numpy as np

class ImageSet:
    """
    this class will hold onto a set of images

    """
    def __init__(self,sliceSize, sliceStep):
        self._images = [[None,None,None],
                        [None,None,None],
                        [None,None,None]]
        self._names = [ [None,None,None],
                        [None,None,None],
                        [None,None,None]]
        self._xOffset = 0
        self._yOffset = 0
        self._sliceSize = sliceSize
        self._sliceStep = sliceStep
        self._labels=[]
    
    def loadGroup(self,name):
        """
        takes the name and loads it and the images next to it spatially
        If the image name is already in our names list, we will shift their references
        this would recenter our focused name and put Nones in the unloaded images' spaces
        if the name is not in our names set, it will reload the entire array of images
        """
    
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
        """
    
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
    m=ImageSet()