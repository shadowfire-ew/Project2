import numpy as np
import matplotlib.pyplot as plt

def sigmoid(val):
    return(1/(1+np.exp(-val)))

class NeuralNetwork:
    """
    a class that handles the neural network features and functions
    uses arrays rather than vectors
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
            print("please input at least an input and output count")
            raise Exception
        self._inputnum = sizes[0]
        self._thetas=[]
        for ind in range((len(sizes)-1)):
            # shaped specifically like this
            # because im using 1XN array/matrix/list for input
            self._thetas.append(np.random.rand(sizes[ind]+1,sizes[ind+1]))
        self._resetDeltas()
    
    def _resetDeltas(self):
        """
        resets our Delta matrices
        these inform how thetas are changed
        """
        self._deltas=[]
        for i in range(len(self._thetas)):
            thetashape = self._thetas[i].shape
            self._deltas.append(np.zeros(thetashape))


    def ForwardProp(self,inarray):
        """
        takes an input numpy array and transforms it through the neural network
        """
        inlen = len(inarray.shape)
        if inlen == 1:
            inlen = inarray[0]
        elif inlen == 2:
            inlen = inarray[1]
        else:
            inlen=-1
        if inarray.shape[0] != self._inputnum:
            print("Wrong input shape, expecting m by {a}".format(self._inputnum))
            raise Exception
        # reset activations
        self._a=[None]*(len(self._thetas)+1)
        # pass inputs as activations
        outarray=inarray
        # get remaining activations
        for ind in range(len(self._thetas)):
            theta = self._thetas[ind]
            # add bias and save to activations
            self._a[ind] = np.concatenate(([1],outarray))
            # linear transform into new dimensions
            outarray = np.matmul(self._a[ind],theta)
            # apply sigmoid
            outarray = sigmoid(outarray)
        # save final array
        self._a[-1] = outarray
        # return final array
        return(outarray)
    
    def BackProp(self,hypothesis,y):
        """
        inputs:
            the output array from forward prop
            and the intended y (np array)
        outputs:
            accumulates delta
        """
        if hypothesis.shape != y.shape:
            print("shapes do not match")
            raise Exception
        # set up delta arrays (to inform self._deltas)
        delta = [0]*len(self._thetas)
        # get our last entry (cost of outputs)
        delta[-1] = y-hypothesis
        # travel backwards
        for ind in reversed(range(1,len(self._thetas))):
            thetaT = np.transpose(self._thetas[ind])
            tempdelta = np.matmul(delta[ind],thetaT)
            delta[ind-1] = tempdelta[1:]
        # fold into Delta
        for ind in range(len(self._deltas)):
            aT=np.reshape(self._a[ind],(-1,1))
            deltaMat = np.reshape(delta[ind],(1,-1))
            self._deltas[ind] += np.matmul(aT,deltaMat)
            

if __name__ == "__main__":
    # test NN constructor
    testNN = NeuralNetwork((3,2,1))
    """#------------
    for arr in testNN._thetas:
        print(arr.shape)
    #"""#------------
    """#------------
    # test sigmoid
    x = np.linspace(-10,10,100)
    z = sigmoid(x)
    plt.plot(x,z)
    plt.xlabel("X")
    plt.ylabel("Sigmoid(X)")
    plt.show()
    #"""#------------
    # testing
    x = np.array([0.6,0.9,0.1])
    y = np.array([1])
    y1 = testNN.ForwardProp(x)
    print(type(y1))
    print(y-y1)
    testNN.BackProp(y1,y)