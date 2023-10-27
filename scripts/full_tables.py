#!bin/bash

#This is a python script to go through all files in a dir and for each species, make individual .fa files for each busco gene
#---------------------------------------------------------------------------------------------------------------------------------
import os
import subprocess
#---------------------------------------------------------------------------------------------------------------------------------

pattern = '.TransPi.bus4.tsv'
pattern2 = '.Trinity.bus4.tsv'
patterns = [pattern, pattern2]
search_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/full_tables'
fasta_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/Cnidaria/'
output_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/full_tables_output'

i=0
while i < len(patterns):
    for f in os.listdir(search_dir):
        if patterns[i] in f:
            #print(f'{f}  {patterns[i]}')
            file_basename = f.split('.')[0][11:]
            print(file_basename)
            with open(search_dir + '/' + f, 'r') as file:
                sequence = busco_id = ''
                for num, line in enumerate(file):
                    if num < 3:
                        continue
                    line = line.strip().split('\t')
                    #print(line)
                    busco_id = line[0]
                    #print(busco_id)
                    if(len(line) > 2):
                        sequence = line[2]
                        #print(sequence)
                    if i == 0:
                        grep_cmd = f'grep {sequence} {fasta_dir}{file_basename}/evigene/{file_basename}.combined.okay.fa'
                    else:
                        grep_cmd = f'grep {sequence} {fasta_dir}{file_basename}/assemblies/{file_basename}.Trinity.fa'
                    
                    #TODO
                    #add split for assemblies + evigene
                    
                    if num == 4:
                        print(grep_cmd)
                    
                        result = subprocess.run([grep_cmd], shell=True, capture_output=True, text=True)
                        print(result.stdout)

                    
                    #make a new file for each busco gene
                    #with open ('output_dir' + busco_id + '.fa', 'w') as busco_fasta:
                    
        print()
    i+=1
    
    
    
