# Multi-Grid Analysis: VMM Hybrid Read-out 

Application for analysis of Multi-Grid data taken with the VMM Hybrid read-out system.
The program consists of a GUI Interface which allows the user to cluster and analyse data using different tools, such as:

- Event gating
- PHS (Cumulative or individual channel)
- Coincidences (2D and 3D)
- ToF

## Requisties
- Python3 (https://www.python.org/downloads/)
- Anaconda (https://www.anaconda.com/distribution/)

## Installation
Install dependencies:
```
conda install -c anaconda pyqt 
conda install -c plotly plotly
conda install h5py
```

Clone the repository:
```
git clone https://github.com/ess-dg/MultiGrid24_STF_VMM_measurements.git
```

## Execution
Navigate to MultiGridVMM->Code and enter:
```
python main.py
```
## Notes

The code requires two excel-documents to work:
- Mappin_VMM_MG.xlsx
- MG_to_VMM_Mapping.xlsx

These can be found in the 'Tables'-folder in the repository, and the files can be manipulated according to the specific conditions of the measurement.
