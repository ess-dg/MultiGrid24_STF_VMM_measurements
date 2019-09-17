import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import plotly as py
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os

from Plotting.HelperFunctions import filter_events, filter_coincident_events

# =============================================================================
# Timestamp
# =============================================================================


def timestamp_plot(window):
    data_sets = window.data_sets.splitlines()[0]
    # Import data
    df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Plot
    fig = plt.figure()
    fig.set_figheight(4.5)
    fig.set_figwidth(9)
    plt.suptitle('Timestamp vs event number\nData set(s): %s' % data_sets)
    # 20 layers
    plt.subplot(1, 2, 1)
    plt.title('20 layers')
    plt.plot(df_20.srs_timestamp, color='black', zorder=5)
    plt.xlabel('Event number')
    plt.ylabel('Timestamp [TDC channels]')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    # for 16 layers
    plt.subplot(1, 2, 2)
    plt.title('16 layers')
    plt.plot(df_16.srs_timestamp, color='black', zorder=5)
    plt.xlabel('Event number')
    plt.ylabel('Timestamp [TDC channels]')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    plt.subplots_adjust(left=0.08, right=0.96, top=0.82, bottom=0.12, wspace=0.32)
    return fig

# =============================================================================
# Number of times a channel is used in each VMM chip
# =============================================================================

def chip_channels_plot(window):
    def chip_ch_plot_bus(events, sub_title):
        # Plot
        plt.title("VMM chip %s %s" %(VMM, sub_title))
        plt.xlabel('chip channel id')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')
        plt.xticks(np.arange(0, 65, 10))
        plt.hist(events.channel, align="left", bins=65, range=[0, 65],
                 color='lightgrey', ec='black', zorder=5)

    # Import data before any clustering or mapping
    clusters_16 = window.data
    clusters_20 = window.data
    # Declare parameters
    VMM_order_16 = [2, 3, 4, 5]
    VMM_order_20 = [2, 3, 4, 5]
    # Prepare figure
    fig = plt.figure()
    fig.set_figheight(8)
    fig.set_figwidth(13)
    plt.suptitle('Channels per chip \n(%s, ...)' % window.data_sets.splitlines()[0])
    #plt.title('16 layers')

    # Plot figure
    # for 20 layers
    for i, VMM in enumerate(VMM_order_20):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(2, 4, i+1)
        sub_title = "-- 20 layers"
        chip_ch_plot_bus(events_VMM_20, sub_title)
    # for 16 layers
    for i, VMM in enumerate(VMM_order_16):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(2, 4, i+5)
        sub_title = "-- 16 layers"
        chip_ch_plot_bus(events_VMM_16, sub_title)
    plt.subplots_adjust(left=0.07, right=0.98, top=0.88, bottom=0.09, wspace=0.4, hspace=0.35)
    return fig

def channel_rates(window):
    """plots neutron event rate for each channel"""
    def channel_rates_plot_bus(events, subtitle, typeCh, wires):
        plt.xlabel('grid channel')
        plt.ylabel('Rate of total counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.title("Grid rates")
        #print("Grid channel \t rate")
        gChs = []
        g_rates = []
        if typeCh == 'gCh':
            for gCh in np.arange(0, 12, 1):
                counts = len(events[events.gCh == gCh])
                rate = counts/((end_time - start_time) * 1e-9)
                gChs.append(gCh)
                g_rates.append(rate)
                #print(gCh, "\t", rate, "Hz")
            plt.scatter(gChs, g_rates, color="darkorange", zorder=2)
            plt.title(sub_title)

        #print("Wire channel \t rate")
        wChs = []
        w_rates = []
        if typeCh == 'wCh':
            for wCh in np.arange(0, wires, 1):
                counts = len(events[events.wCh == wCh])
                rate = counts/((end_time - start_time) * 1e-9)
                wChs.append(wCh)
                w_rates.append(rate)
                #print(wCh, "\t", rate, "Hz")
            plt.scatter(wChs, w_rates, color="crimson", zorder=2)
            plt.title(sub_title)

    clusters_16 = window.Clusters_16_layers
    clusters_16 = filter_coincident_events(clusters_16, window)
    clusters_20 = window.Clusters_20_layers
    clusters_20 = filter_coincident_events(clusters_20, window)
    start_time = clusters_16.head(1)['Time'].values[0]
    end_time = clusters_16.tail(1)['Time'].values[0]
    typeChs = ['gCh', 'wCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # plot
    fig = plt.figure()
    fig.set_figheight(5)
    fig.set_figwidth(10)
    plt.suptitle('Total rate per channel \n%s)' % window.data_sets.splitlines()[0])

    # for 20 layers
    for i, typeCh in enumerate(typeChs):
        sub_title = "%s -- 20 layers" % grids_or_wires[typeCh]
        wires = 80
        plt.subplot(2,2,i+1)
        channel_rates_plot_bus(clusters_20, sub_title, typeCh, wires)

    # for 16 layers
    for i, typeCh in enumerate(typeChs):
        sub_title = "%s -- 16 layers" % grids_or_wires[typeCh]
        plt.subplot(2,2,i+3)
        wires = 64
        channel_rates_plot_bus(clusters_16, sub_title, typeCh, wires)

    plt.subplots_adjust(left=0.1, right=0.98, top=0.86, bottom=0.09, wspace=0.25, hspace=0.45)
    return fig
