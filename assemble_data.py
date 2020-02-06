import numpy as np
import pandas as pd

with open('./productions/mmpbsa_all_frames/frame_energies.csv','r') as f:
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

distances = pd.read_csv('./productions/binding_site_distance_all.dat', nrows=len(energies))
distances['energy'] = energies

distances.to_csv('training_data_distances_all.csv')

