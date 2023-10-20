#!bin/bash

#This is a python script to go through all files in a dir and for each species, make individual .fa files for each busco gene
#---------------------------------------------------------------------------------------------------------------------------------
import os
#---------------------------------------------------------------------------------------------------------------------------------

pattern = '.TransPi.bus4.tsv'
pattern2 = '.Trinity.bus4.tsv'
patterns = [pattern, pattern2]
search_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/full_tables'
output_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/full_tables_output'

i=0
while i < len(patterns):
    for f in os.listdir(search_dir):
        if patterns[i] in f:
            print(f)
            with open(search_dir + '/' + f, 'r') as file:
                for line in file:
                    print(line.strip())
        print()
    i+=1
