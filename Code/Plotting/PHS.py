import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib.colors import LogNorm
from Plotting.HelperFunctions import filter_events, filter_coincident_events

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
                 range=[0, 1050], histtype='stepfilled',
                 facecolor='lightgrey', ec='black', zorder=5)
    # Declare parameters
    VMM_order_20 = [2, 3, 4, 5]
    VMM_order_16 = [2, 3, 4, 5]
    number_bins = int(window.phsBins.text())
    # Import data
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    #print(df_16)
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, VMM in enumerate(VMM_order_20):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(4, 2, i+1)
        sub_title = 'VMM: %s' % VMM + " -- 20 layers"
        PHS_1D_plot_bus(events_VMM_20, sub_title, number_bins)
    plt.tight_layout()
    """
    # for 16 layers
    for i, VMM in enumerate(VMM_order_16):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        #plt.subplot(4, 2, i+5)
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s' % VMM + " -- 16 layers"
        PHS_1D_plot_bus(events_VMM_16, sub_title, number_bins)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.87, bottom=0.08, wspace=0.25, hspace=0.33)
    return fig

# ============================================================================
# PHS (1D) - MG
# ============================================================================


def PHS_1D_MG_plot(window):
    def PHS_1D_plot_bus(clusters, typeCh, sub_title, number_bins):
        # Plot
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')
        plt.hist(clusters[clusters[typeCh] >= 0].adc, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled', ec='black',
                 facecolor='lightgrey', zorder=5)

    # Declare parameters
    number_bins = int(window.phsBins.text())
    typeChs = ['gCh', 'wCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}

    # Import data
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)

    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(4.5)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(2, 2, i+1)
        sub_title = "%s -- 20 layers" % typeCh
        PHS_1D_plot_bus(clusters_20, typeCh, sub_title, number_bins)
    plt.tight_layout()
    """
    # for 16 layers
    for i, typeCh in enumerate(typeChs):
        plt.subplot(1, 2, i+1)
        sub_title = "%s -- 16 layers" % grids_or_wires[typeCh]
        PHS_1D_plot_bus(clusters_16, typeCh, sub_title, number_bins)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.85, bottom=None, wspace=0.25, hspace=None)

    return fig


# =============================================================================
# PHS (2D) - VMM
# =============================================================================


