#!bin/bash

# Inputs: species list, busco list (default all)
# Output: heatmap of all 3 types of BUSCO genes                    
#-------------------------------------------------------------------------------------------------------------------------------
import os
import subprocess
import textwrap
import argparse 
#-------------------------------------------------------------------------------------------------------------------------------
search_dir = '/netvolumes/srva229/molpal/Members/Alexander/Proteomes/'
#-------------------------------------------------------------------------------------------------------------------------------
#Arg Parser
parser = argparse.ArgumentParser(
                    prog='prot_Busco',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description=textwrap.dedent('''
                    Inputs: 1. file containing a list of species (1 per line), default is all in search dir
                            2. busco list file (A file containing a list of Busco genes to include, default contains all)
                    Output: heatmap of all 3 types of BUSCO genes)''')
)

parser.add_argument('--species_list', type=str, nargs=1,
                    help='Path to a file containing a list of species (1 per line), default is all in search dir')
parser.add_argument('--busco_list', type=str, nargs='?',
                    help='Optional: A file containing a list of Busco genes to include, leave exmpty to default to all 954')

args = parser.parse_args()
print(args)
#-------------------------------------------------------------------------------------------------------------------------------
#read in arg files
species_list_path = args.species_list[0] if args.species_list else None
busco_list_path = args.busco_list if args.busco_list else "default"
search_species=[]
search_busco=[]

if species_list_path is not None:
    with open(species_list_path) as sl:
        for line in sl:
            search_species.append(line)
if busco_list_path != "default":
    with open(busco_list_path) as bl:
        for line in bl:
            search_busco.append(line)
            
print(search_species)
print()
print(search_busco)
            
#-------------------------------------------------------------------------------------------------------------------------------
#make a dict of busco name + fragmented/multi/single for each species
    #if not contained in any it is interpreted as missing later 
#add that dict to all_species
#a dictionary containing a dictionary of busco classification for each species
all_species={}

for species in os.listdir(search_dir):
    if species_list_path is not None: #check if species is in list
        if species in search_species:
            print(species)
            species_dict={}
            #fragmented/multi/single
            single=search_dir+species+'/run_metazoa_odb10/busco_sequences/single_copy_busco_sequences/'
            fragmented=search_dir+species+'/run_metazoa_odb10/busco_sequences/fragmented_busco_sequences/'
            multi=search_dir+species+'/run_metazoa_odb10/busco_sequences/multi_copy_busco_sequences/'

            for file in os.listdir(single):
                with open(single+file) as f:
                    busco=f.readline().strip().split()[0][1:]
                    species_dict[busco]='single'
            for file in os.listdir(fragmented):
                with open(fragmented+file) as f:
                    busco=f.readline().strip().split()[0][1:]
                    species_dict[busco]='fragmented'
            for file in os.listdir(multi):
                with open(multi+file) as f:
                    busco=f.readline().strip().split()[0][1:]
                    species_dict[busco]='multi'
            print(len(species_dict))
            all_species[species]=species_dict
print(len(all_species))    
#-------------------------------------------------------------------------------------------------------------------------------
#Plot













#-------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------



