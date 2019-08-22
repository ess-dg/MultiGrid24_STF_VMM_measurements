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


def import_data(file_path, window):
    h5_file = h5py.File(file_path, 'r')
    if window.sample_button.isChecked():
        data = pd.DataFrame(h5_file['srs_hits'].value[100:120])
    else:
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
    data_dict['wCh'][index], data_dict['gCh'][index] = -1, -1
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
        MG_channels['wCh'][i+1], MG_channels['gCh'][i+1] = -1, -1
        if (Time - start_time) < time_window: # selecting max ADC channel within a time window
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
            data_dict['wCh'][index], data_dict['gCh'][index] = -1, -1
            data_dict['Time'][index] = start_time
            # Modify new cluster
            xCh, xM, xADC, xMAX = chip_id_to_wire_or_grid[chip_id]
            data_dict[xADC][index] += ADC
            data_dict[xM][index] += 1
            #print(chip_id)
            #print(chip_id_to_wire_or_grid[chip_id])
            #print(xCh, xM)
            if ADC > gw_ADC_max[xMAX]:
                gw_ADC_max[xMAX] = ADC
                data_dict[xCh][index] = mgCh
        # Add MG channel to the raw events
        MG_channels[xCh][i+1] = mgCh

    #Remove empty elements and save in DataFrame for easier analysis
    for key in data_dict.keys():
        data_dict[key] = data_dict[key][0:index]
    df_clustered = pd.DataFrame(data_dict)
    # Append vector to raw dataframe with MG channels
    df_raw = df_raw.join(pd.DataFrame(MG_channels))

    return df_clustered, df_raw


# =============================================================================
# SAVE DATA
# =============================================================================


def save_data(path, window):
    # Initiate loading bar
    window.save_progress.setValue(0)
    window.save_progress.show()
    window.refresh_window()
    # Save clusters
    window.Clusters.to_hdf(path, 'Clusters', complevel=9)
    window.save_progress.setValue(33)
    window.refresh_window()
    # Save events
    window.Events.to_hdf(path, 'Events', complevel=9)
    window.save_progress.setValue(66)
    window.refresh_window()
    # Save parameters
    data_sets = pd.DataFrame({'data_sets': [window.data_sets]})
    measurement_time = pd.DataFrame({'measurement_time': [window.measurement_time]})
    data_sets.to_hdf(path, 'data_sets', complevel=9)
    measurement_time.to_hdf(path, 'measurement_time', complevel=9)
    window.save_progress.setValue(100)
    window.refresh_window()
    window.save_progress.close()
    window.refresh_window()


# =============================================================================
# LOAD DATA
# =============================================================================


def load_data(path, window):
    # Initiate loading bar
    window.load_progress.setValue(0)
    window.load_progress.show()
    window.refresh_window()
    # Load clusters
    Clusters = pd.read_hdf(path, 'Clusters')
    window.load_progress.setValue(25)
    window.refresh_window()
    # Load events
    Events = pd.read_hdf(path, 'Events')
    window.load_progress.setValue(50)
    window.refresh_window()
    # Load parameters
    measurement_time_df = pd.read_hdf(path, 'measurement_time')
    measurement_time = measurement_time_df['measurement_time'].iloc[0]
    data_sets_df = pd.read_hdf(path, 'data_sets')
    data_sets = data_sets_df['data_sets'].iloc[0]
    # Write or append
    if window.write_button.isChecked():
        window.Clusters = Clusters
        window.Events = Events
        window.measurement_time = measurement_time
        window.data_sets = data_sets
    else:
        window.Clusters = window.Clusters.append(Clusters)
        window.Events = window.Events.append(Events)
        window.measurement_time += measurement_time
        window.data_sets += '\n' + data_sets
    # Reset index on clusters and events
    window.Clusters.reset_index(drop=True, inplace=True)
    window.Events.reset_index(drop=True, inplace=True)
    # Update text browser and close loading bar
    window.load_progress.setValue(100)
    window.refresh_window()
    window.load_progress.close()
    window.data_sets_browser.setText(window.data_sets)
    window.refresh_window()


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
    #path_mapping = os.path.join(dir_name, '../Tables/Latest_Isabelle_MG_to_VMM_Mapping.xlsx')
    #path_mapping = os.path.join(dir_name, '../Tables/MG_to_VMM_Mapping_old.xlsx')
    #path_mapping = os.path.join(dir_name, '../Tables/MG_to_VMM_Mapping_16_flipped.xlsx')
    path_mapping = os.path.join(dir_name, '../Tables/new_THE_MG_to_VMM_Mapping.xlsx')
    mapping_matrix = pd.read_excel(path_mapping).values
    #print(mapping_matrix)
    # Store in convenient format
    VMM_ch_to_MG24_ch = np.empty((6, 80), dtype='object')
    for row in mapping_matrix:
        VMM_ch_to_MG24_ch[row[1]][row[2]] = row[5]
    #print(VMM_ch_to_MG24_ch)
    return VMM_ch_to_MG24_ch
