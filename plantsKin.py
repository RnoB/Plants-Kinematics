import numpy as np
import math


InteractionsName = ['Tropism','ApicalTropism','Proprioception']
GrowthMode = ['Apical','Exponential']



class skeletonElements:

    x = np.zeros((1,3))
    theta = 0
    curvature = 0
    s = 0
    ds = .1
    psiC = 0
    psiG = 0

    theta0 = 0
    thetaApical =0
    psi0 = 0
    interactions = []
    growth = {'name':'no'}

    def __init__(self,x,theta0,curvature0,s,ds,psi0 = 0,psiC0 = 0,psiG0 = 0,dt = .1):
        
        self.x = x
        self.theta = theta0
        self.curvature = curvature0
        self.ds = ds
        self.s = s
        self.psiC = psiC0
        self.psiG = psiG0
        self.psi0 = psi0
        self.dt = dt

    def updateCurvilinearAbscissa(self,s):
        self.s = s

    def updateApicalAngle(self,theta):
        self.thetaApical = theta

    def updateOrientation(self,theta):
        self.theta = theta  

    def updateSpatialPosition(self,x0,theta0,psi0,ds0):
        self.x[0]  = x0[0] + self.ds0 * (np.cos(theta0) * np.cos(psi0))
        self.x[1]  = x0[1] + self.ds0 * (np.cos(theta0) * np.sin(psi0))
        self.x[2]  = x0[2] + self.ds0 * (np.sin(theta0))


    def addInteractions(self,name,intensity=0,direction = 0):
        self.interactions.append({'name':name,'intensity':intensity,'direction':direction})

    def update(self):
        delta = 0
        deltaParrallel = 0
        deltaPerpendicular = 0
        for interaction in self.interactions:
            if interaction.name == 'Proprioception':
                deltaParrallel += self.growthRate * interaction.intensity * self.cuvature * self.dt
            else:
                if interaction.name == 'Tropism':
                    delta += self.growthRate * interaction.intensity * (self.theta - interaction.direction) * self.dt
                if interaction.name == 'ApicalTropism':
                    delta += self.growthRate * interaction.intensity * (self.thetaApical - interaction.direction) * self.dt
                deltaParrallel += delta * cos(self.psiG - self.psiC)
                delataPerpendicular += delta * sin(self.psiG - self.psiC)
        self.curvature = deltaParrallel * self.growthRate * self.dt
        if math.abs(self.curvature) >0:
            self.psiC = (deltaParrallel * self.growthRate * self.dt)/self.curvature
        if self.growth.name in GrowthMode:
            self.ds += self.ds * self.growth.rate * self.dt 






class Plant:


    x0 = np.zeros((1,3))

    theta0 = 0
    curvature0 = 0
    length0 = 1
    length = 1

    psi0 = 0
    ds = .1
    dt = .1
    skeleton = []

    interactions = []
    growth = {'no'}
    def __init__(self,x0,theta0=0,curvature0=0,length0 = 1,psi0 = 0,psiC0 = 0,psiG0 = 0,N = 100,dt=.1,growth = 'no',growthZone = 1,growthRate = 1):
        
        self.x = []
        self.s = []
        self.theta = []
        self.curvature = [] 

        self.x0 = x0
        self.theta0 = theta0
        self.curvature0 = curvature0
        
        self.length0 = length0
        self.length = length0
        self.ds = length0/N
        self.psi0 = psi0
        self.dt = dt

        x = self.x0
        theta = self.theta0
        curvature = self.curvature0

        self.growth = {'name':growth,'growthZone':growthZone,'growthRate':growthRate}

        s = 0

        self.skeleton.append(skeletonElements(np.copy(x),theta,curvature,0,self.ds,self.psi0,psiC0,psiG0,self.dt))
        

        for k in range(1,N):
            
            x[0]  = x[0] + self.ds * (np.cos(theta0) * np.cos(psi0))
            x[1]  = x[1] + self.ds * (np.cos(theta0) * np.sin(psi0))
            x[2]  = x[2] + self.ds * (np.sin(theta0))
            s += self.ds
            self.skeleton.append(skeletonElements(np.copy(x),theta,curvature,s,self.ds,self.psi0,psiC0,psiG0,self.dt))
        self.flatten()

    def updateSpatialPosition(self):
        s = 0
        for k in range(1,len(self.skeleton)):
            s += self.ds
            self.skel[k].updateCurvilinearAbscissa(s)
            self.skel[k].updateOrientation(self.skel[k-1].theta + self.skel[k-1].curvature * self.skel[k-1].ds)
            self.skel[k].updateSpatialPosition(self.skel[k-1].x,self.skel[k-1].theta,self.skel[k-1].psiC,self.skel[k-1].ds)
            


    def addInteractions(self,name,intensity=0,direction = 0):
        if name in InteractionsName:
            self.interactions.append({'name':name,'intensity':intensity,'direction':direction})
            for skel in self.skeleton:
                skel.addInteractions(name,intensity,direction)
        else:
            print(' --- '+name+' is not part of the known interactions ')
            print(' --- please use one of the following interaction :')
            for names in InteractionsName:
                print(' --- --- '+str(names))

    def flatten(self):
        
        self.x=np.array([skel.x for skel in self.skeleton])
        self.s=np.array([skel.s for skel in self.skeleton])
        self.theta=np.array([skel.theta for skel in self.skeleton])
        self.curvature=np.array([skel.curvature for skel in self.skeleton])
        self.length = self.s[-1]


    def updateGrowth(self):
        if self.growth.name in GrowthMode:
            for skel in self.skeleton:
                if growth.name == 'Exponential':
                    skel.growthRate = self.growth.growthRate 
                if growth.name == 'Apical':
                    if (self.length-skel.s) < growth.growthZone:
                        skel.growthRate = self.growth.growthRate

    def update(self):
        for skel in self.skeleton:
            skel.update()


        
