'''
---How to use---

After make PSO by MicrogridPSO_module.py

df ,total_check, variables =loop_flowchart(PSO)
'''

import numpy as np
import pandas as pd


# ? 太陽光の最大発電許容量PSO.pv_max(h)を求める関数
def pv_generate(PSO):
    PSO.pv = (PSO.pv_cap_max / PSO.pv_capacity_per_unit) * \
        PSO.np_PV_efficient[PSO.h]
    return PSO.pv


# ? 風力の最大発電許容量PSO.wind_max(h)を求める関数
def wind_generate(PSO):
    PSO.wind = (PSO.wind_cap_max / PSO.wind_capacity_per_unit) * \
        PSO.np_Wind_efficient[PSO.h]
    return PSO.wind


# ? タイムステップ1回分のフローチャート
def flowchart(PSO):

    # * initialize some parameters
    if PSO.h == 0:
        PSO.battery_need = 0
        PSO.p_battery = PSO.battery_cap_max * \
            PSO.initial_input_values["SOC_start[%]"]
        PSO.battery_max = PSO.battery_cap_max * \
            PSO.initial_input_values["SOC_max[%]"]
        PSO.battery_min = PSO.battery_cap_max * \
            PSO.initial_input_values["SOC_min[%]"]
    PSO.pv = pv_generate(PSO)
    PSO.wind = wind_generate(PSO)
    PSO.check = "True"
    PSO.p_diesel = 0
    PSO.trashed_power = 0
    PSO.battery_charging_power = 0
    PSO.battery_discharging_power = 0
    PSO.flowchart_root = str(PSO.h) + "h"
    # ? SOCは、0 < SOC < 1 の範囲
    SOC = (PSO.p_battery / PSO.battery_cap_max)

    # * 太陽光の発電量が需要より多いか確認
    if PSO.pv + PSO.wind > PSO.np_demand[PSO.h]:
        # * 風力発電が需要を上回るときの処理
        # * ディーゼルは必要ない
        PSO.Diesel_Cf = 0

        # * バッテリーに必要な電力を導出
        if SOC < PSO.initial_input_values["SOC_max[%]"]:
            # * バッテリーの充電が必要
            PSO.battery_need = PSO.battery_cap_max * \
                (PSO.initial_input_values["SOC_max[%]"] - SOC)
        else:
            PSO.battery_need = 0
            PSO.flowchart_root = str(
                PSO.h) + "h: " + "Fullcharge ,no diesel "

        if PSO.wind > PSO.np_demand[PSO.h]:
            # * バッテリのSOCを確認 max時よりより多いか確認
            if SOC > PSO.initial_input_values["SOC_max[%]"]:
                # * バッテリーを充電する必要がない
                PSO.wind = PSO.np_demand[PSO.h]
                PSO.pv = 0
            else:
                # * バッテリーを充電する必要がある
                # * バッテリーを目標値まで充電可能か判断 風力が充電する電力 PSO.battery_need
                if PSO.wind - PSO.np_demand[PSO.h] > PSO.battery_need:
                    # * 目標SOCまで風力発電だけで充電可能
                    PSO.wind = PSO.np_demand[PSO.h] + PSO.battery_need
                    PSO.pv = 0
                    PSO.flowchart_root = str(
                        PSO.h) + "h: " + "Battery charge only wind" + str(round(PSO.battery_need, 3))
                else:
                    # * 目標SOCまで充電できないので、足りない分、太陽光が使えるかチェック
                    PSO.battery_need_pv = PSO.battery_need - \
                        (PSO.wind - PSO.np_demand[PSO.h])
                    if PSO.pv > PSO.battery_need_pv:
                        # * PVで賄える
                        PSO.pv = PSO.battery_need_pv
                        PSO.flowchart_root = str(
                            PSO.h) + "h: " + "Battery charge wind and PV" + str(round(PSO.battery_need, 3))
                    else:
                        # * PVで賄えない場合、ともに最大出力であまりを充電
                        PSO.battery_need = PSO.pv + \
                            PSO.wind - PSO.np_demand[PSO.h]

        # * 風力発電が需要を上回らないときの処理、つまり、需要はカバーできるが、風力はフル出力でPVの発電量を調整
        else:
            # * バッテリーを充電する必要があるか確認
            if SOC > PSO.initial_input_values["SOC_max[%]"]:
                # * 充電する必要がなく、需要の不足分だけPVを発電する
                PSO.pv = PSO.np_demand[PSO.h] - PSO.wind
            else:
                # * 充電する必要があり、需要の不足分だけPVを発電した後、バッテリに充電する。
                if PSO.pv - (PSO.np_demand[PSO.h] -
                             PSO.wind) > PSO.battery_need:
                    # * 目標SOCまで充電できる
                    PSO.pv = PSO.np_demand[PSO.h] - PSO.wind + PSO.battery_need
                else:
                    # * 目標SOCまで充電できない
                    PSO.battery_need = PSO.pv + PSO.wind - PSO.np_demand[PSO.h]

    else:
        # * 太陽光と風力の発電量が需要より少ない時の処理
        # * ディーゼルを使うかチェック 当然、PSO.battery_need = 0
        PSO.battery_need = 0
        # * ディーゼルを使用しない。
        if PSO.p_battery - \
                PSO.battery_min > (PSO.np_demand[PSO.h] - PSO.pv - PSO.wind):
            PSO.battery_discharging_power = PSO.np_demand[PSO.h] - \
                PSO.pv - PSO.wind
            PSO.p_battery = PSO.p_battery - \
                (PSO.np_demand[PSO.h] - PSO.pv - PSO.wind)
            PSO.flowchart_root = str(PSO.h) + "h: " + "discharging " + str(
                round(PSO.np_demand[PSO.h] - PSO.pv - PSO.wind, 3)) + "[kWh]."
            PSO.Diesel_Cf = 0
        # * ディーゼルを使用する。
        else:
            PSO.battery_discharging_power = PSO.p_battery - PSO.battery_min
            PSO.p_diesel = PSO.np_demand[PSO.h] - PSO.pv - \
                PSO.wind - (PSO.p_battery - PSO.battery_min)
            # * ディーゼルの容量を超える場合はエラー
            if PSO.p_diesel > PSO.diesel_max:
                PSO.check = False
                PSO.flowchart_root = str(
                    PSO.h) + "h: " + "Error! diesel capacity is over!"
            # * ディーゼル使用可
            else:
                PSO.flowchart_root = str(
                    PSO.h) + "h: " + "discharging " + str(
                    round(
                        PSO.p_battery - PSO.battery_min,
                        3)) + "[kWh], diesel " + str(
                    round(
                        PSO.p_diesel,
                        3)) + "[kWh]."
                PSO.p_battery = PSO.battery_min
                """ TODO PSO.diesel_maxは大きすぎるため、ひとまず,rated output per unit=1.8に置き換え"""
                PSO.Diesel_fc = PSO.initial_cost_parameters["Diesel_Adg"] * \
                    1.8 + PSO.initial_cost_parameters["Diesel_Bdg"] * PSO.p_diesel
                PSO.Diesel_Cf = PSO.initial_cost_parameters["Diesel_Pf"] * \
                    PSO.Diesel_fc

    # print(PSO.p_battery, PSO.p_battery + PSO.battery_need)
    PSO.p_battery = PSO.p_battery + PSO.battery_need
    PSO.battery_charging_power = PSO.battery_need
    SOC = (PSO.p_battery / PSO.battery_cap_max)

    PSO.parameters = {"hour": PSO.h,
                      "pv": PSO.pv,
                      "pv+wind-demand": PSO.pv + PSO.wind - PSO.np_demand[PSO.h],
                      "wind": PSO.wind,
                      "battery state[kWh]": PSO.p_battery,
                      "battery state[%]": SOC * 100,
                      "demand": PSO.np_demand[PSO.h],
                      "diesel power": PSO.p_diesel,
                      "trashed power": PSO.trashed_power,
                      "Check": PSO.check,
                      "flowchart_root": PSO.flowchart_root,
                      "battery_charging_power": PSO.battery_charging_power,
                      "battery_discharging_power": PSO.battery_discharging_power,
                      "Diesel_Cf": PSO.Diesel_Cf}

    return PSO.parameters, PSO.check, PSO.flowchart_root


