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
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #events_20 = filter_events(df_20, window)
    #events_16 = filter_events(df_16, window)
    # Plot
    fig = plt.figure()
    plt.suptitle('Timestamp vs event number')
    """
    # 20 layers
    plt.subplot(1, 2, 1)
    plt.title('20 layers')
    plt.plot(df_20.srs_timestamp, color='black', zorder=5)
    plt.title('Timestamp vs event number -- 20 layers')
    plt.xlabel('Event number')
    plt.ylabel('Timestamp [TDC channels]')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    """
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

def chip_channels_plot(window):
    def chip_ch_plot_bus(events):
        # Plot
        plt.title("VMM chip %s" %VMM)
        plt.xlabel('chip channel id')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')
        plt.hist(events.channel, color='lightgrey', bins=48,
                 range=[-0.5, 47.5], ec='black', zorder=5)

    # Import data before any clustering or mapping
    #clusters_16 = window.data
    clusters_16 = window.Events_16_layers
    print(clusters_16)
    # Declare parameters
    VMM_order = [2, 3, 4, 5]

    # Prepare figure
    fig = plt.figure()
    fig.set_figheight(8)
    fig.set_figwidth(10)
    plt.suptitle('Channels per chip \n(%s, ...)' % window.data_sets.splitlines()[0])
    plt.title('16 layers')

    # Plot figure
    for i, VMM in enumerate(VMM_order):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(2, 2, i+1)
        chip_ch_plot_bus(events_VMM_16)
    plt.tight_layout()
    return fig
