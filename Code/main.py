from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import os
import pandas as pd
import numpy as np
import time

from cluster import import_data, cluster_data
from Plotting.PHS import (PHS_1D_VMM_plot, PHS_1D_MG_plot, PHS_2D_VMM_plot,
                          PHS_2D_MG_plot, PHS_Individual_plot,
                          PHS_Individual_Channel_plot, PHS_cluster_plot,
                          PHS_1D_overlay_plot)
from Plotting.Coincidences import Coincidences_2D_plot, Coincidences_3D_plot
from Plotting.Miscellaneous import timestamp_plot, chip_channels_plot, channel_rates
from Plotting.HelperFunctions import filter_coincident_events
from Plotting.HelpMessage import gethelp

# =============================================================================
# Windows
# =============================================================================


class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)
        dir_name = os.path.dirname(__file__)
        title_screen_path = os.path.join(dir_name, '../Windows/mainwindow.ui')
        self.ui = uic.loadUi(title_screen_path, self)
        self.app = app
        self.measurement_time = 0
        self.data_sets = ''
        #self.Clusters_20_layers = pd.DataFrame()
        self.Clusters_16_layers = pd.DataFrame()
        #self.Events_20_layers = pd.DataFrame()
        self.Events_16_layers = pd.DataFrame()
        #self.cluster_progress.close()
        self.VMM.setEnabled
        self.show()
        self.refresh_window()

    # =========================================================================
    # Actions
    # =========================================================================

    def cluster_action(self):
        t0 = time.time()
        # Import data
        file_paths = QFileDialog.getOpenFileNames(self, 'Open file', '../data')[0]
        size = len(file_paths)
        if size > 0:
            # Check if we want to append or write
            if self.write_button.isChecked():
                self.measurement_time = 0
                self.Clusters_20_layers = pd.DataFrame()
                self.Clusters_16_layers = pd.DataFrame()
                self.Events_20_layers   = pd.DataFrame()
                self.Events_16_layers   = pd.DataFrame()
                self.data_sets = ''
            else:
                self.data_sets += '\n'
            # Iterate through selected files
            for i, file_path in enumerate(file_paths):
                data = import_data(file_path, self)
                self.data = data
                print("DATA")
                print(data)
                print("length",len(data))
                clusters, events = cluster_data(data, self, i+1, size)
                print("EVENTS")
                print(events)
                print("length", len(events))
                print("CLUSTERS")
                print(clusters)
                print("length", len(clusters))
                self.measurement_time += self.get_duration(events)
                self.Clusters_20_layers = self.Clusters_20_layers.append(clusters)
                self.Clusters_16_layers = self.Clusters_16_layers.append(clusters)
                self.Events_20_layers = self.Events_20_layers.append(events)
                self.Events_16_layers = self.Events_16_layers.append(events)
                self.refresh_window()
            self.Clusters_20_layers.reset_index(drop=True, inplace=True)
            self.Clusters_16_layers.reset_index(drop=True, inplace=True)
            self.Events_20_layers.reset_index(drop=True, inplace=True)
            self.Events_16_layers.reset_index(drop=True, inplace=True)
            # Assign data set names and refresh window
            file_names = self.get_file_names(file_paths)
            self.data_sets += file_names
            self.data_sets_browser.setText(self.data_sets)
            self.update()
            self.update()
            self.data_sets = file_names
            self.refresh_window()
            #print(self.Clusters_16_layers)
            #print(self.Events_16_layers)
            #print(self.Clusters_20_layers)
            #print(self.Events_20_layers)

    def save_action(self):
        save_path = QFileDialog.getSaveFileName()[0]
        if save_path != '':
            save_data(save_path, self)

    def load_action(self):
        load_path = QFileDialog.getOpenFileName()[0]
        if load_path != '':
            load_data(load_path, self)

    def PHS_1D_action(self):
        if self.data_sets != '':
            if self.PHS_raw.isChecked():
                if self.VMM.isChecked():
                    fig = PHS_1D_VMM_plot(self)
                else:
                    fig = PHS_1D_MG_plot(self)
            elif self.PHS_clustered.isChecked():
                if self.VMM.isChecked():
                    fig = PHS_1D_VMM_plot(self)
                else:
                    fig = PHS_cluster_plot(self)
            elif self.PHS_overlay.isChecked():
                if self.VMM.isChecked():
                    fig = PHS_1D_VMM_plot(self)
                else:
                    fig = PHS_1D_overlay_plot(self)
            fig.show()

    def PHS_2D_action(self):
        if self.data_sets != '':
            if self.VMM.isChecked():
                fig = PHS_2D_VMM_plot(self)
            else:
                fig = PHS_2D_MG_plot(self)
            fig.show()

    def PHS_Individual_action(self):
        if self.data_sets != '':
            if self.ind_gCh.isChecked() or self.ind_wCh.isChecked():
                channel = self.ind_channel.value()
                fig = PHS_Individual_Channel_plot(self, channel)
                fig.show()
            else:
                fig = PHS_Individual_plot(self)

    def Coincidences_2D_action(self):
        if self.data_sets != '':
            fig = Coincidences_2D_plot(self)
            fig.show()

    def Coincidences_3D_action(self):
        if self.data_sets != '':
            Coincidences_3D_plot(self)

    def timestamp_action(self):
        if self.data_sets != '':
            fig = timestamp_plot(self)
            fig.show()

    def rate_action(self):
        if self.data_sets != '':
            ce_16 = self.Clusters_16_layers
            ce_20 = self.Clusters_20_layers
            layers_vec = [16, 20]
            events_vec = [ce_16, ce_20]
            for layer, events in zip(layers_vec, events_vec):
                ce_red = filter_coincident_events(events, self)
                start_time = ce_red.head(1)['Time'].values[0]
                end_time = ce_red.tail(1)['Time'].values[0]
                rate = ce_red.shape[0]/((end_time - start_time) * 1e-9)
                print('Total neutron rate (%s layers): %f Hz' % (layer, rate))

    def channel_rate_action(self):
        if self.data_sets != '':
            fig = channel_rates(self)
            fig.show()

    def help_action(self):
        print("HELP!!!!")
        gethelp()

    def chip_channels_action(self):
        if self.data_sets != '':
            fig = chip_channels_plot(self)
            fig.show()

    # =========================================================================
    # Helper Functions
    # =========================================================================

    def setup_buttons(self):
        # File handling
        self.cluster_button.clicked.connect(self.cluster_action)
        # PHS
        self.PHS_1D_button.clicked.connect(self.PHS_1D_action)
        self.PHS_2D_button.clicked.connect(self.PHS_2D_action)
        self.PHS_Individual_button.clicked.connect(self.PHS_Individual_action)
        # Coincidences
        self.Coincidences_2D_button.clicked.connect(self.Coincidences_2D_action)
        self.Coincidences_3D_button.clicked.connect(self.Coincidences_3D_action)
        # Miscellaneous
        self.timestamp_button.clicked.connect(self.timestamp_action)
        self.rate_button.clicked.connect(self.rate_action)
        self.channel_rate_button.clicked.connect(self.channel_rate_action)
        self.chip_ch_button.clicked.connect(self.chip_channels_action)
        self.toogle_VMM_MG()
        # Help
        self.helpbutton.clicked.connect(self.help_action)
        # Individual channels
        self.toggle_ind_channels()
        self.toggle_PHS_choice()
        self.toggle_detector_choice()

        # Styles and colours:
        self.helpbutton.setStyleSheet("background-color:hsv(0,120,230);border:2px solid hsv(0,120,210)")
        self.line.setStyleSheet("background-color:gray")
        self.line_2.setStyleSheet("background-color:gray")
        self.line_7.setStyleSheet("background-color:gray")
        self.line_5.setStyleSheet("background-color:gray")
        self.line_8.setStyleSheet("background-color:gray")
        self.ind_gCh.setStyleSheet("background-color:hsv(240, 10, 220)")
        self.ind_wCh.setStyleSheet("background-color:hsv(240, 10, 220)")
        self.ind_channel.setStyleSheet("background-color:hsv(240, 10, 220)")
        self.PHS_Individual_button.setStyleSheet("background-color:hsv(240,10,220);border:2px solid hsv(240,10,200)")
        self.PHS_1D_button.setStyleSheet("background-color:hsv(190,10,220);border:2px solid hsv(190,10,200)")
        self.PHS_2D_button.setStyleSheet("background-color:hsv(190,10,220);border:2px solid hsv(190,10,200)")
        self.MG.setStyleSheet("background-color:hsv(190,10,220)")
        self.VMM.setStyleSheet("background-color:hsv(190,10,220)")
        self.ind_ch_16.setStyleSheet("background-color:hsv(240, 10, 220)")
        self.ind_ch_20.setStyleSheet("background-color:hsv(240, 10, 220)")
        self.line_6.setStyleSheet("background-color:gray")
        self.line_16.setStyleSheet("background-color:gray")


    def refresh_window(self):
        self.update()
        self.app.processEvents()
        self.update()
        self.app.processEvents()
        self.update()
        self.app.processEvents()
        self.app.processEvents()
        self.app.processEvents()

    def get_file_names(self, file_paths):
        file_names = ''
        for i, file_path in enumerate(file_paths):
            file_names += file_path.rsplit('/', 1)[-1]
            if i < len(file_paths) - 1:
                file_names += '\n'
        return file_names

    def get_duration(self, events):
        start_time = events.head(1)['srs_timestamp'].values[0]
        end_time = events.tail(1)['srs_timestamp'].values[0]
        return end_time - start_time

    def toogle_VMM_MG(self):
        self.MG.toggled.connect(
            lambda checked: checked and self.VMM.setChecked(False))
        self.VMM.toggled.connect(
            lambda checked: checked and self.MG.setChecked(False))

    def toggle_ind_channels(self):
        self.ind_wCh.toggled.connect(
            lambda checked: checked and self.ind_gCh.setChecked(False))
        self.ind_gCh.toggled.connect(
            lambda checked: checked and self.ind_wCh.setChecked(False))

    def toggle_PHS_choice(self):
        self.PHS_raw.toggled.connect(
            lambda checked: checked and (self.PHS_clustered.setChecked(False), self.PHS_overlay.setChecked(False)))
        self.PHS_clustered.toggled.connect(
            lambda checked: checked and (self.PHS_raw.setChecked(False), self.PHS_overlay.setChecked(False)))
        self.PHS_overlay.toggled.connect(
            lambda checked: checked and (self.PHS_raw.setChecked(False), self.PHS_clustered.setChecked(False)))

    def toggle_detector_choice(self):
        self.ind_ch_16.toggled.connect(
            lambda checked: checked and self.ind_ch_20.setChecked(False))
        self.ind_ch_20.toggled.connect(
            lambda checked: checked and self.ind_ch_16.setChecked(False))

# =============================================================================
# Start GUI
# =============================================================================

app = QApplication(sys.argv)
main_window = MainWindow(app)
main_window.setAttribute(Qt.WA_DeleteOnClose, True)
main_window.setup_buttons()
sys.exit(app.exec_())
