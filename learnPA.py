"""
learns agains the full PA dataset
"""
from learn import Teach
from labels import FindStateBoundaries
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fname = "panames.txt"
    slice_size = 25
    slice_step = 10
    alpha = 0.1
    epochs = 1000
    lam = 0.1
    labels = [FindStateBoundaries("Pennsylvania")]
    hidden_layers = (210,70,20)
    nnPA,costs = Teach(fname,slice_size,slice_step,alpha,epochs,lam,labels,hidden_layers)
    print("Learning done in {a} epochs".format(),a=len(costs))
    sfname = "PAonlyNN.json"
    print("neural network saved to",sfname)
    nnPA.SaveToFile(sfname)
    plt.figure()
    plt.scatter(x=range(len(costs)),y=costs)
    plt.title("cost per epoch")
    plt.savefig("PAonlyNNcosts.png")