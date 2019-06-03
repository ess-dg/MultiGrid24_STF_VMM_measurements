import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import struct
import re
import zipfile
import shutil
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import h5py


# =============================================================================
# IMPORT DATA
# =============================================================================


def import_data(file_path):
    h5_file = h5py.File(file_path, 'r')
    data = pd.DataFrame(h5_file['srs_hits'].value)
    return data

# =============================================================================
# CLUSTER DATA
# =============================================================================


def cluster_data(df_raw):
    # Declare parameters
    size = df_raw.shape[0]
    data_dict = {'indices': np.zeros([size], dtype=int),  # Clusters
                 'gCh': np.zeros([size], dtype=int),
                 'wCh': np.zeros([size], dtype=int),
                 'wM': np.zeros([size], dtype=int),
                 'gM': np.zeros([size], dtype=int),
                 'wADC': np.zeros([size], dtype=int),
                 'gADC:': np.zeros([size], dtype=int)
                 }
    # Initiate temporary variables
    start_time = df_raw.head(1)['srs_timestamp'].values[0]
    cluster_index = 0
    wM, gM, wADC, gADC, gCh, wCh = 0, 0, 0, 0, -1, -1
    # Insert first element
    data_dict['indices'][0] = cluster_index
    data_dict['gCh']

    # Iterate through data
    #for index, row in df_raw.iloc[1:].iterrows():
    #    current_time = row['srs_timestamp']
    #    if (current_time - start_time) > 3e3:
    #        pass
    #    else:
    #        # Increase cluster index and reset temporary variables
    #        cluster_index += 1
    #        start_time = current_time
    #        wM, gM, wADC, gADC, gCh, wCh = 0, 0, 0, 0, -1, -1
    #        # Start new cluster

    return df_raw, df_raw


# =============================================================================
# Helper Functions
# =============================================================================

def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise




