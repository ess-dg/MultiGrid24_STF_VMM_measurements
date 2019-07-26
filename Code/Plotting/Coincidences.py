import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import plotly as py
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import os
from Plotting.HelperFunctions import filter_coincident_events


# =============================================================================
# Coincidence Histogram (2D)
# =============================================================================


def Coincidences_2D_plot(window):
    # Declare parameters (added with condition if empty array)
    data_sets = window.data_sets.splitlines()[0]
    # Import data
    df_20 = window.Clusters_20_layers
    df_16 = window.Clusters_16_layers
    # Initial filter, keep only coincident events
    clusters_20 = filter_coincident_events(df_20, window)
    clusters_16 = filter_coincident_events(df_16, window)

    # Plot data
    fig = plt.figure()
    plt.suptitle('Coincident events (2D)\nData set(s): %s' % data_sets)

    # for 20 layers
    plt.subplot(1, 2, 1)
    plt.title('20 layers')
    plt.hist2d(clusters_20.wCh, clusters_20.gCh, bins=[80, 12],
               range=[[-0.5, 79.5], [-0.5, 11.5]],
               norm=LogNorm(), cmap='jet')
    plt.xlabel('Wire [Channel number]')
    plt.ylabel('Grid [Channel number]')
    plt.colorbar()

    # for 16 layers
    plt.subplot(1, 2, 2)
    plt.title('16 layers')
    plt.hist2d(clusters_16.wCh, clusters_16.gCh, bins=[64, 12],
               range=[[-0.5, 63.5], [-0.5, 11.5]],
               norm=LogNorm(), cmap='jet')
    plt.xlabel('Wire [Channel number]')
    plt.ylabel('Grid [Channel number]')
    plt.colorbar()
    return fig


# =============================================================================
# Coincidence Histogram (3D)
# =============================================================================

