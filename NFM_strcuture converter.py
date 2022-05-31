import pandas as pd
from tkinter import filedialog
import ctypes
import tkinter as tk
from Legs import *
from ROB import *
from shutil import copyfile

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
##Prompts to select the excel file that has the day by day consumption
Mbox('File Selection', 'Please Select the Fuel Tool Version you wish to use', 0)
root = tk.Tk()
file_path = filedialog.askopenfilename()
root.destroy()

budget_db = pd.read_excel(file_path, sheet_name = "NFM_Structure")
print(budget_db.info())
print(budget_db)

ship_names = [x for x in pd.unique(budget_db['Ship'])]

#'create a temporary dataframe for each individual ship'

for ship in ship_names[0:3]:
    ship_specific_liftplan = pd.DataFrame()
    temp_budget_db = pd.DataFrame()
    #set the columns that will be used for the background information of the lift plan
    temp_budget_db = budget_db.loc[budget_db["Ship"] == ship].fillna(0)
    temp_budget_db.reset_index()
    HFO_IN_PORT, HFO_AT_SEA = func_grab_HFO_consumption(temp_budget_db)
    MGO_IN_PORT, MGO_AT_SEA = func_grab_MGO_consumption(temp_budget_db)
    LNG_IN_PORT, LNG_AT_SEA = func_grab_LNG_Consumption(temp_budget_db)

    ship_specific_liftplan['Port'] = temp_budget_db.iloc[:,3]
    ship_specific_liftplan['TTG C.C.'] = temp_budget_db['TTG C.C.']
    ship_specific_liftplan['Port Arrival Date Time'] = temp_budget_db['Port Arrival Date Time']
    ship_specific_liftplan['Port Departure Date Time']= temp_budget_db['Port Departure Date Time']
    if sum(HFO_AT_SEA) != 0:
        ship_specific_liftplan['HFO at Sea'] = HFO_AT_SEA
    if sum(MGO_AT_SEA) != 0:
        ship_specific_liftplan['MGO at Sea'] = MGO_AT_SEA
    if sum(LNG_AT_SEA) != 0:
        ship_specific_liftplan['LNG at Sea'] = LNG_AT_SEA
    if sum(LNG_AT_SEA) + sum(HFO_AT_SEA) == 0:
        ship_specific_liftplan['Single Fuel Type'] = True

    if sum(HFO_IN_PORT) != 0:
        ship_specific_liftplan['HFO in Port'] = HFO_IN_PORT
    if sum(MGO_IN_PORT) != 0:
        ship_specific_liftplan['MGO in Port'] = MGO_IN_PORT
    if sum(LNG_IN_PORT) != 0:
        ship_specific_liftplan['LNG in Port'] = LNG_IN_PORT

    if sum(LNG_IN_PORT) + sum(HFO_IN_PORT) == 0:
        ship_specific_liftplan['Empty'] = False

    ship_specific_liftplan['ShorePower'] = temp_budget_db['Shore Power']

    # Call User Interface to enter ROB's
    #    get_starting_ROBs(ship)
    First_Starting_ROB = Starting_ROB_Dict[ship][0]
    Second_Starting_ROB = Starting_ROB_Dict[ship][1]

    #Creates the Bunker columnes
    if sum(HFO_IN_PORT) != 0:
        ship_specific_liftplan['HFO Arriving ROB'] = ""
        ship_specific_liftplan["HFO Arriving ROB"].iloc[0] = First_Starting_ROB
        ship_specific_liftplan['HFO Bunker'] = ""
        ship_specific_liftplan['HFO Departing ROB'] = ""
    if sum(MGO_IN_PORT) != 0:
        ship_specific_liftplan['MGO Arriving ROB'] = ""
        ship_specific_liftplan["MGO Arriving ROB"].iloc[0] = Second_Starting_ROB
        ship_specific_liftplan['MGO Bunker'] = ""
        ship_specific_liftplan['MGO Departing ROB'] = ""
    if sum(LNG_IN_PORT) != 0:
        ship_specific_liftplan['LNG Arriving ROB'] = ""
        ship_specific_liftplan["LNG Arriving ROB"].iloc[0] = First_Starting_ROB
        ship_specific_liftplan['LNG Bunker'] = ""
        ship_specific_liftplan['LNG Departing ROB'] = ""



# Export Dataframe to excel worksheet
    temp_file = str(ship) + " Test.xlsx"
    copyfile("Test.xlsx", temp_file)
    with pd.ExcelWriter(temp_file, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
        ship_specific_liftplan.to_excel(writer, sheet_name="Lifting Structure", startrow=3)

    print(ship_specific_liftplan)