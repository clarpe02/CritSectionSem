"""
Created on Thu Mar  3 15:20:29 2022

@author: CLARA PÉREZ ESTEBAN
"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 10
NPROD = 5
NCONS = 1
k = 5 #capacidad del buffer


def delay(factor = 3):
    sleep(random()/factor)
       
        
def producer(storage,last, empty_array, non_empty_array,index):
    for v in range(N):
        pid = int(current_process().name.split('_')[1])
        empty_array[pid].acquire()
        print (f"producer {current_process().name} produciendo")
        delay(6)
        storage[index[pid]] = last[pid] + randint(0,5)
        last[pid] = storage[index[pid]]
        index[pid] += 1
        delay(6)
        non_empty_array[pid].release()
        print (f"producer {current_process().name} almacenado {storage[index[pid]-1]}")
    
    empty_array[pid].acquire()
    storage[k*pid+k-1] = -1
    non_empty_array[pid].release()
    

def consumer(storage, empty_array, non_empty_array,index):
    for i in range(NPROD): # espera a que todos hayan producido
        non_empty_array[i].acquire()
    l = [] #lista con elementos consumidos
    while ([-1 for i in range (NPROD*k)])!= [storage[i] for i in range (NPROD*k)]:
        lista_minimos = [storage[j*k] for j in range(NPROD)]
        for i in range (NPROD):
            if lista_minimos[i] != -1:
                j = lista_minimos[i]
                pos = i
                break
        for n in range(NPROD-1):
            if j > lista_minimos[n+1] and lista_minimos[n+1]!=-1:
                j = lista_minimos[n+1]
                pos = n+1    
        index[pos] = index[pos]-1
        for h in range(pos*k,pos*k+k-1):
            storage[h] = storage[h+1]
        if storage[pos*k+k-1] == -1:
            storage[pos*k+k-1] = -1
        else:
            storage[pos*k+k-1] = 0
        print (f"consumer consumiendo {j}")
        l.append(j)
        empty_array[pos].release()
        delay(6)
        non_empty_array[pos].acquire()
    print ("elementos consumidos: " + str(l))

        

def main():
    storage = Array('i', NPROD*k)
    last = Array('i', NPROD)#guarda el último elemento almacenado por cada productor
    index = Array('i',NPROD)#tendrá un número entre k*NPROD y k*NPROD+k-1 que indica posición en la que toca almacenar
    for i in range (NPROD):
        index[i] = i*k
        last[i] = 0
    for i in range(NPROD*k):
        storage[i] = 0
    print ("almacen inicial", storage[:])
    
    non_empty_array = [Semaphore(0) for i in range(NPROD)]
    empty_array = [BoundedSemaphore(k) for i in range(NPROD)]

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(storage,last, empty_array, non_empty_array, index))
                for i in range(NPROD) ]

    conslst = [Process(target=consumer,
                      name=f"cons",
                      args=(storage, empty_array, non_empty_array,index))]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

if __name__ == '__main__':
    main()
