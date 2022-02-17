#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:06:16 2022

@author: alumno
"""

from multiprocessing import Process, BoundedSemaphore
from multiprocessing import Value

N = 8


def task(common, tid, bsemaphore):  
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')       
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')   
        bsemaphore.acquire()
        try:
            print(f'{tid}−{i}: Critical section')    
            v = common.value + 1
            print(f'{tid}−{i}: Inside critical section')  
            common.value = v
            print(f'{tid}−{i}: End of critical section')     
        finally:
            bsemaphore.release()
        
def main(): 
    lp = []    
    common = Value('i', 0)   
    bsemaphore = BoundedSemaphore(1)
    for tid in range(N):     
        lp.append(Process(target=task, args=(common, tid, bsemaphore)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:      
        p.start()
    for p in lp:   
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")



if __name__ == "__main__": 
    main()