#!bin/bash
#-------------------------------------------------------------------------------------------------------------------------------
#This is a python script to go through all files in a dir and for each species, make individual .fa files for each busco gene
#For this file lauch 2 subprocesses, 1 for Trinity, 1 for Transpi  
            #both need a file containing sequence ($2) of the things we are grepping for 
            #Trinity needs a single line, get all headers and sequences at the same time
                #Then seperate the returned output into header, sequence pairs
                    #Then write a file with that sequence and header
            #Transpi make a new non-multiline temp fasta file
                #needs a ready made list of things to grep for
                    #Then seperate the returned output into header, sequence pairs
                        #Then write a file with that sequence and header
                        #rm tmp file
#-------------------------------------------------------------------------------------------------------------------------------
import os
import subprocess
#-------------------------------------------------------------------------------------------------------------------------------
pattern = '.TransPi.bus4.tsv'
pattern2 = '.Trinity.bus4.tsv'
patterns = [pattern, pattern2]
search_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/full_tables'
fasta_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/Cnidaria/'
output_dir = '/netvolumes/srva229/molpal/hpc_exchange/Alex/GeoBio_Results_processing/full_tables_output/'
#-------------------------------------------------------------------------------------------------------------------------------
#reset out_dir
cmd = f'rm {output_dir}*'
subprocess.run([cmd], shell=True, capture_output=True, text=True)

#create dirs inside out_dir
for d in os.listdir(fasta_dir):
    #print(d)
    path = output_dir + d
    #print(path)
    if not os.path.isdir(path):
        os.mkdir(path)
        os.mkdir(path+'/assemblies')
        os.mkdir(path+'/evigene')

#-------------------------------------------------------------------------------------------------------------------------------
i=0
while i < len(patterns):
    for f in os.listdir(search_dir):
        if patterns[i] in f:
            print(f)
            file_basename = f.split('.')[0][11:]
            #print(file_basename)
            
            #make a list of things to be grepped for
            with open(f'./grep_search_{file_basename}{patterns[i]}', 'w') as grep_file:
                with open(search_dir + '/' + f, 'r') as file:
                    sequence = 'Missing!'
                    busco_id = ''
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
                        grep_file.write(f'{busco_id}\t{sequence}\n')
                        

            #TransPi
            if i == 0:
                #print(f'{fasta_dir}{file_basename}/evigene/{file_basename}.combined.okay.fa')
                
                transcriptome_to_fix = f'{fasta_dir}{file_basename}/evigene/{file_basename}.combined.okay.fa'
                
                awk = f'awk \'{{ if($1 ~ />/){{ print $0 }} else{{ gsub(/{chr(92)}n$/,\"\"); printf "%s", $0 }}}}\' {transcriptome_to_fix} | sed \'s/>/{chr(92)}n>/g\' > {transcriptome_to_fix}_single_line.tmp'
                
                subprocess.run([awk], shell=True, capture_output=True, text=True)
                
                with open(f'./grep_search_{file_basename}.TransPi.bus4.tsv', 'r') as grep:
                    for line in grep:
                        split_line = line.strip('\n').split('\t')
                        seq = split_line[1]
                        busco = split_line[0]
                        if 'Missing!' not in seq:
                            grep_cmd = f'grep {seq} -A 1 --no-group-separator {transcriptome_to_fix}_single_line.tmp'
                            #print(grep_cmd)
                            result = subprocess.run([grep_cmd], shell=True, capture_output=True, text=True).stdout.split('\n')
                            header = result[0]
                            sequence = result[1]
                            with open(output_dir + file_basename + '/evigene/' + busco + '.fa', 'a') as busco_new:
                                busco_new.write(f'{header}\n')
                                busco_new.write(f'{sequence}\n')
                                    
                                
                #remove tmp file
                remove_tmp = f'rm {transcriptome_to_fix}_single_line.tmp'
                subprocess.run([remove_tmp], shell=True, capture_output=True, text=True)
                print(f'finished Transpi {file_basename}')

                
            #Trinity
            else:
                with open(f'./grep_search_{file_basename}.Trinity.bus4.tsv', 'r') as grep:
                    for line in grep:
                        split_line = line.strip('\n').split('\t')
                        seq = split_line[1]
                        busco = split_line[0]
                        if 'Missing!' not in seq:
                            grep_cmd = f'grep {seq} -A 1 --no-group-separator {fasta_dir}{file_basename}/assemblies/{file_basename}.Trinity.fa'
                            #print(grep_cmd)
                            result = subprocess.run([grep_cmd], shell=True, capture_output=True, text=True).stdout.split('\n')
                            header = result[0]
                            sequence = result[1]
                            with open(output_dir + file_basename + '/assemblies/' + busco + '.fa', 'a') as busco_new:
                                busco_new.write(f'{header}\n')
                                busco_new.write(f'{sequence}\n')
                print(f'finished Trinity {file_basename}')

                    
        print()
    i+=1
#-------------------------------------------------------------------------------------------------------------------------------    
    