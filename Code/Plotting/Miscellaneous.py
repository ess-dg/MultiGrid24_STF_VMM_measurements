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


def timestamp_plot(events, window):
    # Initial filter
    events = filter_events(events, window)
    # Plot
    fig = plt.figure()
    plt.plot(events.srs_timestamp, color='black', zorder=5)
    plt.title('Timestamp vs event number')
    plt.xlabel('Event number')
    plt.ylabel('Timestamp [TDC channels]')
    plt.grid(True, which='major', zorder=0)
    plt.grid(True, which='minor', linestyle='--', zorder=0)
    return fig


