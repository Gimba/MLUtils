#! /usr/bin/env python

import sys

import numpy as np
import pandas as pd


def main(args):
    # read in MMGBSA Delta G values
    with open('./frame_energies_all.csv', 'r') as f:
        energies = []

        # flag used to start reading in line data
        flag = False
        for line in f.readlines():
            # Delta G values begin after the first occurence of DELTA
            if 'DELTA' in line:
                flag = True
                # skip the next line since it is also a header
                continue
            if flag:
                line = line.split(',')
                # since Delta G values are the last element of the line they also contain the new line character which
                # gets removed here
                line = [ll.replace('\n', '') for ll in line]
                if len(line) > 1:
                    energies.append(line[-1])

    energies = np.asarray(energies)

    # read in as many lines from the cpptraj generated file as there are values in energies
    metrics = pd.read_csv('bindingsite_metrics.dat', nrows=len(energies), header=0, delim_whitespace=True)

    # overwrite the first line of the cpptraj data frame with energy values
    metrics['#Frame'] = energies
    # rename first column to energies (not really necessary since column headers are not part of the training data file)
    metrics.rename(columns={'#Frame': 'energies'}, inplace=True)

    metrics.to_csv('training_data_WT_cs25.csv', sep=',', header=None, index=None)


if __name__ == '__main__':
    main(sys.argv)
