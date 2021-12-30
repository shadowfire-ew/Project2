"""
learns agains the full PA dataset
"""
from learn import Teach
from labels import FindStateBoundaries
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    fname = "panames.txt"
    slice_size = 25
    slice_step = 10
    alpha = 0.1
    epochs = 1000
    lam = 0.1
    labels = [FindStateBoundaries("Pennsylvania")]
    hidden_layers = (210,70,20)
    start = time.time()
    nnPA,costs = Teach(fname,slice_size,slice_step,alpha,epochs,lam,labels,hidden_layers)
    total = (time.time()-start)/(3600)
    print("Learning done in {a} epochs, {b} hours".format(a=len(costs),b=total))
    sfname = "PAonlyNN.json"
    nnPA.SaveToFile(sfname)
    print("neural network saved to",sfname)
    ifname="PAonlyNNcosts.png"
    plt.figure()
    plt.scatter(x=range(len(costs)),y=costs)
    plt.title("cost per epoch")
    plt.savefig(ifname)
    print("Cost Descent graph save to",ifname)
    print("costs:",costs)