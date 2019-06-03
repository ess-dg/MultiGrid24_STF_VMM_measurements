from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import os
import pandas as pd

from cluster import import_data, cluster_data
from Plotting.PHS import PHS_1D_plot, PHS_2D_plot

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
        self.cluster_progress.close()
        self.save_progress.close()
        self.load_progress.close()
        self.show()
        self.refresh_window()

    # Actions
    def cluster_action(self):
        # Intitate progress bar
        self.cluster_progress.show()
        self.cluster_progress.setValue(0)
        # Import data
        file_paths = QFileDialog.getOpenFileNames()[0]
        if len(file_paths) > 0:
            for i, file_path in enumerate(file_paths):
                data = import_data(file_path)
                clusters = cluster_data(data)
                self.measurement_time += self.get_duration(clusters)
                self.Clusters = self.Clusters.append(clusters)
                self.cluster_progress.setValue(i/len(file_paths)*100)
                self.refresh_window()
        self.cluster_progress.close()
        # Assign data set names and refresh window
        file_names = self.get_file_names(file_paths)
        self.data_sets_browser.setText(file_names)
        self.update()
        self.data_sets = file_names
        self.refresh_window()

    def PHS_1D_action(self):
        fig = PHS_1D_plot(self.Clusters, self)
        fig.show()

    def PHS_2D_action(self):
        fig = PHS_2D_plot(self.Clusters)
        fig.show()

    # Helper functions
    def setup_buttons(self):
        self.cluster_button.clicked.connect(self.cluster_action)
        self.PHS_1D_button.clicked.connect(self.PHS_1D_action)
        self.PHS_2D_button.clicked.connect(self.PHS_2D_action)

    def refresh_window(self):
        self.update()
        self.app.processEvents()
        self.update()
        self.app.processEvents()
        self.update()

    def get_file_names(self, file_paths):
        file_names = ''
        for i, file_path in enumerate(file_paths):
            file_names += file_path.rsplit('/', 1)[-1]
            #if i < len(file_paths) - 1:
            file_names += '\n'
        return file_names

    def get_duration(self, clusters):
        start_time = clusters.head(1)['srs_timestamp'].values[0]
        end_time = clusters.tail(1)['srs_timestamp'].values[0]
        return end_time - start_time




# =============================================================================
# Start GUI
# =============================================================================

app = QApplication(sys.argv)
main_window = MainWindow(app)
main_window.setAttribute(Qt.WA_DeleteOnClose, True)
main_window.setup_buttons()
sys.exit(app.exec_())
