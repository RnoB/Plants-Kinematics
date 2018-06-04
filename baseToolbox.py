import numpy as np 





def distPointToPoint(x,theta):
    
    distance = np.zeros((len(x[:,0]),len(x[:,0])))
    X = []
    for k in range(0,len(x[0,:])):
        X1 = np.tile(x[:,k],(len(x[:,k]),1))
        X2 = np.tile(x[:,k],(len(x[:,k]),1)).T

        distance += (X2-X1)**2
        X.append((X2-X1))
    X1 = X[0]*np.cos(-theta)+X[2]*np.sin(-theta)
    X2 = -X[0]*np.sin(-theta)+X[2]*np.cos(-theta)
    angle = np.arctan2(X1,X2)
    distance = np.sqrt(distance)
    return distance, angle

