import time
from math import log
import sys
import ast
def createSemiPrimeSieve(n): 
  
    # Storing indices in each element of vector 

    v = [i for i in range(n + 1)] 
    countDivision = [2 for i in range(n + 1)] 
   
    print("-----------------------")
    squareSemis = []
    tim = time.perf_counter_ns()
    for i in range(2, n + 1, 1): 
        othercounter = 0
        if (v[i] == i and countDivision[i] == 2):
            tom = time.perf_counter_ns()
            dur = tom-tim
            if (dur > 10**9): # x seconds
                print("i at %d, counter at %d, approx. %0.3f%% done"%(i,othercounter,log(i)/log(n+1)))
                tim = tom
            sq = i*i
            if sq < n+1:
                squareSemis.append(sq)
            for j in range(2 * i, n + 1, i): 
                othercounter+=1
                if (countDivision[j] > 0): 
                    v[j] = int(v[j] / i) 
                    countDivision[j] -= 1
    print("-----------------------")
    # A new vector to store all Semi Primes 
        
    index = 0
    res = [] 
    for i in range(2, n + 1, 1): 
        if(index<len(squareSemis) and i == squareSemis[index]):
            res.append(i)
            index+=1
        if (v[i] == 1 and countDivision[i] == 0): 
            res.append(i) 
    return res 


def storeIntsAsBits(nums):
    filename ='semiprimes/'+str(nums[-1])+'.txt'
    with open(filename,'w') as out:
        index=0
        for k in range(nums[-1]+1):
            if k % 10000000 == 0: print ("STORING %d out of %d" % (k,nums[-1]+1))

            if k == nums[index]:
                out.write('1')
                index+=1
            else:
                out.write('0')
    return filename

def encode(bin_string):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    # Split the string of 1s and 0s into lengths of 6.
    chunks = [bin_string[i:i+6] for i in range(0, len(bin_string), 6)]
    # Store the length of the last chunk so that we can add that as the last bit
    # of data so that we know how much to pad the last chunk when decoding.
    last_chunk_length = len(chunks[-1])
    # Convert each chunk from binary into a decimal
    decimals = [int(chunk, 2) for chunk in chunks]
    # Add the length of our last chunk to our list of decimals.
    decimals.append(last_chunk_length)
    # Produce an ascii string by using each decimal as an index of our charset.
    ascii_string = ''.join([charset[i] for i in decimals])

    return ascii_string

def decode(ascii_string):
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    # Convert each character to a decimal using its index in the charset.
    decimals = [charset.index(char) for char in ascii_string]
    # Take last decimal which is the final chunk length, and the second to last
    # decimal which is the final chunk, and keep them for later to be padded
    # appropriately and appended.
    last_chunk_length, last_decimal = decimals.pop(-1), decimals.pop(-1)
    # Take each decimal, convert it to a binary string (removing the 0b from the
    # beginning, and pad it to 6 digits long.
    bin_string = ''.join([bin(decimal)[2:].zfill(6) for decimal in decimals])
    # Add the last decimal converted to binary padded to the appropriate length
    bin_string += bin(last_decimal)[2:].zfill(last_chunk_length)

    return bin_string

def convertToHex(fileIn,fileOut):
    with open(fileIn) as fin:
        with open(fileOut,'w') as fout:
            while True:
                data = fin.read()
                if not data:
                    print("End of file")
                    break
                bin_int = int(data,16)
                fout.write(str(bin_int))


# Driver code 
if __name__ == '__main__': 
    n = 2**29

    if len(sys.argv)>1:
        n = ast.literal_eval(sys.argv[1])
    tic = time.perf_counter()
    semiPrime = createSemiPrimeSieve(n)
    tac = time.perf_counter()
    p1Time = tac - tic
    print("created %d sieve in %0.4f seconds" %(n,p1Time))

    filename = storeIntsAsBits(semiPrime) 
    toc = time.perf_counter()
    print("part2:",toc-tac)
    print("Took a total of %0.4f seconds"%(toc-tic))


    # # Print all semi-primes 
    # for i in range(len(semiPrime)): 
    #     print(semiPrime[i], end = " ") 
    with open(filename,"r") as fin:
        encoded =  encode(fin.read())
        with open(filename+"-encoded.txt","w") as fout:
            fout.write(encoded)
