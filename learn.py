"""
this file will hold all the nescessary functions for learning
will need to create .py files for each type of learning schema
i think that i will be able to make this scalable
"""

from dataset_slicer_labeler import ImageSet


class Teacher:
    """
    this class will handle the teaching of our algorithms
    """
    def __init__(self,epochs,alpha,slice_size,slice_step,labels):
        self._epochs = epochs
        self._alpha = alpha
        self._set = ImageSet(slice_size,slice_step)
        # TODO: somehow get our polygon info
        for label in labels:
            self._set.addLabel(label,["polygon"])

    def teach(self):
        """
        this function will handle the actual teaching of the various models
        it will then save them to files
        returns a satus
        TODO: how to approach epochs with our progressive dataset loading
        """
        names = None
        with open("names.txt",'r') as f:
            names = f.read().split('\n')
        # how the images will be handled
        for cname in names:
            self._set.loadGroup(cname)
            cslice,label = self._set.getNextSlice()
            while cslice is not None:
                # do something, maybe go through all the epochs?
                cslice,label = self._set.getNextSlice()
        return "done"