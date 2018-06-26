
import math
import numpy as np
import numpy.matlib
import time
import uuid
import os
import sqlite3
import datetime
import threading
import multiprocessing 
import time
import random
import sys
sys.path.append("../src/")
import plantsKin as pk
from math import pi

threaded = True
nThreads = 10
parametersName = 'PlantsParameters.db'
dbName = 'PlantsSimulation.db'
dbVideo = 'PlantsVideo.db'
tMax = 1e5
xMax =20
lockDB = False
replicate = 1

def FirstGen():
    conn = sqlite3.connect(parametersName)
    c = conn.cursor()
    c.execute('''CREATE TABLE parameters (id text,  
                                          N integer, dx real,dt real,
                                          theta0 real,
                                          nElements integer,
                                          growth text, growthRate real, growthZone real, 
                                          tropismIntensity real, tropismDirection real, 
                                          apicalTropismIntensity real,apicalTropismDirection real,
                                          collectiveTropism text,
                                          collectiveTropismAttractionZone real,collectiveTropismRepulsionZone real,
                                          collectiveTropismAttractionIntensity real,collectiveTropismRepulsionIntensity real,
                                          proprioception real)''')
    conn.commit()
    conn.close()
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('''CREATE TABLE simulation (id text, repId text,date text,
                                          N integer, dx real,dt real,
                                          theta0 real,
                                          nElements integer,
                                          growth text, growthRate real, growthZone real, 
                                          tropismIntensity real, tropismDirection real, 
                                          apicalTropismIntensity real,apicalTropismDirection real,
                                          collectiveTropism text,
                                          collectiveTropismAttractionZone real,collectiveTropismRepulsionZone real,
                                          collectiveTropismAttractionIntensity real,collectiveTropismRepulsionIntensity real,
                                          proprioception real)''')
    conn.commit()
    conn.close()

def SecondGen():
    conn = sqlite3.connect(dbVideo)
    c = conn.cursor()
    c.execute('''CREATE TABLE video (id text, url text)''')
    conn.commit()
    conn.close()

