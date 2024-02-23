#!bin/bash

# Inputs: species list, busco list (default all)
# Output: heatmap of all 3 types of BUSCO genes                    
#-------------------------------------------------------------------------------------------------------------------------------
import os
import subprocess
import textwrap
import argparse 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------------------------------------------------------------
#Arg Parser
parser = argparse.ArgumentParser(
                    prog='prot_Busco',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    description=textwrap.dedent('''
                    Inputs: 1. file containing a list of species (1 per line), default is all in search dir
                            2. busco list file (A file containing a list of Busco genes(no file endings) to include, default contains all)
                    Output: heatmap of all 3 types of BUSCO genes)''')
)

parser.add_argument('--species_list', type=str, nargs=1,
                    help='Path to a file containing a list of species (1 per line), default is all in search dir')
parser.add_argument('--busco_list', type=str, nargs='?',
                    help='Optional: A file containing a list of Busco genes to include, leave exmpty to default to all 954')
parser.add_argument('--search_dir', type=str, nargs='?',
                    help='Path to the head dir you want to search in')

args = parser.parse_args()
print(args)
#-------------------------------------------------------------------------------------------------------------------------------
#read in arg files
species_list_path = args.species_list[0] if args.species_list else None
busco_list_path = args.busco_list if args.busco_list else None
search_dir = args.search_dir if args.search_dir else '/netvolumes/srva229/molpal/Members/Alexander/Proteomes/'
search_species=None
search_busco=None

if species_list_path is not None:
    search_species=[]
    with open(species_list_path) as sl:
        for line in sl:
            search_species.append(line.strip())
if busco_list_path is not None:
    search_busco=[]
    with open(busco_list_path) as bl:
        for line in bl:
            search_busco.append(line[:line.index('.')].strip())
            
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
                file_name = file[:file.index('.')]
                if search_busco is not None:
                    if file_name in search_busco:
                        species_dict[file_name]='single'
                else:
                    species_dict[file_name]='single'
            for file in os.listdir(fragmented):
                file_name = file[:file.index('.')]
                if search_busco is not None:
                    if file_name in search_busco:
                        species_dict[file_name]='fragmented'
                else:
                    species_dict[file_name]='fragmented'
            for file in os.listdir(multi):
                file_name = file[:file.index('.')]
                if search_busco is not None:
                    if file_name in search_busco:
                        species_dict[file_name]='multi'
                else:
                    species_dict[file_name]='multi'
            print(len(species_dict))
            all_species[species]=species_dict
    else:
        print(species)
        species_dict={}
        #fragmented/multi/single
        single=search_dir+species+'/run_metazoa_odb10/busco_sequences/single_copy_busco_sequences/'
        fragmented=search_dir+species+'/run_metazoa_odb10/busco_sequences/fragmented_busco_sequences/'
        multi=search_dir+species+'/run_metazoa_odb10/busco_sequences/multi_copy_busco_sequences/'

        for file in os.listdir(single):
            file_name = file[:file.index('.')]
            if search_busco is not None:
                if file_name in search_busco:
                    species_dict[file_name]='single'
            else:
                species_dict[file_name]='single'
        for file in os.listdir(fragmented):
            file_name = file[:file.index('.')]
            if search_busco is not None:
                if file_name in search_busco:
                    species_dict[file_name]='fragmented'
            else:
                species_dict[file_name]='fragmented'
        for file in os.listdir(multi):
            file_name = file[:file.index('.')]
            if search_busco is not None:
                if file_name in search_busco:
                    species_dict[file_name]='multi'
            else:
                species_dict[file_name]='multi'
        print(len(species_dict))
        all_species[species]=species_dict
print(len(all_species))    
#-------------------------------------------------------------------------------------------------------------------------------
#data wrangling
df = pd.DataFrame(all_species).T.fillna('missing')
color_mapping = {'single': 0, 'fragmented': 1, 'multi': 2, 'missing' : 3}
df_mapped = df.replace(color_mapping)

#-------------------------------------------------------------------------------------------------------------------------------
#Plot
plt.figure(figsize=(300, 200))
cmap = sns.color_palette("deep", 4) 
ax = sns.heatmap(df_mapped, cmap=cmap, annot=False, cbar_kws={'ticks': [0, 1, 2], 'label': 'Busco Type'})
# modify colorbar:
colorbar = ax.collections[0].colorbar 
r = colorbar.vmax - colorbar.vmin 
colorbar.set_ticks([colorbar.vmin + r / 4 * (0.5 + i) for i in range(4)])
colorbar.set_ticklabels(list(color_mapping.keys()), rotation=0)    
ax.set_yticklabels(ax.get_yticklabels(), rotation='horizontal')
plt.title('Busco Type Heatmap')
plt.xlabel('Busco Genes')
plt.ylabel('Species')
plt.show()
#-------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------



