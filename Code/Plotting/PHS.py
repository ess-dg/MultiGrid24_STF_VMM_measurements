import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib.colors import LogNorm
from Plotting.HelperFunctions import filter_events

# ============================================================================
# PHS (1D) - VMM
# ============================================================================


def PHS_1D_VMM_plot(window):
    def PHS_1D_plot_bus(events, sub_title, number_bins):
        # Plot
        if VMM == 2:
            sub_title += ' (Grids)'
        else:
            sub_title += ' (Wires)'
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')
        plt.hist(events.adc, bins=number_bins,
                 range=[0, 1050], histtype='step',
                 color='black', zorder=5)
    # Declare parameters
    VMM_order_20 = [2, 3, 4, 5]
    VMM_order_16 = [2, 3, 4, 5]
    number_bins = int(window.phsBins.text())
    # Import data
    df_20 = window.Events#window.Clusters_20_layers
    df_16 = window.Events#window.Clusters_16_layers
    # Initial filter
    clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    # for 20 layers
    for i, VMM in enumerate(VMM_order_20):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(4, 2, i+1)
        sub_title = 'VMM: %s' % VMM + " -- 20 layers"
        PHS_1D_plot_bus(events_VMM_20, sub_title, number_bins)
    plt.tight_layout()
    # for 16 layers
    for i, VMM in enumerate(VMM_order_16):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(4, 2, i+5)
        sub_title = 'VMM: %s' % VMM + " -- 16 layers"
        PHS_1D_plot_bus(events_VMM_16, sub_title, number_bins)
    plt.tight_layout()
    return fig


# ============================================================================
# PHS (1D) - MG
# ============================================================================


def PHS_1D_MG_plot(events, window):
    def PHS_1D_plot_bus(events, typeCh, sub_title, number_bins):
        # Plot
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')
        plt.hist(events[events[typeCh] >= 0].adc, bins=number_bins,
                 range=[0, 1050], histtype='step',
                 color='black', zorder=5)

    # Declare parameters
    number_bins = int(window.phsBins.text())
    typeChs = ['wCh', 'gCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Initial filter
    events = filter_events(events, window)
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    fig.set_figheight(4)
    fig.set_figwidth(10)
    # Plot figure
    for i, typeCh in enumerate(typeChs):
        plt.subplot(1, 2, i+1)
        sub_title = grids_or_wires[typeCh]
        PHS_1D_plot_bus(events, typeCh, sub_title, number_bins)
    plt.tight_layout()
    return fig


# =============================================================================
# PHS (2D) - VMM
# =============================================================================


def PHS_2D_VMM_plot(events, window):
    def PHS_2D_plot_bus(events, VMM, limit, bins, sub_title, vmin, vmax):
        if VMM == 2:
            sub_title += ' (Grids)'
        else:
            sub_title += ' (Wires)'
        plt.xlabel('Channel')
        plt.ylabel('Charge [ADC channels]')
        plt.title(sub_title)
        plt.hist2d(events.channel, events.adc, bins=[bins, 120],
                   range=[limit, [0, 1050]], norm=LogNorm(),
                   vmin=vmin, vmax=vmax, cmap='jet')
        plt.colorbar()


    number_bins = int(window.phsBins.text())
    # Import data
    df_20 = window.Events#window.Clusters_20_layers
    df_16 = window.Events#window.Clusters_16_layers
    # Initial filter
    clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)
    # Declare parameters
    VMM_order_20 = [2, 3, 4, 5]
    VMM_order_16 = [2, 3, 4, 5]
    VMM_limits_20 = [[15.5, 48.5],
                    [17.5, 46.5],
                    [16.5, 46.5],
                    [16.5, 46.5]]
    VMM_limits_16 = [[15.5, 48.5],
                    [17.5, 46.5],
                    [16.5, 46.5],
                    [16.5, 46.5]]
    VMM_bins_20 = [33, 29, 30, 30]
    VMM_bins_16 = [33, 29, 30, 30]
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - VMM\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    vmin = 1
    vmax_20 = clusters_20.shape[0] // 1000 + 100
    vmax_16 = clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    # for 20 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order, VMM_limits, VMM_bins)):
        events_VMM = events[events.chip_id == VMM]
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s' % VMM
        PHS_2D_plot_bus(events_VMM, VMM, limit, bins, sub_title, vmin, vmax)
    plt.tight_layout()
    # for 16 laysers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order, VMM_limits, VMM_bins)):
        events_VMM = events[events.chip_id == VMM]
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s' % VMM
        PHS_2D_plot_bus(events_VMM, VMM, limit, bins, sub_title, vmin, vmax)
    plt.tight_layout()
    return fig

# =============================================================================
# PHS (2D) - MG
# =============================================================================


def PHS_2D_MG_plot(events, window):
    def PHS_2D_plot_bus(events, typeCh, limit, bins, sub_title, vmin, vmax):
        plt.xlabel('Channel')
        plt.ylabel('Charge [ADC channels]')
        plt.title(sub_title)
        plt.hist2d(events[typeCh], events.adc, bins=[bins, 120],
                   range=[limit, [0, 1050]], norm=LogNorm(),
                   vmin=vmin, vmax=vmax, cmap='jet')
        plt.colorbar()

    def get_wire_events(events, window):
        events_red = None
        if window.wCh_filter.isChecked():
            wCh_min = window.wCh_min.value()
            wCh_max = window.wCh_max.value()
            events_red = events[(events['wCh'] >= wCh_min)
                                & (events['wCh'] <= wCh_max)]
        else:
            events_red = events[(events['wCh'] >= 0)
                                & (events['wCh'] <= 79)]

        return events_red

    def get_grid_events(events, window):
        events_red = None
        if window.gCh_filter.isChecked():
            gCh_min = window.gCh_min.value()
            gCh_max = window.gCh_max.value()
            events_red = events[(events['gCh'] >= gCh_min)
                                & (events['gCh'] <= gCh_max)]
        else:
            events_red = events[(events['gCh'] >= 0)
                                & (events['gCh'] <= 12)]

        return events_red
    # Declare parameters
    typeChs = ['wCh', 'gCh']
    limits = [[-0.5, 78.5], [-0.5, 11.5]]
    bins = [79, 12]
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Initial filter
    events = filter_events(events, window)
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - MG\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    vmin = 1
    vmax = events.shape[0] // 1000 + 100
    fig.set_figheight(4)
    fig.set_figwidth(10)
    # Plot figure
    for i, (typeCh, limit, bins) in enumerate(zip(typeChs, limits, bins)):
        # Filter events based on wires or grids
        if typeCh == 'wCh':
            events_red = get_wire_events(events, window)
        else:
            events_red = get_grid_events(events, window)
        plt.subplot(1, 2, i+1)
        sub_title = 'PHS: %s' % grids_or_wires[typeCh]
        PHS_2D_plot_bus(events_red, typeCh, limit, bins, sub_title, vmin, vmax)
    plt.tight_layout()
    return fig
