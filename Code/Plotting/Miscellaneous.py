import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import plotly as py
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os

from Plotting.HelperFunctions import filter_events

# =============================================================================
# Timestamp
# =============================================================================


def timestamp_plot(window):
    # Import data
    df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #events_20 = filter_events(df_20, window)
    #events_16 = filter_events(df_16, window)
    # Plot
    fig = plt.figure()
    plt.suptitle('Timestamp vs event number')
    # 20 layers
    plt.subplot(1, 2, 1)
    plt.title('20 layers')
    plt.plot(df_20.srs_timestamp, color='black', zorder=5)
    plt.title('Timestamp vs event number -- 20 layers')
    plt.xlabel('Event number')
    plt.ylabel('Timestamp [TDC channels]')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)

    # for 16 layers
    plt.subplot(1, 2, 2)
    plt.title('16 layers')
    plt.plot(df_16.srs_timestamp, color='black', zorder=5)
    plt.title('Timestamp vs event number -- 16 layers')
    plt.xlabel('Event number')
    plt.ylabel('Timestamp [TDC channels]')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    return fig
