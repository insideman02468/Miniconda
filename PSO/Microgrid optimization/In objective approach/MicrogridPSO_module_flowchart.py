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

def flowchart(PSO):

    # initialize some parameters
    PSO.pv = pv_generate(PSO)
    PSO.check = "True"
    PSO.p_diesel = 0
    PSO.trashed_power = 0
    PSO.battery_charging_power = 0
    PSO.battery_discharging_power = 0
    PSO.flowchart_root= str(PSO.h)+"h"
    # 太陽光の発電量が需要より多いか確認
    if PSO.pv > PSO.np_demand[PSO.h]:
        # 太陽光の発電量が需要より多い時の処理
        # バッテリーが過充電にならないかのチェック、過充電の場合、余った電気は捨てる。
        if PSO.p_battery+(PSO.pv-PSO.np_demand[PSO.h]) <= PSO.battery_max:
            PSO.p_battery = PSO.p_battery+(PSO.pv-PSO.np_demand[PSO.h])
            PSO.battery_charging_power=PSO.battery_charging_power+PSO.pv-PSO.np_demand[PSO.h]
            PSO.flowchart_root=str(PSO.h)+"h: "+"Battery charge without diesel."
        else:
            PSO.trashed_power = ((PSO.pv-PSO.np_demand[PSO.h])+PSO.p_battery) - PSO.battery_max
            PSO.battery_charging_power=PSO.battery_charging_power + (PSO.battery_max - PSO.p_battery)
            PSO.p_battery = PSO.battery_max
            PSO.flowchart_root=str(PSO.h)+"h: "+"Fullcharge ,no diesel, trashed "\
                 + str(round(PSO.trashed_power, 2))+"[kWh]."

    else:
        # 太陽光の発電量が需要より少ない時の処理
        # ディーゼルを使うかチェック
            #ディーゼルを使用しない。。
        if PSO.p_battery > (PSO.np_demand[PSO.h]-PSO.pv) and PSO.p_battery-(PSO.np_demand[PSO.h]-PSO.pv) > PSO.battery_min:
            PSO.battery_discharging_power=PSO.np_demand[PSO.h]-PSO.pv
            PSO.p_battery = PSO.p_battery-(PSO.np_demand[PSO.h]-PSO.pv)
            PSO.flowchart_root= str(PSO.h)+"h: "+"discharging " \
            + str(round(PSO.np_demand[PSO.h]-PSO.pv, 3) )+"[kWh]."
        else:   #ディーゼルを使用する。
            PSO.battery_discharging_power=PSO.p_battery-PSO.battery_min
            PSO.p_diesel = PSO.np_demand[PSO.h]-PSO.pv-(PSO.p_battery-PSO.battery_min)
            # ディーゼルの容量を超える場合はエラー
            if PSO.p_diesel > PSO.diesel_max:
                PSO.check = 'False'
                PSO.flowchart_root=str(PSO.h)+"h: "+"Error! diesel capacity is over!"
            else:
                PSO.flowchart_root= str(PSO.h)+"h: "+"discharging " + str(round(PSO.p_battery-PSO.battery_min, 3) )\
                      +"[kWh], diesel " + str( round(PSO.p_diesel, 3) ) +"[kWh]."
                PSO.p_battery = PSO.battery_min

    PSO.parameters = {"hour": PSO.h,
                  "pv": PSO.pv,
                  "pv-demand" :PSO.pv-PSO.np_demand[PSO.h],
                  "battery state[kWh]": PSO.p_battery,
                  "battery state[%]": (PSO.p_battery/PSO.battery_max)*100,
                  "demand": PSO.np_demand[PSO.h],
                  "diesel power": PSO.p_diesel,
                  "trashed power": PSO.trashed_power,
                  "Check":PSO.check,
                  "flowchart_root":PSO.flowchart_root,
                  "battery_charging_power":PSO.battery_charging_power,
                  "battery_discharging_power": PSO.battery_discharging_power
                    }

    return PSO.parameters, PSO.check, PSO.flowchart_root

def calc_cost(variables, initial_cost_parameters):
    #initial_cost_parameters["PV_cost[yen/kWh]"]
    #initial_cost_parameters["battery_cost[yen/kWh]"]
    #initial_cost_parameters["diesel_cost[yen/kWh]"]
    total_cost = variables["pv_power_sum"] * initial_cost_parameters["PV_cost[yen/kWh]"] \
                +(variables["battery_charging_power_sum"] + variables["battery_discharging_power_sum"] ) \
                * initial_cost_parameters["battery_cost[yen/kWh]"] \
                +variables["diesel_power_sum"] * initial_cost_parameters["diesel_cost[yen/kWh]"]

    return total_cost

def loop_flowchart(PSO):
    #からのデータフレームを作成
    PSO.df = pd.DataFrame()
    for PSO.h in range(24):
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
                 "battery_cap_max": PSO.battery_cap_max,
                 "battery_max": PSO.battery_max,
                 "battery_min": PSO.battery_min,
                 "diesel_max": PSO.diesel_max,
                 "demand_sum": PSO.df['demand'].sum(),
                 "pv_power_sum": PSO.df['pv'].sum(),
                 "battery_charging_power_sum":PSO.df['battery_charging_power'].sum(),
                 "battery_discharging_power_sum":PSO.df['battery_discharging_power'].sum(),
                 "diesel_power_sum": PSO.df['diesel power'].sum(),
                 "trashed_power_sum": PSO.df['trashed power'].sum()
                    }

    PSO.total_cost= calc_cost(PSO.variables, PSO.initial_cost_parameters)

    return PSO.df ,PSO.total_check, PSO.variables, PSO.total_cost, Success_loops, Failed_loops
