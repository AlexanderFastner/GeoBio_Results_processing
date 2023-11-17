#!bin/bash

#This is a python script to go through all files in a dir and summarize the content in one large table
#Do for .Transpi.bus4.txt and for .Trinity.bus4.txt
#-------------------------------------------------------------------------------------------------------------------------------
import os
import typer
from typing_extensions import Annotated
#-------------------------------------------------------------------------------------------------------------------------------
app = typer.Typer()

@app.command()
def main(file_list: Annotated[str, typer.Argument()] = '',
         search_dir_in: Annotated[str, typer.Argument()] = '../short_summaries'
        
        ):
    """
    Python script to go through all files in a dir and summarize the content in one large table
    Default is ../short_summaries
    """    

    pattern = '.TransPi.bus4.txt'
    pattern2 = '.Trinity.bus4.txt'
    patterns = [pattern, pattern2]
    outputs = ['TransPi.tsv','Trinity.tsv']
    search_dir = search_dir_in
    out_dir = '../short_summaries_results'
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
        
#-------------------------------------------------------------------------------------------------------------------------------
    #TODO replace search dir with inputted

    def make_file_list(given_list):
        for j, entry in enumerate(outputs):
            with open (f'{out_dir}/{entry}', 'w') as out:
                out.write(f'species_name\tComplete_BUSCOs\tComplete_&_single-copy\tComplete_&_duplicated\tFragmented\tMissing\tTotal\n')
                for f in os.listdir(search_dir):
                    base_name = f.split('.')[3].strip()
                    #if on the list
                    if (len(given_list) > 1):
#                         print(given_list)
#                         print()
#                         print(base_name)
                        if base_name in given_list:
                            if patterns[j] in f:
                                print(base_name)
                                with open(search_dir + '/' + f, 'r') as file:
                                    species_name = ''
                                    c = s = d = f = m = total = 0
                                    for i, line in enumerate(file):
                                        #print(i)
                                        line = line.strip()
                                        #print(line)
                                        if i == 2:
                                            sub = line.split(' ')
                                            species_name = str(sub[-1:][0]).split('.')[0]
                                        if i == 8:
                                            c = line.split('\t')[0]
                                        if i == 9:
                                            s = line.split('\t')[0]
                                        if i == 10:
                                            d = line.split('\t')[0]
                                        if i == 11:
                                            f = line.split('\t')[0]
                                        if i == 12:
                                            m = line.split('\t')[0]
                                        if i == 13:
                                            total = line.split('\t')[0]
                                out.write(f'{species_name}\t{c}\t{s}\t{d}\t{f}\t{m}\t{total}\n')
                    else:
                        print('list not long enough')
            out.close()

    def make_file():
        for j, entry in enumerate(outputs):
            with open (f'{out_dir}/{entry}', 'w') as out:
                out.write(f'species_name\tComplete_BUSCOs\tComplete_&_single-copy\tComplete_&_duplicated\tFragmented\tMissing\tTotal\n')                
                for f in os.listdir(search_dir):
                    if patterns[j] in f:
                        with open(search_dir + '/' + f, 'r') as file:
                            species_name = ''
                            c = s = d = f = m = total = 0
                            for i, line in enumerate(file):
                                #print(i)
                                line = line.strip()
                                #print(line)
                                if i == 2:
                                    sub = line.split(' ')
                                    species_name = str(sub[-1:][0]).split('.')[0]
                                if i == 8:
                                    c = line.split('\t')[0]
                                if i == 9:
                                    s = line.split('\t')[0]
                                if i == 10:
                                    d = line.split('\t')[0]
                                if i == 11:
                                    f = line.split('\t')[0]
                                if i == 12:
                                    m = line.split('\t')[0]
                                if i == 13:
                                    total = line.split('\t')[0]
                        out.write(f'{species_name}\t{c}\t{s}\t{d}\t{f}\t{m}\t{total}\n')
            out.close()
            
#------------------------------------------------------------------------------------------------------------------------------- 

    #if len(file_list) is not None:
    if len(file_list) > 1:
        species = []
        with open(file_list, 'r') as files:
            for line in files:
                print(f'line : {line}')
                species.append(line.strip())
        #go through all files in species
        make_file_list(species)

    else:
        #do for all in ../short_summaries
        make_file()
    
#-------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app()
#-------------------------------------------------------------------------------------------------------------------------------
