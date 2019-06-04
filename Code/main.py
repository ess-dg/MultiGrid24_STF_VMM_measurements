from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import os
import pandas as pd

from cluster import import_data, cluster_data
from Plotting.PHS import (PHS_1D_VMM_plot, PHS_1D_MG_plot, PHS_2D_VMM_plot,
                          PHS_2D_MG_plot)
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
        self.Clusters = pd.DataFrame()
        self.Events = pd.DataFrame()
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
        # Intitate progress bar
        self.cluster_progress.show()
        self.cluster_progress.setValue(0)
        # Import data
        file_paths = QFileDialog.getOpenFileNames()[0]
        size = len(file_paths)
        if size > 0:
            # Check if we want to append or write
            if self.write.isChecked():
                self.measurement_time = 0
                self.Clusters = pd.DataFrame()
                self.Events = pd.DataFrame()
            # Iterate through selected files
            for i, file_path in enumerate(file_paths):
                data = import_data(file_path)
                clusters, events = cluster_data(data, self, i+1, size)
                self.measurement_time += self.get_duration(events)
                self.Clusters = self.Clusters.append(clusters)
                self.Events = self.Events.append(events)
                self.cluster_progress.setValue(i/len(file_paths)*100)
                self.refresh_window()
            self.Clusters.reset_index(drop=True, inplace=True)
            self.Events.reset_index(drop=True, inplace=True)
            self.cluster_progress.close()
            # Assign data set names and refresh window
            file_names = self.get_file_names(file_paths)
            self.data_sets_browser.setText(file_names)
            self.update()
            self.update()
            self.data_sets = file_names
            self.refresh_window()

    def PHS_1D_action(self):
        if self.data_sets != '':
            if self.VMM.isChecked():
                fig = PHS_1D_VMM_plot(self.Events, self)
            else:
                fig = PHS_1D_MG_plot(self.Events, self)
            fig.show()

    def PHS_2D_action(self):
        if self.data_sets != '':
            if self.VMM.isChecked():
                fig = PHS_2D_VMM_plot(self.Events, self)
            else:
                fig = PHS_2D_MG_plot(self.Events, self)
            fig.show()

    def timestamp_action(self):
        if self.data_sets != '':
            fig = timestamp_plot(self.Events, self)
            fig.show()

    # =========================================================================
    # Helper Functions
    # =========================================================================

    def setup_buttons(self):
        self.cluster_button.clicked.connect(self.cluster_action)
        self.PHS_1D_button.clicked.connect(self.PHS_1D_action)
        self.PHS_2D_button.clicked.connect(self.PHS_2D_action)
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