def PHS_2D_VMM_plot(window):
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
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
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
    #VMM_bins_20 = [33, 29, 30, 30]
    VMM_bins_16 = [33, 29, 30, 30]
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - VMM\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.99)
    vmin = 1
    #vmax_20 = clusters_20.shape[0] // 1000 + 100
    vmax_16 = clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order_20, VMM_limits_20, VMM_bins_20)):
        events_VMM_20 = clusters_20[clusters_20.chip_id == VMM]
        plt.subplot(4, 2, i+1)
        sub_title = 'VMM: %s -- 20 layers' % VMM
        PHS_2D_plot_bus(events_VMM_20, VMM, limit, bins, sub_title, vmin, vmax_20)
    plt.tight_layout()
    """
    # for 16 layers
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order_16, VMM_limits_16, VMM_bins_16)):
        events_VMM_16 = clusters_16[clusters_16.chip_id == VMM]
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s -- 16 layers' % VMM
        PHS_2D_plot_bus(events_VMM_16, VMM, limit, bins, sub_title, vmin, vmax_16)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.95, top=0.89, bottom=0.08, wspace=0.25, hspace=0.33)
    return fig

# =============================================================================
# PHS (2D) - MG
# =============================================================================


def PHS_2D_MG_plot(window):
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


    # Import data
    #df_20 = window.Events_20_layers
    df_16 = window.Events_16_layers
    # Declare parameters
    typeChs = ['gCh', 'wCh']
    limits_20 = [[-0.5, 11.5], [-0.5, 78.5]]
    bins_20 = [12, 79]
    limits_16 = [[-0.5, 11.5], [-0.5, 62.5]]
    bins_16 = [12, 63]
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Initial filter
    #clusters_20 = filter_events(df_20, window)
    clusters_16 = filter_events(df_16, window)

    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D) - MG\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.99)
    vmin = None# 1
    vmax_20 = None #clusters_20.shape[0] // 1000 + 100
    vmax_16 = None #clusters_16.shape[0] // 1000 + 100
    fig.set_figheight(4.5)
    fig.set_figwidth(10)
    # Plot figure
    """
    # for 20 layers
    for i, (typeCh, limit, bins) in enumerate(zip(typeChs, limits_20, bins_20)):
        # Filter events based on wires or grids
        if typeCh == 'wCh':
            events_red_20 = get_wire_events(clusters_20, window)
        else:
            events_red_20 = get_grid_events(clusters_20, window)
        plt.subplot(2, 2, i+1)
        sub_title = 'PHS: %s -- 20 layers' % grids_or_wires[typeCh]
        PHS_2D_plot_bus(events_red_20, typeCh, limit, bins, sub_title, vmin, vmax_20)
    plt.tight_layout()
    """
    # for 16 layers
    for i, (typeCh, limit, bins) in enumerate(zip(typeChs, limits_16, bins_16)):
        # Filter events based on wires or grids
        if typeCh == 'wCh':
            events_red_16 = get_wire_events(clusters_16, window)
        else:
            events_red_16 = get_grid_events(clusters_16, window)
        plt.subplot(1, 2, i+1)
        sub_title = 'PHS: %s -- 16 layers' % grids_or_wires[typeCh]
        PHS_2D_plot_bus(events_red_16, typeCh, limit, bins, sub_title, vmin, vmax_16)
    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.98, top=0.83, bottom=0.12, wspace=0.25, hspace=None)
    return fig


# =============================================================================
# PHS (Individual Channels)
# =============================================================================

def PHS_Individual_plot(window):
    # Import data
    #df_20 = window.Events
    df_events_16 = window.Events_16_layers
    df_clusters_16 = window.Clusters_16_layers
    # Intial filter
    events_16 = filter_events(df_events_16, window)
    clusters_16 = filter_coincident_events(df_clusters_16, window)
    #events_20 = filter_events(df_20, window)
    # Declare parameters
    events_vec = [events_16]#[events_16, events_20]
    clusters_vec = [clusters_16]
    detectors = ['16_layers']#['16_layers', '20_layers']
    layers_vec = [16]#[16, 20]
    dir_name = os.path.dirname(__file__)
    folder_path = os.path.join(dir_name, '../../Results/PHS')
    number_bins = int(window.phsBins.text())

    if window.PHS_raw.isChecked():
        # Save all PHS
        for events, detector, layers in zip(events_vec, detectors, layers_vec):
            # Save wires PHS
            for wCh in np.arange(0, layers*4, 1):
                print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
                # Get ADC values
                adcs = events[events.wCh == wCh]['adc']
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
                # Save
                output_path = '%s/%s/Wires_raw/Channel_%d.pdf' % (folder_path, detector, wCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()
            # Save grids PHS
            for gCh in np.arange(0, 12, 1):
                print('%s, Grids: %d/11' % (detector, gCh))
                # Get ADC values
                adcs = events[events.gCh == gCh]['adc']
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
                # Save
                output_path = '%s/%s/Grids_raw/Channel_%d.pdf' % (folder_path, detector, gCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()

    elif window.PHS_clustered.isChecked():
        # Save all PHS
        for clusters, detector, layers in zip(clusters_vec, detectors, layers_vec):
            # Save wires PHS
            for wCh in np.arange(0, layers*4, 1):
                print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
                # Get ADC values
                adcs = clusters[clusters.wCh == wCh]['wADC']
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
                # Save
                output_path = '%s/%s/Wires_clustered/Channel_%d.pdf' % (folder_path, detector, wCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()
            # Save grids PHS
            for gCh in np.arange(0, 12, 1):
                print('%s, Grids: %d/11' % (detector, gCh))
                # Get ADC values
                adcs = clusters[clusters.gCh == gCh]['gADC']
                # Plot
                fig = plt.figure()
                plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
                # Save
                output_path = '%s/%s/Grids_clustered/Channel_%d.pdf' % (folder_path, detector, gCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()

    elif window.PHS_overlay.isChecked():
        # Save all PHS
        for clusters, events, detector, layers in zip(clusters_vec, events_vec, detectors, layers_vec):
            # Save wires PHS
            for wCh in np.arange(0, layers*4, 1):
                print('%s, Wires: %d/%d' % (detector, wCh, layers*4-1))
                # Get ADC values
                adcs_events = events[events.wCh == wCh]['adc']
                adcs_clusters = clusters[clusters.wCh == wCh]['wADC']
                # Plot
                fig = plt.figure()
                plt.hist(adcs_events, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5)
                plt.hist(adcs_clusters, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', alpha=0.5, zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS wires - Channel %d\nData set: %s' % (wCh, window.data_sets))
                # Save
                output_path = '%s/%s/Wires_overlay/Channel_%d.pdf' % (folder_path, detector, wCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()
            # Save grids PHS
            for gCh in np.arange(0, 12, 1):
                print('%s, Grids: %d/11' % (detector, gCh))
                # Get ADC values
                adcs_events = events[events.gCh == gCh]['adc']
                adcs_clusters = clusters[clusters.gCh == gCh]['gADC']
                # Plot
                fig = plt.figure()
                plt.hist(adcs_events, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightgrey', ec='black', zorder=5)
                plt.hist(adcs_clusters, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                         facecolor='lightblue', ec='black', alpha=0.5, zorder=5)
                plt.grid(True, which='major', zorder=0)
                plt.grid(True, which='minor', linestyle='--', zorder=0)
                plt.xlabel('Collected charge [ADC channels]')
                plt.ylabel('Counts')
                plt.title('PHS grids - Channel %d\nData set: %s' % (gCh, window.data_sets))
                # Save
                output_path = '%s/%s/Grids_overlay/Channel_%d.pdf' % (folder_path, detector, gCh)
                fig.savefig(output_path, bbox_inches='tight')
                plt.close()


def PHS_Individual_Channel_plot(window, channel):
    # Import data
    df_events_16 = window.Events_16_layers
    df_clusters_16 = window.Clusters_16_layers
    # Intial filter
    events_16 = filter_events(df_events_16, window)
    clusters_16 = filter_coincident_events(df_clusters_16, window)
    number_bins = int(window.phsBins.text())
    # Plot
    fig = plt.figure()
    # Get ADC values
    if window.PHS_raw.isChecked():
        if window.ind_gCh.isChecked():
            adcs = events_16[events_16.gCh == channel]['adc']
            w_or_g = 'grid'
        elif window.ind_wCh.isChecked():
            adcs = events_16[events_16.wCh == channel]['adc']
            w_or_g = 'wire'
        plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                facecolor='lightgrey', ec='black', zorder=5)
    elif window.PHS_clustered.isChecked():
        if window.ind_gCh.isChecked():
            adcs = clusters_16[clusters_16.gCh == channel]['gADC']
            w_or_g = 'grid'
        elif window.ind_wCh.isChecked():
            adcs = clusters_16[clusters_16.wCh == channel]['wADC']
            w_or_g = 'wire'
            plt.hist(adcs, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                    facecolor='lightblue', ec='black', zorder=5)
    elif window.PHS_overlay.isChecked():
        if window.ind_gCh.isChecked():
            adcs_events = events_16[events_16.gCh == channel]['adc']
            adcs_clusters = clusters_16[clusters_16.gCh == channel]['gADC']
            w_or_g = 'grid'
        elif window.ind_wCh.isChecked():
            adcs_events = events_16[events_16.wCh == channel]['adc']
            adcs_clusters = clusters_16[clusters_16.wCh == channel]['wADC']
            w_or_g = 'wire'
            plt.hist(adcs_events, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                     facecolor='lightgrey', ec='black', zorder=5)
            plt.hist(adcs_clusters, bins=number_bins, range=[0, 1050], histtype='stepfilled',
                     facecolor='lightblue', ec='black', alpha=0.5, zorder=5)

    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    plt.xlabel('Collected charge [ADC channels]')
    plt.ylabel('Counts')
    plt.title('PHS %s channel %d\nData set: %s' % (w_or_g, channel, window.data_sets))
    return fig

def PHS_cluster_plot(window):
    # Import data
    df_16 = window.Clusters_16_layers
    # Initial filter
    clusters_16 = filter_coincident_events(df_16, window)
    number_bins = int(window.phsBins.text())
    # Prepare figure
    fig = plt.figure()
    title = 'PHS clustered (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(4.5)
    fig.set_figwidth(10)
    # Plot figure
    plt.subplot(1, 2, 1)
    adcs_16 = clusters_16['gADC']
    plt.xlabel('Collected charge [ADC channels]')
    plt.ylabel('Counts')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    plt.yscale('log')
    plt.hist(adcs_16, bins=number_bins, range=[0, 1050], histtype='stepfilled',
             facecolor='lightblue', ec='black', zorder=5)
    plt.title("PHS grid channels")

    plt.subplot(1, 2, 2)
    adcs_16 = clusters_16['wADC']
    plt.xlabel('Collected charge [ADC channels]')
    plt.ylabel('Counts')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    plt.yscale('log')
    plt.hist(adcs_16, bins=number_bins, range=[0, 1050], histtype='stepfilled',
            facecolor='lightblue', ec='black', zorder=5)
    plt.title("PHS wire channels")

    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.93, top=0.83, bottom=0.12, wspace=0.25, hspace=None)
    return fig

def PHS_1D_overlay_plot(window):
    def PHS_1D_overlay_plot_bus(clusters_16, typeCh, sub_title, number_bins, events_16):
        # Plot
        plt.title(sub_title)
        plt.xlabel('Collected charge [ADC channels]')
        plt.ylabel('Counts')
        plt.grid(True, which='major', zorder=0)
        plt.grid(True, which='minor', linestyle='--', zorder=0)
        plt.yscale('log')

        if typeCh == 'gCh':
            adcs_clusters_16 = clusters_16['gADC']
        elif typeCh == 'wCh':
            adcs_clusters_16 = clusters_16['wADC']
        plt.hist(events_16[events_16[typeCh] >= 0].adc, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled', ec='black',
                 facecolor='lightgrey', zorder=5, label='raw')
        plt.hist(adcs_clusters_16, bins=number_bins,
                 range=[0, 1050], histtype='stepfilled', ec='black',
                 facecolor='lightblue', alpha=0.5, zorder=5, label='clustered')
        plt.legend()

    # Import data
    raw_16 = window.Events_16_layers
    clustered_16 = window.Clusters_16_layers
    # Apply filters
    events_16 = filter_events(raw_16, window)
    clusters_16 = filter_coincident_events(clustered_16, window)
    number_bins = int(window.phsBins.text())
    typeChs = ['gCh', 'wCh']
    grids_or_wires = {'wCh': 'Wires', 'gCh': 'Grids'}
    # Prepare figure
    fig = plt.figure()
    title = 'PHS overlay (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=0.98)
    fig.set_figheight(4.5)
    fig.set_figwidth(10)
    # Plot figure
    for i, typeCh in enumerate(typeChs):
        plt.subplot(1, 2, i+1)
        sub_title = "%s -- 16 layers" % grids_or_wires[typeCh]
        PHS_1D_overlay_plot_bus(clusters_16, typeCh, sub_title, number_bins, events_16)

    plt.subplots_adjust(left=0.1, right=0.93, top=0.83, bottom=0.12, wspace=0.25, hspace=None)
    return fig
