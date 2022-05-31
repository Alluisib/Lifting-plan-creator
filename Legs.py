import numpy as np
import pandas as pd

dict_type_columns = {"BEFORE PIN @ SEA-Con. \nHFO": float,
                     "BEFORE PIN @ SEA-Con. \nHFO instead of MGO by scrubber": float,
                     "BEFORE PIN @ SEA-Con. \nadditional HFO consumption for scrubber usage": float,
                     "MAN-IN\nCon. HFO": float,
                     "MAN-IN @ Con. \nHFO instead of MGO by scrubber": float,
                     "MAN-IN @ Con.\nadditional HFO consumption for scrubber usage": float,
                     "MAN-OUT\nCon. HFO": float,
                     "MAN-OUT @ Con. \nHFO instead of MGO by scrubber": float,
                     "MAN-OUT @ Con.\nadditional HFO consumption for scrubber usage": float,
                     "AFTER POUT\n@ SEA-Con. HFO": float,
                     "AFTER POUT @ SEA-Con. \nHFO instead of MGO by scrubber": float,
                     "AFTER POUT @ SEA-Con. \nadditional HFO consumption for scrubber usage": float,
                     "BEFORE PIN \n@ SEA-Con. MGO": float,
                     "BEFORE PIN \n@ SEA-Con. MGO due to AAQS non allowance": float,
                     "BEFORE PIN \n@ SEA-Con. MGO for LNG Ignition": float,
                     "MAN-IN\nCon. MGO": float,
                     "MAN-IN Con.\nMGO for LNG Ignition": float,
                     "MAN-OUT\nCon. MGO": float,
                     "MAN-OUT Con.\nMGO for LNG Ignition": float,
                     "AFTER POUT\n@ SEA-Con. MGO": float,
                     "AFTER POUT\n@ SEA-Con. MGO due to AAQS non allowance": float,
                     "AFTER POUT \n@ SEA-Con. \nMGO for LNG Ignition": float,
                     "BEFORE PIN \n@ SEA-Con. LNG": float,
                     "MAN-IN\nCon. LNG": float,
                     "MAN-OUT\nCon. LNG": float,
                     "AFTER POUT\n@ SEA-Con. LNG": float,
                     "PORT-Con. HFO": float,
                     "PORT-Con HFO instead of MGO due to scrubber": float,
                     "PORT Consumption. \nadditional HFO consumption for scrubber usage": float,
                     "PORT-Con. MGO": float,
                     "PORT-Con.\nMGO for LNG Ignition": float,
                     "PORT-Con. LNG": float,

            }

hfo_sea_dict = {0: "BEFORE PIN @ SEA-Con. \nHFO",
            1: "BEFORE PIN @ SEA-Con. \nHFO instead of MGO by scrubber",
            2: "BEFORE PIN @ SEA-Con. \nadditional HFO consumption for scrubber usage",
            3: "MAN-IN\nCon. HFO",
            4: "MAN-IN @ Con. \nHFO instead of MGO by scrubber",
            5: "MAN-IN @ Con.\nadditional HFO consumption for scrubber usage",
            6: "MAN-OUT\nCon. HFO",
            7: "MAN-OUT @ Con. \nHFO instead of MGO by scrubber",
            8: "MAN-OUT @ Con.\nadditional HFO consumption for scrubber usage",
            9: "AFTER POUT\n@ SEA-Con. HFO",
            10: "AFTER POUT @ SEA-Con. \nHFO instead of MGO by scrubber",
            11: "AFTER POUT @ SEA-Con. \nadditional HFO consumption for scrubber usage",
            }


mgo_sea_dict = {0: "BEFORE PIN \n@ SEA-Con. MGO",
            1: "BEFORE PIN \n@ SEA-Con. MGO due to AAQS non allowance",
            2: "BEFORE PIN \n@ SEA-Con. MGO for LNG Ignition",
            3: "MAN-IN\nCon. MGO",
            4: "MAN-IN Con.\nMGO for LNG Ignition",
            5: "MAN-OUT\nCon. MGO",
            6: "MAN-OUT Con.\nMGO for LNG Ignition",
            7: "AFTER POUT\n@ SEA-Con. MGO",
            8: "AFTER POUT\n@ SEA-Con. MGO due to AAQS non allowance",
            9: "AFTER POUT \n@ SEA-Con. \nMGO for LNG Ignition"
            }
