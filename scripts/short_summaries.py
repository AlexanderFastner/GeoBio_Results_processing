#!bin/bash

#This is a python script to go through all files in a dir and summarize the content in one large table
#Do for .Transpi.bus4.txt and for .Trinity.bus4.txt
#---------------------------------------------------------------------------------------------------------------------------------
import os
#---------------------------------------------------------------------------------------------------------------------------------

pattern = '.TransPi.bus4.txt'
pattern2 = '.Trinity.bus4.txt'
patterns = [pattern, pattern2]
outputs = ['TransPi.tsv','Trinity.tsv']
search_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/short_summaries'

for j, entry in enumerate(outputs):
    with open (entry, 'a') as out:
        out.write(f'species_name\tC\tS\tD\tF\tM\tTotal\n')
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