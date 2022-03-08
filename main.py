'''
This is a trial for a lifting tool that will produce a simplified port by port overview of consumption.
The tool will use the day by day budget already created in the current fuel planning tool
Only one vessel can be entered into the budget day by day (this will be amended for multiple ships
'''

import tkinter as tk
import ctypes
import numpy as np
from tkinter import filedialog
import pandas as pd
from Legs import *

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
##Prompts to select the excel file that has the day by day consumption
Mbox('File Selection', 'Please Select the Fuel Tool Version you wish to use', 0)
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

budget_db = pd.read_csv(file_path)

budget_db.columns = budget_db.loc[2]
budget_db = budget_db.iloc[3:,:]
budget_db.dropna(subset = ["Ship"], inplace = True)
budget_db = budget_db.astype(dict_type_columns)
budget_db.fillna(0, inplace=True)
ship_names = pd.unique(budget_db['Ship'])

new_lifting_dataframe = pd.DataFrame()

legs_reference = func_get_legs(budget_db)
new_lifting_dataframe['Legs'] = [x[0] for x in legs_reference]
ETA_reference, ETD_reference = func_get_eta_etd(legs_reference, budget_db)
new_lifting_dataframe['ETA'] = [x[0]+" " + x[1] for x in ETA_reference]
new_lifting_dataframe['ETD'] = [x[0]+" " + x[1] for x in ETD_reference]

#Call At Sea Consumption
HFO_AT_SEA_REF = func_calc_hfo_sea(ETA_reference, ETD_reference, legs_reference, budget_db)
MGO_AT_SEA_REF = func_calc_mgo_sea(ETA_reference, ETD_reference, legs_reference, budget_db)
LNG_AT_SEA_REF = func_calc_lng_sea(ETA_reference, ETD_reference, legs_reference, budget_db)
if sum(HFO_AT_SEA_REF) != 0:
    new_lifting_dataframe['HFO at Sea'] = HFO_AT_SEA_REF
if sum(MGO_AT_SEA_REF) != 0:
    new_lifting_dataframe['MGO at Sea'] = MGO_AT_SEA_REF
if sum(LNG_AT_SEA_REF) != 0:
    new_lifting_dataframe['LNG at Sea'] = LNG_AT_SEA_REF

#Call In-Port Consumption
ports_reference = func_get_ports(budget_db)
HFO_IN_PORT = func_calc_hfo_in_port(ports_reference, budget_db)
MGO_IN_PORT = func_calc_mgo_in_port(ports_reference, budget_db)
LNG_IN_PORT = func_calc_lng_in_port(ports_reference, budget_db)
if sum(HFO_IN_PORT) !=0:
    new_lifting_dataframe['HFO in Port'] = HFO_IN_PORT
if sum(MGO_IN_PORT) != 0:
    new_lifting_dataframe['MGO in Port'] = MGO_IN_PORT
if sum(LNG_IN_PORT) != 0:
    new_lifting_dataframe['LNG in Port'] = LNG_IN_PORT
print(new_lifting_dataframe)