lng_sea_dict = {0: "BEFORE PIN \n@ SEA-Con. LNG",
                1: "MAN-IN\nCon. LNG",
                2: "MAN-OUT\nCon. LNG",
                3: "AFTER POUT\n@ SEA-Con. LNG"}

hfo_port_dict = {0: "PORT-Con. HFO",
            1: "PORT-Con HFO instead of MGO due to scrubber",
            2: "PORT Consumption. \nadditional HFO consumption for scrubber usage"}
mgo_port_dict = {0: "PORT-Con. MGO",1: "PORT-Con.\nMGO for LNG Ignition"}
lng_port_dict = {0: "PORT-Con. LNG"}

def func_get_legs(df):
    reference_list = []
    i=0
    previous_port = ""
    for port in df['Port']:
        if str(port) != "At Sea":
            if previous_port != port:
                reference_list.append((str(port),i))
        i += 1
        previous_port = port
    return reference_list

def func_get_eta_etd(legs, df):
    eta = []
    etd = []
    count = 0
    for leg in legs:
        eta.append((df['Day'].iloc[leg[1]], df['ETA'].iloc[leg[1]]))
        if df['ETD'].iloc[leg[1]] == "overnight":
            count = leg[1]
            while df['ETD'].iloc[count] == "overnight":
                count +=1
            etd.append((df['Day'].iloc[count],df['ETD'].iloc[count]))
        etd.append((df['Day'].iloc[leg[1]],df['ETD'].iloc[leg[1]]))
    return eta,etd
def func_get_cruise_code(legs, df):
    cruise_code = []
    count = 0
    for leg in legs:
        cruise_code.append(df['Cruise #'].iloc[leg[1]])
    return cruise_code

def func_calc_hfo_sea(eta, etd,legs, df):
    hfo_sea_consumption = []
    leg_counter = 0
    lastleg = (0,0)
    for leg in legs:
        hfo_temp_calculator = 0

        if leg[1] == 0:
            hfo_sea_consumption.append(hfo_temp_calculator)

        else:

            if eta[leg_counter][0] == etd[leg_counter][0]:
                    #As long as the leg is not the first the HFO calculation will be the same
                    starting_line = lastleg[1]
                    endingline = leg[1]

                    while starting_line < endingline:
                        counter = 0
                        while counter < len(hfo_sea_dict):

                            if counter > 5:
                                #looks up in the data frame the HFO column listed on previous line
                                hfo_temp_calculator += df[hfo_sea_dict[counter]].iloc[starting_line]
                            else:
                                hfo_temp_calculator += df[hfo_sea_dict[counter]].iloc[starting_line+1]
                            counter +=1

                        #adds the total HFO consumption from the HFO columns to the list
                        starting_line += 1
                    hfo_sea_consumption.append(hfo_temp_calculator)
            else:
                print("Overnight found")

        leg_counter+=1
        lastleg = leg

    return hfo_sea_consumption

def func_calc_mgo_sea(eta, etd,legs, df):
    mgo_sea_consumption = []
    leg_counter = 0
    lastleg = (0,0)
    for leg in legs:
        mgo_temp_calculator = 0

        if leg[1] == 0:
            mgo_sea_consumption.append(mgo_temp_calculator)

        else:

            if eta[leg_counter][0] == etd[leg_counter][0]:
                    #As long as the leg is not the first the HFO calculation will be the same
                    starting_line = lastleg[1]
                    endingline = leg[1]

                    while starting_line < endingline:
                        counter = 0
                        while counter < len(mgo_sea_dict):

                            if counter > 4:
                                #looks up in the data frame the HFO column listed on previous line
                                mgo_temp_calculator += df[mgo_sea_dict[counter]].iloc[starting_line]
                            else:
                                mgo_temp_calculator += df[mgo_sea_dict[counter]].iloc[starting_line+1]
                            counter +=1

                        #adds the total HFO consumption from the HFO columns to the list
                        starting_line += 1
                    mgo_sea_consumption.append(mgo_temp_calculator)
            else:
                print("Overnight found")

        leg_counter+=1
        lastleg = leg

    return mgo_sea_consumption

