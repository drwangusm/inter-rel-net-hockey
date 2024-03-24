'''
read the skeleton file for validation set of fold 4 and see if there are 15 joints available for all the subset of data
'''

import numpy as np
import os

main_path = r"/demo/inter-rel-net-hockey/data/sbu"
# skl = np.loadtxt(main_path,delimiter=",")
# print('done')

for path, subdirs, files in os.walk(main_path):
    for name in files:
        if name == 'skeleton_pos.txt':
            filename = os.path.join(path, name)
            skl = np.loadtxt(filename,delimiter=",")
            if skl.shape[1] != 91:
                print(str(skl.shape), filename)

