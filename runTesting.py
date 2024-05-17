import testing
import json
import logging
import time


def main():
    MAX_NUM = 2**29
    threads = 8
    n = int(MAX_NUM/threads)
    max_int_in_file = 1000
    max_int_in_summary = 15
    tic = time.perf_counter()

    nums=testing.parallelRun(n,threads)
    partitionPrint(nums, n, threads,max_int_in_file,max_int_in_summary)
    # simplePrint(nums,n,threads)
    toc = time.perf_counter()
    print("time elapsed (in seconds):",toc-tic)

    
def simplePrint(nums,n,threads):
    with open("results/blah/real-"+str(n*threads)+".json", 'w') as outfile:
        outfile.write("results:")
        for key in sorted(nums):
            outfile.write("\n %s: #=%s: \n\t"% (key, len(nums[key])))
            json.dump(nums[key], outfile,sort_keys=True)
            


def partitionPrint(nums,n, threads, max_int_in_file, max_int_in_summary):
    with open("results/partitioned/"+ str(n*threads)+"-encoded-summary.txt", 'w') as summary: 
        for key in sorted(nums):
            distance = int(key[0:-1])*int(key[0:-1])
            message = "There are %d numbers that are %d^2 (%d) distance away:" % (len(nums[key]), int(key[0:-1]),distance)
            summary.write(message+'\n')
            with open("results/partitioned/"+ str(n*threads)+"-"+str(key)+"encoded.json", 'w') as outfile:
                outfile.write(message+'\n')
                print(message)

                if len(nums[key])<max_int_in_summary:
                    print('\t',nums[key],'\n')
                    summary.write(" |____"+ "".join(str(nums[key]))+"\n")
                    json.dump(nums[key], outfile,sort_keys=True)
                elif len(nums[key])<max_int_in_file:
                    print("\\ These are the first %d:"%(max_int_in_summary))
                    print('\t',nums[key][:max_int_in_summary],'\n')
                    outfile.write(" |____"+ "".join(str(nums[key]))+"\n")
                    summary.write("\\ These are the first %d:\n"%(max_int_in_summary))
                    summary.write(" |____"+ "".join(str(nums[key][:max_int_in_summary]))+"\n")

                else:
                    print("\\ These are the first %d:"%(max_int_in_summary))
                    print('\t',nums[key][:max_int_in_summary],'\n')
                    outfile.write("\\ These are the first %d:\n"%(max_int_in_file))
                    outfile.write("|____"+ "".join(str(nums[key][:max_int_in_summary]))+"\n")
                    summary.write("\\ These are the first %d:\n"%(max_int_in_summary))
                    summary.write(" |____"+ "".join(str(nums[key][:max_int_in_summary]))+"\n")



if __name__ == "__main__":
    main()