def Coincidences_3D_plot(window):
    # Import data
    df_20 = window.Clusters_20_layers
    df_16 = window.Clusters_16_layers
    # Perform initial filters
    clusters_20 = filter_coincident_events(df_20, window)
    clusters_16 = filter_coincident_events(df_16, window)
    # Declare max and min count
    min_count = 0
    max_count = np.inf
    # Initiate 'voxel_id -> (x, y, z)'-mapping
    MG24_ch_to_coord_20, MG24_ch_to_coord_16 = get_MG24_to_XYZ_mapping()
    # Calculate 3D histogram




    # 20 layers
    H_20, edges_20 = np.histogramdd(clusters_20[['wCh', 'gCh']].values,
                              bins=(80, 13),
                              range=((0, 80), (0, 13))
                              )
    # Insert results into an array
    hist_20 = [[], [], [], []]
    loc_20 = 0
    labels_20 = []
    for wCh in range(0, 80):
        for gCh in range(0, 13):
            over_min = H_20[wCh, gCh] > min_count
            under_max = H_20[wCh, gCh] <= max_count
            if over_min and under_max:
                coord = MG24_ch_to_coord_20[gCh, wCh]
                hist_20[0].append(coord['x'])
                hist_20[1].append(coord['y'])
                hist_20[2].append(coord['z'])
                hist_20[3].append(H_20[wCh, gCh])
                loc_20 += 1
                labels_20.append('Wire Channel: ' + str(wCh) + '<br>'
                              + 'Grid Channel: ' + str(gCh) + '<br>'
                              + 'Counts: ' + str(H_20[wCh, gCh])
                              )

    # 16 layers
    H_16, edges_16 = np.histogramdd(clusters_16[['wCh', 'gCh']].values,
                              bins=(64, 13),
                              range=((0, 64), (0, 13))
                              )
    # Insert results into an array
    hist_16 = [[], [], [], []]
    loc_16 = 0
    labels_16 = []
    for wCh in range(0, 64):
        for gCh in range(0, 13):
            over_min = H_16[wCh, gCh] > min_count
            under_max = H_16[wCh, gCh] <= max_count
            if over_min and under_max:
                coord = MG24_ch_to_coord_16[gCh, wCh]
                hist_16[0].append(coord['x'])
                hist_16[1].append(coord['y'])
                hist_16[2].append(coord['z'])
                hist_16[3].append(H_16[wCh, gCh])
                loc_16 += 1
                labels_16.append('Wire Channel: ' + str(wCh) + '<br>'
                              + 'Grid Channel: ' + str(gCh) + '<br>'
                              + 'Counts: ' + str(H_16[wCh, gCh])
                              )

    # Produce 3D histogram plot
    labels = []
    labels.extend(labels_20)
    labels.extend(labels_16)

    # Produce 3D histogram plot
    hist = [[], [], [], []]
    hist_x_offset = [i + 100 for i in hist_20[0]]
    hist_z_offset = [i +  40 for i in hist_16[2]]
    hist[0].extend(hist_x_offset)
    hist[0].extend(hist_16[0])
    hist[1].extend(hist_20[1])
    hist[1].extend(hist_16[1])
    hist[2].extend(hist_20[2])
    hist[2].extend(hist_z_offset)
    hist[3].extend(hist_20[3])
    hist[3].extend(hist_16[3])

    MG_3D_trace = go.Scatter3d(x=hist[0],
                               y=hist[1],
                               z=hist[2],
                               mode='markers',
                               marker=dict(size=5,
                                           color=np.log10(hist[3]),
                                           colorscale='Jet',
                                           opacity=1,
                                           colorbar=dict(thickness=20,
                                                         title='log10(counts)'
                                                         ),
                                           ),
                               text=labels,
                               name='Multi-Grid',
                               scene='scene1'
                               )
    # Introduce figure and put everything together
    fig = py.tools.make_subplots(rows=1, cols=1,
                                 specs=[[{'is_3d': True}]]
                                 )
    # Insert histogram
    fig.append_trace(MG_3D_trace, 1, 1)
    # Assign layout with axis labels, title and camera angle
    fig['layout']['scene1']['xaxis'].update(title='x [mm]')
    fig['layout']['scene1']['yaxis'].update(title='y [mm]')
    fig['layout']['scene1']['zaxis'].update(title='z [mm]')
    fig['layout'].update(title='Coincidences (3D)')
    fig.layout.showlegend = False
    # If in plot He3-tubes histogram, return traces, else save HTML and plot
    py.offline.plot(fig,
                    filename='../Results/Ce3Dhistogram.html',
                    auto_open=True)
    #pio.write_image(fig, '../Results/HTML_files/Ce3Dhistogram.pdf')


# =============================================================================
# Helper Functions
# =============================================================================

def get_MG24_to_XYZ_mapping():
    # Declare voxelspacing in [mm]
    WireSpacing = 10
    LayerSpacing = 23.5
    GridSpacing = 23.5
    # Iterate over all channels and create mapping
    # 20 layers
    MG24_ch_to_coord_20 = np.empty((13, 80), dtype='object')
    for gCh in np.arange(0, 13, 1):
        for wCh in np.arange(0, 80, 1):
            x = (wCh // 20) * LayerSpacing
            y = gCh * GridSpacing
            z = (wCh % 20) * WireSpacing
            MG24_ch_to_coord_20[gCh, wCh] = {'x': x, 'y': y, 'z': z}
    MG24_ch_to_coord_16 = np.empty((13, 80), dtype='object')
    # 16 layers
    for gCh in np.arange(0, 13, 1):
        for wCh in np.arange(0, 64, 1):
            x = (wCh // 20) * LayerSpacing
            y = gCh * GridSpacing
            z = (wCh % 20) * WireSpacing
            MG24_ch_to_coord_16[gCh, wCh] = {'x': x, 'y': y, 'z': z}
    return MG24_ch_to_coord_20, MG24_ch_to_coord_16
