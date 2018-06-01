import numpy as np 





def distPointToPoint(x,theta):
    
    distance = np.zeros((len(x[:,0]),len(x[:,0])))
    X = []
    for k in range(0,len(x[0,:])):
        X1 = np.tile(x[:,k],(len(x[:,k]),1))
        X2 = np.tile(x[:,k],(len(x[:,k]),1)).T

        distance += (X1-X2)**2
        X.append((X1-X2))
    X1 = X[0]*cos(-theta)+X[1]*sin(-theta)
    X2 = -X[0]*sin(-theta)+X[1]*cos(-theta)
    angle = np.arctan2(X1,X2)
    distance = np.sqrt(distance)
    return distance, angle

