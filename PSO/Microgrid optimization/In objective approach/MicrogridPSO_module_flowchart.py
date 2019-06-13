'''
---How to use---

After make PSO by MicrogridPSO_module.py

df ,total_check, variables =loop_flowchart(PSO)
'''

import subprocess
import datetime
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import inspect

def pv_generate(PSO):
    PSO.pv=(PSO.pv_cap_max/PSO.pv_capacity_per_unit)*PSO.np_PV_efficient[PSO.h]
    return PSO.pv

def wind_generate(PSO):
    PSO.wind=(PSO.wind_cap_max/PSO.wind_capacity_per_unit)*PSO.np_Wind_efficient[PSO.h]
    return PSO.wind

def flowchart(PSO):

    # initialize some parameters
    PSO.pv = pv_generate(PSO)
    PSO.wind = wind_generate(PSO)
    PSO.check = "True"
    PSO.p_diesel = 0
    PSO.trashed_power = 0
    PSO.battery_charging_power = 0
    PSO.battery_discharging_power = 0
    PSO.flowchart_root= str(PSO.h)+"h"
    # 太陽光の発電量が需要より多いか確認
    if PSO.pv+PSO.wind > PSO.np_demand[PSO.h]:
        # 太陽光の発電量が需要より多い時の処理
        # バッテリーが過充電にならないかのチェック、過充電の場合、余った電気は捨てる。
        if PSO.p_battery+(PSO.pv+PSO.wind-PSO.np_demand[PSO.h]) <= PSO.battery_max:
            PSO.p_battery = PSO.p_battery+(PSO.pv+PSO.wind-PSO.np_demand[PSO.h])
            PSO.battery_charging_power=PSO.battery_charging_power+PSO.pv+PSO.wind-PSO.np_demand[PSO.h]
            PSO.flowchart_root=str(PSO.h)+"h: "+"Battery charge without diesel."
        else:
            PSO.trashed_power = ((PSO.pv+PSO.wind-PSO.np_demand[PSO.h])+PSO.p_battery) - PSO.battery_max
            PSO.battery_charging_power=PSO.battery_charging_power + (PSO.battery_max - PSO.p_battery)
            PSO.p_battery = PSO.battery_max
            PSO.flowchart_root=str(PSO.h)+"h: "+"Fullcharge ,no diesel, trashed "\
                 + str(round(PSO.trashed_power, 2))+"[kWh]."

    else:
        # 太陽光と風力の発電量が需要より少ない時の処理
        # ディーゼルを使うかチェック
            #ディーゼルを使用しない。。
        if PSO.p_battery > (PSO.np_demand[PSO.h]-PSO.pv-PSO.wind) and PSO.p_battery-(PSO.np_demand[PSO.h]-PSO.pv-PSO.wind) > PSO.battery_min:
            PSO.battery_discharging_power=PSO.np_demand[PSO.h]-PSO.pv-PSO.wind
            PSO.p_battery = PSO.p_battery-(PSO.np_demand[PSO.h]-PSO.pv-PSO.wind)
            PSO.flowchart_root= str(PSO.h)+"h: "+"discharging " \
            + str(round(PSO.np_demand[PSO.h]-PSO.pv-PSO.wind, 3) )+"[kWh]."
        else:   #ディーゼルを使用する。
            PSO.battery_discharging_power=PSO.p_battery-PSO.battery_min
            PSO.p_diesel = PSO.np_demand[PSO.h]-PSO.pv-PSO.wind-(PSO.p_battery-PSO.battery_min)
            # ディーゼルの容量を超える場合はエラー
            if PSO.p_diesel > PSO.diesel_max:
                PSO.check = 'False'
                PSO.flowchart_root=str(PSO.h)+"h: "+"Error! diesel capacity is over!"
            else:
                PSO.flowchart_root= str(PSO.h)+"h: "+"discharging " + str(round(PSO.p_battery-PSO.battery_min, 3) )\
                      +"[kWh], diesel " + str( round(PSO.p_diesel, 3) ) +"[kWh]."
                PSO.p_battery = PSO.battery_min
                
    PSO.Diesel_fc=PSO.initial_cost_parameters["Diesel_Adg"]*PSO.diesel_max+PSO.initial_cost_parameters["Diesel_Bdg"]*PSO.p_diesel
    PSO.Diesel_Cf=PSO.initial_cost_parameters["Diesel_Pf"]*PSO.Diesel_fc

    PSO.parameters = {"hour": PSO.h,
                  "pv": PSO.pv,
                  "pv+wind-demand" :PSO.pv+PSO.wind-PSO.np_demand[PSO.h],
                  "wind":PSO.wind,
                  "battery state[kWh]": PSO.p_battery,
                  "battery state[%]": (PSO.p_battery/PSO.battery_max)*100,
                  "demand": PSO.np_demand[PSO.h],
                  "diesel power": PSO.p_diesel,
                  "trashed power": PSO.trashed_power,
                  "Check":PSO.check,
                  "flowchart_root":PSO.flowchart_root,
                  "battery_charging_power":PSO.battery_charging_power,
                  "battery_discharging_power": PSO.battery_discharging_power,
                  "Diesel_Cf":PSO.Diesel_Cf
                    }

    return PSO.parameters, PSO.check, PSO.flowchart_root

