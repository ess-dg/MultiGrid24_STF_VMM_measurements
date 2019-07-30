from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# =============================================================================
# Help message
# =============================================================================

def gethelp():
    msg = QMessageBox()
    msg.setStyleSheet("QLabel{min-width: 650px; min-height: 50px; font-size: 13px;}")
    msg.setText("How to use this program:")
    msg.setInformativeText("1. Click the \"cluster\" button and select a data file to be analysed. \n     Save: Converts and saves the data file (optional). \n     Load: Loads a previously saved data file.\n\n2. Apply filters (optional). Some filters are for events, some for clusters, some for both.\n\n     For events: \n     - Chips: which VMM chips \n     - Charge: ADC channels \n     - VMM channel: which channels for VMM \n\n     For clusters: \n     - gADC: grid ADC channel \t - wADC: wire ADC channel \n     - gM:  \t\t\t - wM: \n\n     For both: \n     - timestamp in ns \n     - gCH: grid channel \t\t - wCH: wire channel \n\n3. Select options. \n     - number of bins for PHS plots \n     - channel mapping: VMM or Multi-Grid channel mapping \n     - clustering time window: select time window for clustering \n\n4. Click on the buttons to get the specific plots.\n     PHS: Pulse Height Spectrum in \n     - 1D (counts vs collected charge), \n     - 2D (charge vs channel) \n     for wires and grids \n     - Individual: saves 1D PHS for each channel in ../Results folder\n     Coincidences: coincidence events in \n     - 2D (grid vs wire channel number)\n     - 3D (spatial) \n     Miscellaneous: \n     - timestamp: timestamp vs event number \n     - rate: prints the rate of neutron events")
    msg.setWindowTitle("Help")
    #msg.setStandardButtons(QMessageBox.Ok).setText("Now you know.")
    msg.addButton(QPushButton('Now you know.'), QMessageBox.YesRole)
    msg.exec_()
