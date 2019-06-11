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


def cluster_data(df_raw, window, file_nbr, file_nbrs):
    # Inititate parameters
    time_window = float(window.time_window.text())  # [TDC Channels]
    # Initate data vectors
    size = df_raw.shape[0]
    data_dict = {'wCh': np.zeros([size], dtype=int),
                 'gCh': np.zeros([size], dtype=int),
                 'wM': np.zeros([size], dtype=int),
                 'gM': np.zeros([size], dtype=int),
                 'wADC': np.zeros([size], dtype=int),
                 'gADC': np.zeros([size], dtype=int),
                 'Time': np.zeros([size], dtype=int)
                 }
    MG_channels = {'wCh': np.zeros([size], dtype=int),
                   'gCh': np.zeros([size], dtype=int)}
    # Get mappings
    VMM_ch_to_MG24_ch = get_VMM_to_MG24_mapping()
    chip_id_to_wire_or_grid = {2: ['gCh', 'gM', 'gADC', 'gMAX'],
                               3: ['wCh', 'wM', 'wADC', 'wMAX'],
                               4: ['wCh', 'wM', 'wADC', 'wMAX'],
                               5: ['wCh', 'wM', 'wADC', 'wMAX']}
    gw_ADC_max = {'wMAX': 0, 'gMAX': 0}
    # Get first values
    index = 0
    first_row = df_raw.iloc[0]
    start_time = int(first_row['srs_timestamp'])
    ADC = int(first_row['adc'])
    chip_id = int(first_row['chip_id'])
    Ch = int(first_row['channel'])
    # Start first cluster
    gw_ADC_max['wMAX'], gw_ADC_max['wMAX'] = 0, 0
    data_dict['wCh'][index], data_dict['gCh'][index] = -10, -10
    data_dict['Time'][index] = start_time
    # Modify first cluster
    mgCh = VMM_ch_to_MG24_ch[chip_id][Ch]
    xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
    data_dict[xADC][index] += ADC
    data_dict[xM][index] += 1
    if ADC > gw_ADC_max[xMAX]:
        gw_ADC_max[xMAX] = ADC
        data_dict[xCh][index] = mgCh
    MG_channels[xCh][0] = mgCh
    # Get numpy arrays from data frame
    Chs = df_raw['channel'].values[1:].astype(np.int64)
    ADCs = df_raw['adc'].values[1:].astype(np.int64)
    chip_ids = df_raw['chip_id'].values[1:].astype(np.int64)
    Times = df_raw['srs_timestamp'].values[1:].astype(np.int64)
    # Iterate through data
    for i, (Ch, ADC, chip_id, Time) in enumerate(zip(Chs, ADCs, chip_ids, Times)):
        mgCh = VMM_ch_to_MG24_ch[chip_id][Ch]
        if mgCh is None:
            mgCh = -10
        MG_channels['wCh'][i+1], MG_channels['gCh'][i+1] = -10, -10
        if (Time - start_time) < time_window:
            # Modify cluster
            xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
            data_dict[xADC][index] += ADC
            data_dict[xM][index] += 1
            if ADC > gw_ADC_max[xMAX]:
                gw_ADC_max[xMAX] = ADC
                data_dict[xCh][index] = mgCh
        else:
            # Increase cluster index and reset temporary variables
            index += 1
            start_time = Time
            # Start new cluster
            gw_ADC_max['wMAX'], gw_ADC_max['gMAX'] = 0, 0
            data_dict['wCh'][index], data_dict['gCh'][index] = -10, -10
            data_dict['Time'][index] = start_time
            # Modify new cluster
            xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
            data_dict[xADC][index] += ADC
            data_dict[xM][index] += 1
            if ADC > gw_ADC_max[xMAX]:
                gw_ADC_max[xMAX] = ADC
                data_dict[xCh][index] = mgCh
        # Add MG channel to the raw events
        MG_channels[xCh][i+1] = mgCh
        # Print progress on screen
        if i % 2000000 == 1:
            window.cluster_progress.setValue((file_nbr/file_nbrs)*(i/size)*100)
            window.refresh_window()

    #Remove empty elements and save in DataFrame for easier analysis
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][0:index]
    df_clustered = pd.DataFrame(data_dict)
    # Append vector to raw dataframe with MG channels
    df_raw = df_raw.join(pd.DataFrame(MG_channels))
    print(df_raw)
    print(df_clustered)
    return df_clustered, df_raw

# =============================================================================
# SAVE DATA
# =============================================================================


def save_data(clusters, events, path, window):
    window.save_progress.setValue(0)
    window.save_progress.show()
    window.update()
    window.app.processEvents()
    
    coincident_events.to_hdf(path, 'coincident_events', complevel=9)
    window.save_progress.setValue(25)
    window.update()
    window.app.processEvents()
    events.to_hdf(path, 'events', complevel=9)
    window.save_progress.setValue(50)
    window.update()
    window.app.processEvents()
    triggers.to_hdf(path, 'triggers', complevel=9)
    window.save_progress.setValue(75)
    window.update()
    window.app.processEvents()
    
    number_det = pd.DataFrame({'number_of_detectors': [number_of_detectors]})
    mod_or     = pd.DataFrame({'module_order': module_order})
    det_types  = pd.DataFrame({'detector_types': detector_types})
    da_set     = pd.DataFrame({'data_set': [data_set]})
    mt         = pd.DataFrame({'measurement_time': [measurement_time]})
    ca         = pd.DataFrame({'calibration': [calibration]})
    ei = pd.DataFrame({'E_i': [E_i]})
        
    number_det.to_hdf(path, 'number_of_detectors', complevel=9)
    mod_or.to_hdf(path, 'module_order', complevel=9)
    det_types.to_hdf(path, 'detector_types', complevel=9)
    da_set.to_hdf(path, 'data_set', complevel=9)
    mt.to_hdf(path, 'measurement_time', complevel=9)
    ei.to_hdf(path, 'E_i', complevel=9)
    ca.to_hdf(path, 'calibration', complevel=9)
    window.save_progress.setValue(100)
    window.update()
    window.app.processEvents()
    window.save_progress.close()


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


def get_VMM_to_MG24_mapping():
    # Import mapping
    dir_name = os.path.dirname(__file__)
    path_mapping = os.path.join(dir_name, '../Tables/MG_to_VMM_Mapping.xlsx')
    mapping_matrix = pd.read_excel(path_mapping).values
    # Store in convenient format
    VMM_ch_to_MG24_ch = np.empty((6, 80), dtype='object')
    for row in mapping_matrix:
        VMM_ch_to_MG24_ch[row[1]][row[2]] = row[5]
    return VMM_ch_to_MG24_ch




