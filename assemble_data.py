#! /usr/bin/env python

# Copyright (c) 2020 Martin Rosellen

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import sys

import numpy as np
import pandas as pd


def main(args):
    parser = argparse.ArgumentParser(description='Merge feature data with target data. The target is in the first '
                                                 'column.')
    parser.add_argument('feature_data', nargs='?', help='name of cpptraj generated .dat file holding the feature data',
                        default="bsite_features.dat")
    parser.add_argument('target_data', nargs='?', help='name of .csv file holding the target data',
                        default="frame_energies.csv")
    parser.add_argument('output', nargs='?', help='name of the training data csv', default="training_data.csv")

    args = parser.parse_args()

    # read in MMGBSA Delta G values
    with open('frame_energies_all.csv', 'r') as f:
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
    metrics = pd.read_csv('bsite_features.dat', nrows=len(energies), header=0, delim_whitespace=True)

    # overwrite the first line of the cpptraj data frame with energy values
    metrics['#Frame'] = energies
    # rename first column to energies (not really necessary since column headers are not part of the training data file)
    metrics.rename(columns={'#Frame': 'energies'}, inplace=True)

    metrics.to_csv('training_data_WT_cs25.csv', sep=',', header=None, index=None)


if __name__ == '__main__':
    main(sys.argv)
