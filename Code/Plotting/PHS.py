import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib.colors import LogNorm

# ============================================================================
# PHS (1D)
# ============================================================================


def PHS_1D_plot(events, window):
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
    VMM_order = [2, 3, 4, 5]
    number_bins = int(window.phsBins.text())
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (1D)\n(%s, ...)' % window.data_sets.splitlines()[0]
    fig.suptitle(title, x=0.5, y=1.03)
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    for i, VMM in enumerate(VMM_order):
        events_VMM = events[events.chip_id == VMM]
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s' % VMM
        PHS_1D_plot_bus(events_VMM, sub_title, number_bins)
    plt.tight_layout()
    return fig


# =============================================================================
# PHS (2D)
# =============================================================================


def PHS_2D_plot(events, window):
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
    # Declare parameters
    VMM_order = [2, 3, 4, 5]
    VMM_limits = [[17.5, 46.5],
                  [17.5, 46.5],
                  [16.5, 46.5],
                  [16.5, 46.5]]
    VMM_bins = [29, 29, 30, 30]
    # Prepare figure
    fig = plt.figure()
    title = 'PHS (2D)\n(%s, ...)' % window.data_sets.rsplit('\n', 1)[0]
    fig.suptitle(title, x=0.5, y=1.03)
    vmin = 1
    vmax = events.shape[0] // 1000 + 100
    fig.set_figheight(8)
    fig.set_figwidth(10)
    # Plot figure
    for i, (VMM, limit, bins) in enumerate(zip(VMM_order, VMM_limits, VMM_bins)):
        events_VMM = events[events.chip_id == VMM]
        plt.subplot(2, 2, i+1)
        sub_title = 'VMM: %s' % VMM
        PHS_2D_plot_bus(events_VMM, VMM, limit, bins, sub_title, vmin, vmax)
    plt.tight_layout()
    return fig












