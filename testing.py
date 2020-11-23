from semiprimesieve import decode
import math 
from concurrent import futures
def traverse(n, m):
    found = True
    distanceMap = {} 
    delta = (m-n)
    numTab = int(n/delta)
    tab = "\t"*numTab
    
    if n <5:
        n=5
    is_semiprime_str = None
    with open("semiprimes/268435451-encoded.txt") as semis:
        temp = semis.read()
        if temp[0] == 'c':
            print("decoding ...")
            is_semiprime_str = decode(temp)
            print("decoded!")
        else:
            is_semiprime_str = temp
    for k in range(n,m):

        if k%1000000 ==0: print("%s SQUARED DISTANCE thread %d at %d of %d" % (tab,numTab, k,m))
        if found:
            found = False
        else:
            print("%d is not a squared distance from any semiprime"% (k-1))
            distanceMap.setdefault(format(-1,'03d')+"x",[]).append(k-1)
        for j in range(k):
            dsquare = j**2
            num = k - dsquare
            inum = k + dsquare
            # if num > 0 and checkSemiprime(num):
            try:
                if num > 0 and num < len(is_semiprime_str) and is_semiprime_str[num] == '1':
                    # print("%d is true for delta %d^2,%d" % (k,j,dsquare))
                    found = True
                    # print(" marking n as true:", k)
                    distanceMap.setdefault(format(j,'03d')+"r",[]).append(k)
                    break
            except IndexError:
                break
            # if num < len() and checkSemiprime(inum):
            #     # print("%d is true for delta %d^2,%d" % (k,j,dsquare))
            #     found = True
            #     # print(" marking n as true:", k)
            #     distanceMap.setdefault(format(j,'03d')+"i",[]).append(k)
            #     break

    return distanceMap

def multi_traverse(params):
     return traverse(*params)

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = (value) +dict1[key]
   return dict3


def parallelRun(n,threads):
    bounds = list(zip(range(0,(threads+1)*n,n)[:-1],range(0,(threads+1)*n,n)[1:]))
    # bounds = []
    # for k in range(threads):
    #     bounds.append((n, k, threads))

    all={} 
    with futures.ProcessPoolExecutor() as pool:
        for nums in pool.map(multi_traverse,bounds):
            all = mergeDict(nums, all)
    return all
