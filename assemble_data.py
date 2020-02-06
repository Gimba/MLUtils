#! /usr/bin/env python

import numpy as np
import pandas as pd

with open('./productions/frame_energies.csv','r') as f:
    energies = []
    flag = False
    for line in f.readlines():
        if 'DELTA' in line:
            flag = True
            continue
        if flag:
            line = line.split(',')
            line = [ll.replace('\n','') for ll in line]
            if len(line) > 1:
                energies.append(line[-1])

energies = np.asarray(energies)

distances = pd.read_csv('./productions/binding_site_distance_all.dat', nrows=len(energies), sep=r"\s+")
distances['energy'] = energies

column_titles = list(distances.columns)
column_titles[0] = column_titles[-1]
new_data = distances.reindex(columns=column_titles[:-1])
new_data = new_data.sample(frac=1)

new_data.to_csv('./productions/training_data_distances_all.csv', index=None, header=None)

