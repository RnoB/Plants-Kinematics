import numpy as np 





def distPointToPoint(x):
    
    distance = np.zeros((len(x[:,0]),len(x[:,0])))
    for k in range(0,len(x[0,:])):
        X1 = np.tile(x[:,k],(len(x[:,k]),1))
        X2 = np.tile(x[:,k],(len(x[:,k]),1)).T

        distance += (X1-X2)**2
    distance = np.sqrt(distance)


def distPointToPoint(x):
    
    distance = np.zeros((len(x[:,0]),len(x[:,0])))
    for k in range(0,len(x[0,:])):
        X1 = np.tile(x[:,k],(len(x[:,k]),1))
        X2 = np.tile(x[:,k],(len(x[:,k]),1)).T

        distance += (X1-X2)**2
    distance = np.sqrt(distance)