def func_calc_lng_sea(eta, etd,legs, df):
    lng_sea_consumption = []
    leg_counter = 0
    lastleg = (0,0)
    for leg in legs:
        lng_temp_calculator = 0

        if leg[1] == 0:
            lng_sea_consumption.append(lng_temp_calculator)

        else:

            if eta[leg_counter][0] == etd[leg_counter][0]:
                    #As long as the leg is not the first the HFO calculation will be the same
                    starting_line = lastleg[1]
                    endingline = leg[1]

                    while starting_line < endingline:
                        counter = 0
                        while counter < len(lng_sea_dict):

                            if counter > 2:
                                #looks up in the data frame the HFO column listed on previous line
                                lng_temp_calculator += df[lng_sea_dict[counter]].iloc[starting_line]
                            else:
                                lng_temp_calculator += df[lng_sea_dict[counter]].iloc[starting_line+1]
                            counter +=1

                        #adds the total HFO consumption from the HFO columns to the list
                        starting_line += 1
                    lng_sea_consumption.append(lng_temp_calculator)
            else:
                print("Overnight found")

        leg_counter+=1
        lastleg = leg

    return lng_sea_consumption

def func_get_ports(df):
    #reference list will have three elements, port name, index point, and number of lines referenced

    reference_list_ports = []
    i=0
    previous_port = ""
    port_day_counter = 0
    for port in df['Port']:
        if str(port) != "At Sea":
            if previous_port == port:
                #starts counting the number of duplicate days
                port_day_counter += 1
            else:
                if port_day_counter > 0:
                    #amends the last entry to have the
                    temp = reference_list_ports[-1]
                    reference_list_ports.pop()
                    reference_list_ports.append((str(temp[0]), temp[1], port_day_counter))
                port_day_counter = 0
                reference_list_ports.append((str(port),i,port_day_counter))
        i += 1
        previous_port = port
    return reference_list_ports


def func_calc_hfo_in_port(ports, df):
    hfo_port_consumption = []

    for port in ports:
        hfo_temp_calculator = 0
        days_in_port_remaining = port[2]
        starting_line = port[1]
        while days_in_port_remaining >= 0:
            counter = 0
            while counter < len(hfo_port_dict):
                hfo_temp_calculator += df[hfo_port_dict[counter]].iloc[starting_line+days_in_port_remaining]
                counter +=1
            days_in_port_remaining -= 1
        hfo_port_consumption.append(hfo_temp_calculator)

    return hfo_port_consumption

def func_calc_mgo_in_port(ports, df):
    mgo_port_consumption = []

    for port in ports:
        mgo_temp_calculator = 0
        days_in_port_remaining = port[2]
        starting_line = port[1]
        while days_in_port_remaining >= 0:
            counter = 0
            while counter < len(mgo_port_dict):
                mgo_temp_calculator += df[mgo_port_dict[counter]].iloc[starting_line+days_in_port_remaining]
                counter +=1
            days_in_port_remaining -= 1
        mgo_port_consumption.append(mgo_temp_calculator)

    return mgo_port_consumption

def func_calc_lng_in_port(ports, df):
    lng_port_consumption = []

    for port in ports:
        lng_temp_calculator = 0
        days_in_port_remaining = port[2]
        starting_line = port[1]
        while days_in_port_remaining >= 0:
            counter = 0
            while counter < len(lng_port_dict):
                lng_temp_calculator += df[lng_port_dict[counter]].iloc[starting_line+days_in_port_remaining]
                counter +=1
            days_in_port_remaining -= 1
        lng_port_consumption.append(lng_temp_calculator)

    return lng_port_consumption

def func_grab_HFO_consumption(df):
    HFO_AT_Sea = df['At Sea Consumption HFO']
    HFO_In_Port = df["In Port Consumption HFO"]
    return HFO_In_Port, HFO_AT_Sea

def func_grab_MGO_consumption(df):
    MGO_AT_Sea = df['At Sea Consumption MGO'] + df['MGO For LNG Ignition SEA']
    MGO_In_Port = df["In Port Consumption MGO"] + df['MGO For LNG Ignition PORT']
    return MGO_In_Port, MGO_AT_Sea

def func_grab_LNG_Consumption(df):
    LNG_AT_Sea = df['At Sea Consumption LNG']
    LNG_In_Port = df["In Port Consumption LNG"]
    return LNG_In_Port, LNG_AT_Sea