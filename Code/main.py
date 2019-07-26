from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import os
import pandas as pd

from cluster import import_data, cluster_data, save_data, load_data
from Plotting.PHS import (PHS_1D_VMM_plot, PHS_1D_MG_plot, PHS_2D_VMM_plot,
                          PHS_2D_MG_plot)
from Plotting.Coincidences import Coincidences_2D_plot, Coincidences_3D_plot
from Plotting.Miscellaneous import timestamp_plot

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
        self.Clusters_20_layers = pd.DataFrame()
        self.Clusters_16_layers = pd.DataFrame()
        self.Events_20_layers = pd.DataFrame()
        self.Events_16_layers = pd.DataFrame()
        self.cluster_progress.close()
        self.save_progress.close()
        self.load_progress.close()
        self.VMM.setEnabled
        self.show()
        self.refresh_window()

    # =========================================================================
    # Actions
    # =========================================================================

    def cluster_action(self):
        # Import data
        file_paths = QFileDialog.getOpenFileNames(self, 'Open file', "../data")[0]
        size = len(file_paths)
        if size > 0:
            # Intitate progress bar
            self.cluster_progress.show()
            self.cluster_progress.setValue(0)
            # Check if we want to append or write
            if self.write_button.isChecked():
                self.measurement_time = 0
                self.Clusters_20_layers = pd.DataFrame()
                self.Clusters_16_layers = pd.DataFrame()
                self.Events_20_layers = pd.DataFrame()
                self.Events_16_layers = pd.DataFrame()
                self.data_sets = ''
            else:
                self.data_sets += '\n'
            # Iterate through selected files
            for i, file_path in enumerate(file_paths):
                data = import_data(file_path)
                clusters, events = cluster_data(data, self, i+1, size)
                self.measurement_time += self.get_duration(events)
                self.Clusters_20_layers = self.Clusters_20_layers.append(clusters)
                self.Clusters_16_layers = self.Clusters_16_layers.append(clusters)
                self.Events_20_layers = self.Events_20_layers.append(events)
                self.Events_16_layers = self.Events_16_layers.append(events)
                self.cluster_progress.setValue(((i+1)/len(file_paths))*100)
                self.refresh_window()
            self.Clusters_20_layers.reset_index(drop=True, inplace=True)
            self.Clusters_16_layers.reset_index(drop=True, inplace=True)
            self.Events_20_layers.reset_index(drop=True, inplace=True)
            self.Events_16_layers.reset_index(drop=True, inplace=True)
            self.cluster_progress.close()
            # Assign data set names and refresh window
            file_names = self.get_file_names(file_paths)
            self.data_sets += file_names
            self.data_sets_browser.setText(self.data_sets)
            self.update()
            self.update()
            self.data_sets = file_names
            self.refresh_window()
            #print(self.Clusters_16_layers)
            print(self.Clusters_20_layers)
            print(self.Events_20_layers)

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
            if self.VMM.isChecked():
                fig = PHS_1D_VMM_plot(self)
            else:
                fig = PHS_1D_MG_plot(self)
            fig.show()

    def PHS_2D_action(self):
        if self.data_sets != '':
            if self.VMM.isChecked():
                fig = PHS_2D_VMM_plot(self)
            else:
                fig = PHS_2D_MG_plot(self)
            fig.show()

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

    # =========================================================================
    # Helper Functions
    # =========================================================================

    def setup_buttons(self):
        # File handling
        self.cluster_button.clicked.connect(self.cluster_action)
        self.save_button.clicked.connect(self.save_action)
        self.load_button.clicked.connect(self.load_action)
        # PHS
        self.PHS_1D_button.clicked.connect(self.PHS_1D_action)
        self.PHS_2D_button.clicked.connect(self.PHS_2D_action)
        # Coincidences
        self.Coincidences_2D_button.clicked.connect(self.Coincidences_2D_action)
        self.Coincidences_3D_button.clicked.connect(self.Coincidences_3D_action)
        # Miscellaneous
        self.timestamp_button.clicked.connect(self.timestamp_action)
        self.toogle_VMM_MG()

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





# =============================================================================
# Start GUI
# =============================================================================

app = QApplication(sys.argv)
main_window = MainWindow(app)
main_window.setAttribute(Qt.WA_DeleteOnClose, True)
main_window.setup_buttons()
sys.exit(app.exec_())
