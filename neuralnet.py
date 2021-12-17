import numpy as np
import matplotlib.pyplot as plt
import json
from os.path import exists

def sigmoid(val):
    return(1/(1+np.exp(-val)))

class NeuralNetwork:
    """
    a class that handles the neural network features and functions
    uses arrays rather than vectors
    """
    def __init__(self,sizes=(1,1)):
        """
        takes an input tuple of sizes;
        needs to be at least len 2:
        - index[0] = input number
        - index[-1] = output number
        \n
        if sizes is a string, the 
        """
        self._m=0
        if type(sizes) is str:
            # attempt to load from file
            self.LoadFromFile(sizes)
        else:
            if type(sizes) is not tuple:
                print("please input a tuple or string")
                raise TypeError
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
        self._m += 1
    
    def Derive(self,m,lam=0):
        """
        creates and returns partial derivatives to inform theta in whatever fasion
        input m is number of data points
            checked against internal counter for sanity
        lam is lambda for regularization term
        """
        if m != self._m:
            print("unmatching m values, call at end of epoch")
            raise Exception
        minv = 1/m
        derivative = [None]*len(self._deltas)
        for ind in range(len(self._deltas)):
            # get the base derivative
            derivative[ind]=self._deltas[ind]*minv
            # get the regularization term
            regularizer = self._thetas[ind]*lam
            # remove the theta0's (0th row of each matrix)
            regularizer[0] = np.zeros(len(regularizer[0]))
            # apply the regularization term to the derivative
            derivative[ind]+=regularizer
        self._m=0
        self._resetDeltas()
        return derivative


        
    def Descend(self,derivative,alpha):
        """
        applies gradient descent to thetas
        multiplies the derviative by alpha
        then adds that to theta
        """  
        if len(derivative) != len(self._thetas):
            print("Wrong derivative")
            raise Exception
        for i in range(len(self._thetas)):
            self._thetas[i] += derivative[i]*alpha
    
    def SaveToFile(self,fname):
        tosave = []
        for t in self._thetas:
            tosave.append(t.tolist())
        with open(fname, 'w+') as fhandle:
            json.dump(tosave,fhandle)
            fhandle.close()

    def LoadFromFile(self,fname):
        if not(exists(fname)):
            print("file does not exist. will not attempt top load")
            return
        jsin = None
        with open(fname, 'r') as fhandle:
            jsin = json.load(fhandle)
            fhandle.close()
        if type(jsin) is not list:
            print(type(jsin))
        self._thetas = []
        for mat in jsin:
            self._thetas.append(np.array(mat))
        self._inputnum = self._thetas[0].shape[0]-1
        self._resetDeltas()
            

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
    print("init hypothesis",y1)
    print("init dif",y-y1)
    print("getting backprop")
    testNN.BackProp(y1,y)
    print("getting derivative")
    deriva = testNN.Derive(1,1)
    print("derivative",deriva)
    print("applying gradient descent")
    testNN.Descend(deriva,0.1)
    y2 = testNN.ForwardProp(x)
    print("new hypothesis",y2)
    print("new dif",y-y2)
    print("differences in difs",(y-y1)-(y-y2))
    print("saving to json file")
    testNN.SaveToFile("testNN.json")
    print("loading from json")
    testNN.LoadFromFile("testNN.json")