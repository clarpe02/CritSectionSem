"""
Created on Thu Feb 24 10:10:01 2022

@author: CLARA PÉREZ ESTEBAN
"""

from multiprocessing import Process
from multiprocessing import Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 10
NPROD = 5
NCONS = 1


def delay(factor = 3):
    sleep(random()/factor)
       
        
def producer(storage,last, empty_array, non_empty_array):
    for v in range(N):
        pid = int(current_process().name.split('_')[1])
        empty_array[pid].acquire()
        print (f"producer {current_process().name} produciendo")
        delay(6)
        storage[pid] = last[pid] + randint(0,5)
        last[pid] = storage[pid]
        delay(6)
        non_empty_array[pid].release()
        print (f"producer {current_process().name} almacenado {storage[pid]}")
    empty_array[pid].acquire()
    storage[pid] = -1
    non_empty_array[pid].release()


def consumer(storage, empty_array, non_empty_array):
    for i in range(NPROD):# espera a que todos hayan producido
        non_empty_array[i].acquire()
    l = [] #lista con elementos consumidos
    while ([-1 for i in range (NPROD)])!= [storage[i] for i in range (NPROD)]:
        for i in range (NPROD):
            if storage[i] != -1:
                j = storage[i]
                pos = i
                break
        for n in range(NPROD-1):
            if j > storage[n+1] and storage[n+1]!=-1:
                j = storage[n+1]
                pos = n+1       
        print (f"consumer consumiendo {j}")
        l.append(j)
        empty_array[pos].release()
        delay(6)
        non_empty_array[pos].acquire()
    print ("elementos consumidos: "+str(l))

        

def main():
    storage = Array('i', NPROD)
    last = Array('i', NPROD)
    for i in range(NPROD):
        storage[i] = 0
        last[i] = 0
    print ("almacen inicial", storage[:])
    
    non_empty_array = [Semaphore(0) for i in range(NPROD)]
    empty_array = [Lock() for i in range(NPROD)]

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(storage,last, empty_array, non_empty_array))
                for i in range(NPROD) ]

    conslst = [Process(target=consumer,
                      name=f"cons",
                      args=(storage, empty_array, non_empty_array))]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

if __name__ == '__main__':
    main()
