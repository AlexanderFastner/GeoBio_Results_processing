#A script to make a dict of species_name : phylum-class
#-------------------------------------------------------------------------------------------------------------------------------
import os
import pandas as pd
#-------------------------------------------------------------------------------------------------------------------------------

df = pd.read_csv('../CANTATA_species_WoRMS_matched.csv', header=0)
subset_df = df.iloc[:,[0,1,8,9]]
#add underline
subset_df.iloc[:, 0] = subset_df.iloc[:, 0].str.replace(' ', '_')
subset_df.columns = subset_df.columns.str.replace('\s+', '_', regex=True)
print(subset_df.columns)

data_dict = {}

# Iterate over each row in subset_df to populate the data_dict
for index, row in subset_df.iterrows():
    phylum_class = str(row['Phylum']) + '-' + str(row['Class'])
    species_name = row['CANTATA_name']

    if phylum_class not in data_dict:
        data_dict[phylum_class] = [species_name]
    else:
        data_dict[phylum_class].append(species_name)

#print(subset_df.columns)
for entry in data_dict.keys():
    #print(', '.join(data_dict.get(entry)))
    print(f'{{"label": "{entry}", "value": "{", ".join(data_dict.get(entry))}"}},')
#print(data_dict)
#-------------------------------------------------------------------------------------------------------------------------------