# ? トータルコスト計算関数
def calc_cost(variables, initial_cost_parameters):
    # * 年間総発電量を計算し、20列のベクトルにする
    Et = [
        variables["pv_power_sum"] + variables["wind_power_sum"] +
        variables["diesel_power_sum"] + variables["battery_discharging_power_sum"]
    ] * 20
    cost_parameters = {
        "(1+r)^t": (
            1 +
            np.array(
                initial_cost_parameters["r[yen/year]"]) ** initial_cost_parameters["operation_year"]).tolist(),
    }

    # TODO O&Mの計算法を修正
    SCL = (
        # * PV
        (variables["pv_cap_max"] / 1000 * np.array(initial_cost_parameters["It_PV_1kW[yen/year]"])
         + np.array([variables["pv_power_sum"]] * 20) * np.array(initial_cost_parameters["Mt_PV_1kW[yen/year]"]))
        # * Wind
        + (variables["wind_cap_max"] * np.array(initial_cost_parameters["It_Wind_1kW[yen/year]"])
            + np.array([variables["wind_power_sum"]] * 20) * np.array(initial_cost_parameters["Mt_Wind_1kW[yen/year]"]))
        # * Diesel
        + (variables["diesel_max"] * np.array(initial_cost_parameters["It_Diesel_1kW[yen/year]"])
            + np.array(initial_cost_parameters["Mt_Diesel_1kW[yen/year]"]) * (
                np.array([variables["wind_power_sum"]] * 20))
            + np.array(variables["Diesel_Cf_sum"] * 20))
        # Battery
        + (variables["battery_cap_max"]
           * np.array(initial_cost_parameters["It_Battery_1kW[yen/year]"]) + np.array(initial_cost_parameters["Mt_Battery_1kW[yen/year]"]))
        - np.array(variables["trashed_power_sum"] * 20) * np.array(
            initial_cost_parameters["Sell_income_from_trashed[kWh/yen]"])
    ) / cost_parameters["(1+r)^t"]

    SEL = np.array(Et) / cost_parameters["(1+r)^t"]
    COST = np.sum(SCL)
    return COST, SCL, SEL


