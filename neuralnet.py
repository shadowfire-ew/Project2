import numpy as np
import matplotlib.pyplot as plt

def sigmoid(val):
    return(1/(1+np.exp(-val)))

class NeuralNetwork:
    """
    a class that handles the neural network features and functions
    """
    def __init__(self,sizes=(1,1)):
        """
        takes an input luplte of sizes
        needs to be at least len 2
        index[0] = input number
        index[-1] = output number
        """
        if type(sizes) is not tuple:
            print("please input a tuple")
            raise Exception
        if len(sizes) < 2:
            print("please input")
        self._inputnum = sizes[0]
        self._thetas=[]
        for ind in range((len(sizes)-1)):
            # shaped specifically like this
            # because im using 1XN array/matrix/list for input
            self._thetas.append(np.random.rand(sizes[ind]+1,sizes[ind+1]))
    

if __name__ == "__main__":
    # test NN constructor
    testNN = NeuralNetwork((3,2,1))
    for arr in testNN._thetas:
        print(arr.shape)
    """--------
    # test sigmoid
    x = np.linspace(-10,10,100)
    z = sigmoid(x)
    plt.plot(x,z)
    plt.xlabel("X")
    plt.ylabel("Sigmoid(X)")
    plt.show()
    #"""