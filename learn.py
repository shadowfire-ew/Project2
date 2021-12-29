"""
this file will hold all the nescessary functions for learning
will need to create .py files for each type of learning schema
i think that i will be able to make this scalable
"""

from dataset_slicer_labeler import ImageSet
from neuralnet import NeuralNetwork
from labels import FindStateBoundaries
import numpy as np
import matplotlib.pyplot as plt


def Teach(fname,slice_size,slice_step,alpha,epochs,lam,labels,hidden_layers=()):
    """
    this function will handle the actual teaching of the various models
    returns a neuralnetwork and costs over time
    """
    # want to get updates for every 10% acheived
    checkinterval = 1
    if epochs > 20:
        checkinterval = epochs//10
    # prepare for the set loading
    set = ImageSet(slice_size,slice_step)
    # add the labels to our set
    for i in range(len(labels)):
        set.addLabel(i,labels[i])
    # our list of names
    names = None
    with open(fname,'r') as f:
        names = f.read().split('\n')
    # our NN object
    # input layer
    layers=[slice_size**2]
    # hidden layers
    for hidden in hidden_layers:
        layers.append(hidden)
    # output layer
    layers.append(len(labels))
    net = NeuralNetwork(tuple(layers))
    costs = []
    # gradient descent through epochs
    print("begining")
    checker = False
    for i in range(epochs):
        if i%checkinterval== 0:
            print("epoch #{a} our of {b}".format(a=i,b=epochs))
            checker = True
        # go through all names
        sumparts = []
        for cname in names:
            # load the group around the name
            set.loadImage(cname)
            # get every slice within the name
            cslice,label = set.getNextSlice()
            # prepare y to compare to
            y = [0]*len(labels)
            while cslice is not None:
                # apply the label
                if label is not None:
                    y[label] = 1
                yarr = np.array(y)
                # apply forward and back prop
                hypo=None
                try:
                    hypo = net.ForwardProp(cslice)
                except Exception as err:
                    print("recieved error {0}".format(err))
                    print(cslice)
                    print(set._rowOffset,set._colOffset)
                    return
                leftpart = np.nan_to_num(np.log(hypo)*yarr)
                onesv = np.ones(hypo.shape)
                rightpart = np.nan_to_num((onesv-y)*np.log(onesv-hypo))
                fullpart = leftpart+rightpart
                sumparts.append(np.sum(fullpart))
                # apply backprop
                net.BackProp(hypo,yarr)
                cslice,label = set.getNextSlice()
            # end of file, go to next one
        # end of epoch
        # calc cost
        # the output cost
        cost_left = -1/(len(sumparts)) * np.sum(sumparts, axis=0)
        # regularization cost
        cost_right = 0
        thetas = net.GetThetas()
        for t in thetas:
            cost_right += np.sum(t**2)
        cost_right *= lam/(2*len(sumparts))
        # full cost
        costs.append(cost_left+cost_right)
        # early exit on cost increasing or negligible
        if i > 0:
            if costs[i]-costs[i-1]>=0:
                print("Cost increasing or not changing. skipping descent and exiting...")
                break
        # get derivative
        derivative = net.Derive(len(sumparts),lam)
        # apply derivative in gradient descent
        net.Descend(derivative,alpha)
    return net,costs

if __name__ == "__main__":
    fname = "panames.txt"
    label = FindStateBoundaries("Pennsylvania")
    nnLearn,costs = Teach(fname,25,3000,0.1,5,0,[label],(100,75))
    nnLearn.SaveToFile("testNN2_gradientDecsentBoogaloo.json")
    print(costs)
    plt.figure()
    plt.scatter(x=range(len(costs)),y=costs,color="red")
    plt.title("cost per epoch")
    plt.savefig("testNNdescentCosts.png")