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


def cluster_data(data):
    return data


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