def dbFiller():
    xMax = 20
    v0 =1
    Nrange=[2,5,10,20,50]
    
    dt = 0.01
    dxRange = [0,0.1,0.2,0.5,1.0,2.0]
    tMax =1e5   
    theta0Range = [0]
    nElementsRange = [1000]

    growthRange = ['None','Apical','Exponential']

    growthZones = [1.0]
    growthRates = [1.0]
    
    tropismRange = [0]
    tropismDirections = [0]
    apicalTropismRange = -np.array([0,1.0,10.0])
    apicalTropismDirections = [0]
    proprioceptionRange = -np.array([0,1.0,10.0])
    collectiveTropisms = ['Apical']
    collectiveTropismAttractionZoneRange = -np.array([0,1.0,10.0])
    collectiveTropismRepulsionZoneRange = -np.array([0,1.0,10.0])
    collectiveTropismAttractionIntensityRange = -np.array([0,1.0,10.0])
    collectiveTropismRepulsionIntensityRange = -np.array([0,1.0,10.0])




    conn = sqlite3.connect(parametersName)
    c = conn.cursor()
    for N in Nrange:
        for nElements in nElementsRange:
            for theta0 in theta0Range:
                for dx in dxRange:
                    for growth in growthRange:
                        for growthZone in growthZones:
                            for growthRate in growthRates:
                                for tropism in tropismRange:
                                    for tropismDirection in tropismDirections:
                                        for apicalTropism in apicalTropismRange:
                                            for apicalTropismDirection in apicalTropismDirections:
                                                for proprioception in proprioceptionRange:
                                                    for collectiveTropism in collectiveTropisms:
                                                        for collectiveTropismIntensity in collectiveTropismRange:

                                                            expId = str(uuid.uuid4())
                                                            values = [expId,N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropism,tropismDirection,apicalTropism,apicalTropismDirection,collectiveTropism,collectiveTropismIntensity,proprioception]
                                    
                                                            c.execute("INSERT INTO parameters VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
    conn.commit()
    conn.close()






def checkExpParam(expId):
    connParam = sqlite3.connect(parametersName, check_same_thread=False)
    cursorParam = connParam.cursor()


    cursorParam.execute("Select N from parameters where id = ?",(expId,))
    N  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select dx from parameters where id = ?",(expId,))
    dx  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select dt from parameters where id = ?",(expId,))
    dt  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select nElements from parameters where id = ?",(expId,))
    nElements  = (cursorParam.fetchall())[0][0]

    cursorParam.execute("Select growth from parameters where id = ?",(expId,))
    growth  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select growthRate from parameters where id = ?",(expId,))
    growthRate  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select growthZone from parameters where id = ?",(expId,))
    growthZone  = (cursorParam.fetchall())[0][0]
    
    cursorParam.execute("Select tropismIntensity from parameters where id = ?",(expId,))
    tropismIntensity  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select tropismDirection from parameters where id = ?",(expId,))
    tropismDirection  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select apicalTropismIntensity from parameters where id = ?",(expId,))
    apicalTropismIntensity  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select apicalTropismDirection from parameters where id = ?",(expId,))
    apicalTropismDirection  = (cursorParam.fetchall())[0][0]

    cursorParam.execute("Select collectiveTropismIntensity from parameters where id = ?",(expId,))
    collectiveTropismIntensity  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select collectiveTropism from parameters where id = ?",(expId,))
    collectiveTropism  = (cursorParam.fetchall())[0][0]

    cursorParam.execute("Select proprioception from parameters where id = ?",(expId,))
    proprioceptionIntensity  = (cursorParam.fetchall())[0][0]




    
    connParam.close()

    return N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropismIntensity , tropismDirection , apicalTropismIntensity ,apicalTropismDirection , collectiveTropism ,collectiveTropismIntensity ,proprioception 


def rootsSim(N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropismIntensity , tropismDirection , apicalTropismIntensity ,apicalTropismDirection , collectiveTropism ,collectiveTropismIntensity ,expId)
    roots = pk.Roots(N,dx,theta0 =theta0,growth=growth,nElements = nElements,,dt=dt,growthRate=growthRate,growthZone = growthZone)
        
    roots.addInteractions(name = 'ApicalTropism' ,intensity=apicalTropismIntensity,direction = apicalTropismDirection)
    roots.addInteractions(name = 'Tropism' ,intensity=tropismIntensity,direction = tropismDirection)
    roots.addInteractions(name = 'Proprioception' ,intensity=proprioception)

    roots.addCollectiveInteraction(name =collectiveTropism,)


def startSimulation(expId):
    global lockDB
    try:
        print("The following experiment is analyzed : "+str(expId[0]))
        print("The following replicate is analyzed  : "+str(expId[1]))
        #expId = str(uuid.uuid4())
        #values = [expId,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),N,nPhi,dt,v0,drag,Vuu,Vpp,Vzz,Vu,Vp,Vz,dVu,dVp,dVz]
                            
        #c.execute("INSERT INTO simulation VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)

        time.sleep(random.random())
        N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropismIntensity , tropismDirection , apicalTropismIntensity ,apicalTropismDirection , collectiveTropism ,collectiveTropismIntensity ,proprioception = checkExpParam(expId[0])
        print([checkExpParam(expId[0])])
        rootsSim(N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropismIntensity , tropismDirection , apicalTropismIntensity ,apicalTropismDirection , collectiveTropism ,collectiveTropismIntensity ,expId)


        while lockDB:
            time.sleep(random.random())
        lockDB = True
        conn = sqlite3.connect(dbName, check_same_thread=False)
        c = conn.cursor()
        
        values = [expId[0],expId[1],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropism,tropismDirection,apicalTropism,apicalTropismDirection,collectiveTropism,collectiveTropismIntensity,proprioception]
        print('----- writing in database')                    
        c.execute("INSERT INTO simulation VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
        conn.commit()
        conn.close()
        print('----- wrote in database')    
        lockDB = False
    except ValueError:
        print(ValueError)


def main():
    print('Starting')

    connParam = sqlite3.connect(parametersName, check_same_thread=False)
    cursorParam = connParam.cursor()
    cursorParam.execute("Select id from parameters")
    expIds=cursorParam.fetchall()
    
    connSim = sqlite3.connect(dbName, check_same_thread=False)
    cursorSim = connSim.cursor()
    parametersList = []




    print('checking the ids')
    running= True
    exp=0
    print('making ' +str(replicate)+' replicates')
    for expId in expIds:
        #print('is the experiment '+expId[0]+' already analyzed ?')
        
        cursorSim.execute("Select * from simulation where id = ?",(str(expId[0]),))
        n=len(cursorSim.fetchall())
        
        k=0
        while n+k<replicate:
            
            k=k+1
            #print('No')
            repId = str(uuid.uuid4())
            parametersList.append([expId[0],repId])
            exp =exp+1

    print('experiments type : '+str(len(expIds)))
    print('experiments todo : '+str(len(expIds)*replicate))
    print('experiments left : '+str(exp))
                

    connParam.close()
    connSim.close()  
    if threaded:
    

        pool = multiprocessing.Pool(processes=nThreads)
        pool.map_async(startSimulation, parametersList)
        pool.close()
        pool.join()
    else:
        for parmater in parametersList:
            startSimulation(parmater)
    

if __name__ == "__main__":
    main()