def calc_cost(variables, initial_cost_parameters):
    Et = [variables["pv_power_sum"]+variables["wind_power_sum"] +
          variables["diesel_power_sum"]]*20
    cost_parameters = {
        "(1+r)^t": (1+np.array(initial_cost_parameters["r[yen/year]"]) ** initial_cost_parameters["operation_year"]).tolist(),
    }
    SCL = ((variables["pv_cap_max"]
         * (np.array(initial_cost_parameters["It_PV_1kW[yen/year]"])+np.array(initial_cost_parameters["Mt_PV_1kW[yen/year]"])))\
        + (variables["wind_cap_max"]\
        * (np.array(initial_cost_parameters["It_Wind_1kW[yen/year]"])+np.array(initial_cost_parameters["Mt_Wind_1kW[yen/year]"]))) \
        + (variables["diesel_max"]\
        * (np.array(initial_cost_parameters["It_Diesel_1kW[yen/year]"])+np.array(initial_cost_parameters["Mt_Diesel_1kW[yen/year]"]) ) ) \
        + (variables["battery_cap_max"]\
        * (np.array(initial_cost_parameters["It_Battery_1kW[yen/year]"])+np.array(initial_cost_parameters["Mt_Battery_1kW[yen/year]"]))) \
        +np.array(variables["Disel_Cf_sum"]*20)) \
        /cost_parameters["(1+r)^t"]
    
    SEL =np.array(Et)/cost_parameters["(1+r)^t"]
    LCOE=np.sum(SCL)/np.sum(SEL)
    return LCOE

def loop_flowchart(PSO):
    #からのデータフレームを作成
    PSO.df = pd.DataFrame()
    for PSO.h in range(len(PSO.Target_input.index)):
        PSO.flowchart_parameters, PSO.check, PSO.flowchart_root=flowchart(PSO)
        PSO.p_battery=PSO.flowchart_parameters['battery state[kWh]']
        PSO.df=pd.concat([PSO.df,pd.io.json.json_normalize(PSO.flowchart_parameters)])

    #ループ内でfalseがあるかチェック　falseがあるとtotal_checkにfalseが入る。
    PSO.total_check = not("False" in PSO.df['Check'].values)

    #Count itterations of flowchrt
    Success_loops, Failed_loops= 0, 0
    if PSO.total_check == True:
        Success_loops=1
    else:
        Failed_loops=1

    PSO.variables = {"pv_cap_max": PSO.pv_cap_max,
                     "wind_cap_max": PSO.wind_cap_max,
                 "battery_cap_max": PSO.battery_cap_max,
                 "battery_max": PSO.battery_max,
                 "battery_min": PSO.battery_min,
                 "diesel_max": PSO.diesel_max,
                 "demand_sum": PSO.df['demand'].sum(),
                 "pv_power_sum": PSO.df['pv'].sum(),
                 "wind_power_sum": PSO.df['wind'].sum(),
                 "battery_charging_power_sum":PSO.df['battery_charging_power'].sum(),
                 "battery_discharging_power_sum":PSO.df['battery_discharging_power'].sum(),
                 "diesel_power_sum": PSO.df['diesel power'].sum(),
                 "trashed_power_sum": PSO.df['trashed power'].sum(),
                 "Disel_Cf_sum":PSO.df['Diesel_Cf'].sum()
                    }

    PSO.total_cost= calc_cost(PSO.variables, PSO.initial_cost_parameters)

    return PSO.df ,PSO.total_check, PSO.variables, PSO.total_cost, Success_loops, Failed_loops
