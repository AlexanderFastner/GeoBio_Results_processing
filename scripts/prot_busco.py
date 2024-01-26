#!bin/bash

# A python script to:
# take all the busco protein files from input dir,
# get all busco genes (proteins),
# seperate them into dir for each species



# TODO
# No split for trinity and transpi
# all pep files
# adapt dir structure
                        
#-------------------------------------------------------------------------------------------------------------------------------
import os
import subprocess
#-------------------------------------------------------------------------------------------------------------------------------
# To run change the fasta (search) and output dirs
fasta_dir = '/netvolumes/srva229/molpal/Members/Alexander/Proteomes'
output_dir = '/netvolumes/srva229/molpal/Members/Alexander/prot_BUSCO_out/'
#-------------------------------------------------------------------------------------------------------------------------------
pattern = 'single_copy_busco_sequences'
#-------------------------------------------------------------------------------------------------------------------------------
#reset out_dir
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
else:
    os.chdir(f'{output_dir}..')
    cmd = f'rm -rf {output_dir}'
    subprocess.run([cmd], shell=True, capture_output=True, text=True)
    os.mkdir(output_dir)
    os.mkdir(f'{output_dir}')

#create dir inside out_dir
for d in os.listdir(fasta_dir):
    if os.path.isdir(d):
        #print(d)
        path = output_dir + d
        #print(path)
        if not os.path.isdir(path):
            #os.mkdir(path)
            print(path)
        
#-------------------------------------------------------------------------------------------------------------------------------



# for single copy only
# combine all data for each busco from each species
# result should be a dir containing files for each busco gene, with each entry from the single files catted together


#-------------------------------------------------------------------------------------------------------------------------------













