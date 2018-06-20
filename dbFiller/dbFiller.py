
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
                                          tropism text, collectiveTropism text)''')
    conn.commit()
    conn.close()
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('''CREATE TABLE simulation (id text, repId text,date text,
                                          N integer, dx real,dt real,
                                          theta0 real,
                                          nElements integer,
                                          growth text, growthRate real, growthZone real, 
                                          tropism text, collectiveTropism text)''')
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
    Nrange=[2,3,4,5,10,20]
    drag = 0.1
    dt = 0.01

    tMax =1e5   

    nPhiRange = [256]

    VuRange=-np.array([0.5,1.0,2])
    VpRange=-np.array([0.5,1.0,2])
    VzRange=-np.array([0.5,1.0,2])
    dVuRange= [0.05, .1,0.2]
    dVpRange= [0.05, .1,0.2]
    dVzRange= [0.05, .1,0.2]

    VuuRange = [1.0]
    VppRange = [1.0]
    VzzRange = [1.0]
    conn = sqlite3.connect(parametersName)
    c = conn.cursor()
    for N in Nrange:
        for nPhi in nPhiRange:
            for Vu in VuRange:
                for Vp in VpRange:
                    for Vz in VzRange:
                        for dVu in dVuRange:
                            for dVp in dVpRange:
                                for dVz in dVzRange: 
                                    for Vuu in VuuRange:
                                        for Vpp in VppRange:
                                            for Vzz in VzzRange:
                                                expId = str(uuid.uuid4())
                                                values = [expId,N,nPhi,dt,v0,drag,Vuu,Vpp,Vzz,Vu,Vp,Vz,dVu,dVp,dVz]
                        
                                                c.execute("INSERT INTO parameters VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
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
    
    cursorParam.execute("Select tropism from parameters where id = ?",(expId,))
    tropism  = eval((cursorParam.fetchall())[0][0])
    cursorParam.execute("Select collectiveTropism from parameters where id = ?",(expId,))
    collectiveTropism  = eval((cursorParam.fetchall())[0][0])
    cursorParam.execute("Select Vp from parameters where id = ?",(expId,))
    Vp  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select Vz from parameters where id = ?",(expId,))
    Vz  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select dVu from parameters where id = ?",(expId,))
    dVu  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select dVp from parameters where id = ?",(expId,))
    dVp  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select dVz from parameters where id = ?",(expId,))
    dVz  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select Vuu from parameters where id = ?",(expId,))
    Vuu  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select Vpp from parameters where id = ?",(expId,))
    Vpp  = (cursorParam.fetchall())[0][0]
    cursorParam.execute("Select Vzz from parameters where id = ?",(expId,))
    Vzz  = (cursorParam.fetchall())[0][0]





    
    connParam.close()

    return N,dx,dt,theta0,nElements,growth,growthRate,growthZone,tropism,collectiveTropism


def startSimulation(expId):
    global lockDB
    try:
        print("The following experiment is analyzed : "+str(expId[0]))
        print("The following replicate is analyzed  : "+str(expId[1]))
        #expId = str(uuid.uuid4())
        #values = [expId,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),N,nPhi,dt,v0,drag,Vuu,Vpp,Vzz,Vu,Vp,Vz,dVu,dVp,dVz]
                            
        #c.execute("INSERT INTO simulation VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)

        time.sleep(random.random())
        N,nPhi,v0,Vu,Vp,Vz,dVu,dVp,dVz,Vuu,Vpp,Vzz,drag,dt = checkExpParam(expId[0])
        print([checkExpParam(expId[0])])
        
        vs.visModel2d(N,xMax,nPhi,v0,Vu,Vp,Vz,dVu,dVp,dVz,Vuu,Vpp,Vzz,drag,dt,tMax =tMax,expId=expId[1])
        
        while lockDB:
            time.sleep(random.random())
        lockDB = True
        conn = sqlite3.connect(dbName, check_same_thread=False)
        c = conn.cursor()
        
        values = [expId[0],expId[1],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),N,nPhi,dt,v0,drag,Vuu,Vpp,Vzz,Vu,Vp,Vz,dVu,dVp,dVz]
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