def loop_flowchart(PSO):
    # * データフレームを作成
    PSO.df = pd.DataFrame()
    number_of_loops = len(PSO.Target_input.index)
    for PSO.h in range(number_of_loops):
        PSO.flowchart_parameters, PSO.check, PSO.flowchart_root = flowchart(
            PSO)

        if not PSO.check:
            print('      *', PSO.h, '[h]-----PSO.check is False.')
            print('      *', PSO.flowchart_root)
            print(
                '      *PSO.diesel_max | PSO.p_diesel |PSO.np_demand[PSO.h] | PSO.np_demand[PSO.h]-PSO.pv-PSO.wind |PSO.p_battery-PSO.battery_min')
            print('      *',
                  PSO.diesel_max,
                  PSO.p_diesel,
                  PSO.np_demand[PSO.h],
                  PSO.np_demand[PSO.h] - PSO.pv - PSO.wind,
                  PSO.p_battery - PSO.battery_min)
            Success_loops, Failed_loops = 0, 1
            PSO.total_check = False
            PSO.variables = "Error"
            PSO.total_cost = "Error"
            PSO.SCL, PSO.SEL = "Error", "Error"
            return PSO.df, PSO.total_check, PSO.variables, PSO.total_cost, PSO.SCL, PSO.SEL, Success_loops, Failed_loops

        PSO.p_battery = PSO.flowchart_parameters['battery state[kWh]']
        PSO.df = pd.concat(
            [PSO.df, pd.io.json.json_normalize(PSO.flowchart_parameters)])

    # * ループ内でfalseがあるかチェック　falseがあるとtotal_checkにfalseが入る。
    PSO.total_check = not(False in PSO.df['Check'].values)

    # * Count iterations of florchart
    Success_loops, Failed_loops = 0, 0
    if PSO.total_check:
        Success_loops = 1
    else:
        Failed_loops = 1

    PSO.variables = {
        "pv_cap_max": PSO.pv_cap_max,
        "wind_cap_max": PSO.wind_cap_max,
        "battery_cap_max": PSO.battery_cap_max,
        "battery_max": PSO.battery_max,
        "battery_min": PSO.battery_min,
        "diesel_max": PSO.diesel_max,
        "demand_sum": PSO.df['demand'].sum(),
        "pv_power_sum": PSO.df['pv'].sum(),
        "wind_power_sum": PSO.df['wind'].sum(),
        "battery_charging_power_sum": PSO.df['battery_charging_power'].sum(),
        "battery_discharging_power_sum": PSO.df['battery_discharging_power'].sum(),
        "diesel_power_sum": PSO.df['diesel power'].sum(),
        "trashed_power_sum": PSO.df['trashed power'].sum(),
        "Diesel_Cf_sum": PSO.df['Diesel_Cf'].sum()}

    PSO.total_cost, PSO.SCL, PSO.SEL = calc_cost(
        PSO.variables, PSO.initial_cost_parameters)
    return PSO.df, PSO.total_check, PSO.variables, PSO.total_cost, PSO.SCL, PSO.SEL, Success_loops, Failed_loops
