import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import plotly as py
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os







# =============================================================================
# Helper Functions
# =============================================================================

def get_MG24_to_XYZ_mapping():
    # Declare voxelspacing
    WireSpacing  = 10     #  [mm]
    LayerSpacing = 23.5   #  [mm]
    GridSpacing  = 23.5   #  [mm]
    # Iterate over all channels and create mapping
    MG24_ch_to_coord = np.empty((13, 80), dtype='object')
    for gCh in np.arange(0, 13, 1):
        for wCh in np.arange(0, 80, 1):
            x = (wCh // 20) * LayerSpacing
            y = gCh * GridSpacing
            z = (wCh % 20) * WireSpacing
            MG24_ch_to_coord[gCh, wCh] = {'x': x, 'y': y, 'z': z}
    return MG24_ch_to_coord










