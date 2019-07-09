from MicrogridPSO_module import MicrogridPSO_initialize
from MicrogridPSO_module_PSO import iterations_PSO
from MicrogridPSO_pareto_animation import Make_animation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from multiprocessing import Pool
import time


def Multifunc(x):

    # CSVを読み込みインスタンスを作成。
    PSO = MicrogridPSO_initialize("Target_input.csv")

    # 初期値を設定
    PSO.set_initial_input_values({
        "number_demand": 1,
        "pv_capacity_per_unit": 245,
        "wind_capacity_per_unit": 2.3,
        "SOC_max[%]": 0.8,
        "SOC_min[%]": 0.2,
        "SOC_start[%]": 0.5
    })

    # 初期値を設定
    PSO.set_initial_cost_parameters({
        "It_PV_1kW[yen/year]": [726383.3333, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Mt_PV_1kW[yen/year]": [4329] * 20,
        "Ft_PV_1kW[yen/year]": [0] * 20,
        "It_Wind_1kW[yen/year]": [302274.7826, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Mt_Wind_1kW[yen/year]": [662.785213] * 20,
        "Ft_Wind_1kW[yen/year]": [0] * 20,
        "It_Diesel_1kW[yen/year]": [33611.11, 33611.11, 0, 33611.11, 33611.11, 0, 33611.11, 33611.11, 0, 33611.11,
                                    33611.11, 0, 33611.11, 33611.11, 0, 33611.11, 33611.11, 0, 33611.11, 33611.11],
        "Mt_Diesel_1kW[yen/year]": [8.8] * 20,
        "Diesel_Pf": 129,
        "Diesel_Adg": 0.2461,
        "Diesel_Bdg": 0.081451,
        "It_Battery_1kW[yen/year]": [13540, 0, 0, 0, 13540, 0, 0, 0, 13540, 0, 0, 0, 13540, 0, 0, 0, 13540, 0, 0, 0],
        "Mt_Battery_1kW[yen/year]": [1100] * 20,
        "Ft_Battery_1kW[yen/year]": [0] * 20,
        "Sell_income_from_trashed[kWh/yen]": [0] * 20,
        "r[yen/year]": [0.0234375] * 20,
        "operation_year": list(range(1, 21))
    })

    PSO.Multiprocessing_parameters = {
        "n_iterations": 1,
        "n_particles": 1,
        "w": 1,
        "c1": 1,
        "c2": 1,
        "state_name": "[1,1,1,1,1]" + str(datetime.datetime.now())
    }

    parameters_list = [
        n_iterations_candidates[x],
        n_particles_candidates[x],
        w_particles_candidates[x],
        c1_particles_candidates[x],
        c2_particles_candidates[x]]

    PSO.set_Multiprocessing_parameters(parameters_list[0], parameters_list[1], parameters_list[2], parameters_list[3], parameters_list[4])

    iterations_PSO(PSO)

    # Result to CSV
    df = PSO.best['table']
    df.to_csv("Result/" +
              str(PSO.Multiprocessing_parameters["state_name"]) +
              'PSO_result_no_income.csv', encoding="SHIFT-JIS")

    # 試行結果をグラフ化
    plot_list = pd.DataFrame({'iteration': np.array(
        PSO.iteration_list) + 1, 'cost': np.array(PSO.best_cost_list)})
    plot_list.plot(
        x="iteration",
        y="cost",
        title='Total cost in each iteration')
    plt.savefig('Result/' +
                str(PSO.Multiprocessing_parameters["state_name"]) +
                'Total cost in each iteration.png')

    # COSTの整理
    COST_PV = (
        PSO.best["variables"]["pv_cap_max"] / 1000) * (
            np.array(
                PSO.initial_cost_parameters["It_PV_1kW[yen/year]"]) + np.array(
                    PSO.initial_cost_parameters["Mt_PV_1kW[yen/year]"]))
    COST_Wind = (PSO.best["variables"]["wind_cap_max"] *
                 (np.array(PSO.initial_cost_parameters["It_Wind_1kW[yen/year]"]) +
                     np.array(PSO.initial_cost_parameters["Mt_Wind_1kW[yen/year]"])))
    COST_Diesel = (
        PSO.best["variables"]["diesel_max"] * (
            np.array(
                PSO.initial_cost_parameters["It_Diesel_1kW[yen/year]"]) + np.array(
                    PSO.initial_cost_parameters["Mt_Diesel_1kW[yen/year]"]))) + np.array(
                        PSO.best["variables"]["Diesel_Cf_sum"] * 20)
    COST_Battery = PSO.best["variables"]["battery_cap_max"] * (
        np.array(
            PSO.initial_cost_parameters["It_Battery_1kW[yen/year]"]) + np.array(
                PSO.initial_cost_parameters["Mt_Battery_1kW[yen/year]"]))

    COST = {
        "COST PV": np.round(COST_PV, 2),
        "TOTAL COST PV": np.round(np.sum(COST_PV), 2),
        "LCOE PV": np.round(np.sum(COST_PV) / (20 * PSO.best["variables"]["pv_power_sum"]), 2),
        "COST Wind": np.round(COST_Wind, 2),
        "TOTAL COST Wind": np.round(np.sum(COST_Wind), 2),
        "LCOE WIND": np.round(np.sum(COST_Wind) / (20 * PSO.best["variables"]["wind_power_sum"]), 2),
        "COST DIESEL": np.round(COST_Diesel, 2),
        "TOTAL COST DIESEL": np.round(np.sum(COST_Diesel), 2),
        "LCOE DIESEL": np.round(np.sum(COST_Diesel) / (20 * PSO.best["variables"]["diesel_power_sum"]), 2),
        "COST BATTERY": np.round(COST_Battery, 2),
        "TOTAL COST BATTERY": np.round(np.sum(COST_Battery), 2),
        "LCOE BATTERY": np.round(np.sum(COST_Battery) / (20 * PSO.best["variables"]["battery_discharging_power_sum"]), 2),
    }

    # 計算結果テキストファイルの作成
    f = open('Result/' +
             str(PSO.Multiprocessing_parameters["state_name"]) +
             'PSO_result_parameters.txt', 'w')  # 書き込みモードで開く
    f_content = 'LCOE:' + str(
        np.sum(
            PSO.best['SCL']) / np.sum(
                PSO.best['SEL'])) + "COST:" + str(COST) + '\nglobal_best_position:' + str(
                    PSO.best['global_best_position']) + '\nglobal_best_fitness_value: ' + str(
                        PSO.best['global_best_fitness_value']) + "\nPSO.best[variables]:" + str(
                            PSO.best["variables"]) + '\nPSO.initial_cost_parameters:' + str(
                                PSO.initial_cost_parameters) + '\nSCL:' + str(
                                    PSO.best['SCL']) + '\nSEL:' + str(
                                        PSO.best['SEL'])
    f.write(f_content)  # 引数の文字列をファイルに書き込む
    f.close()  # ファイルを閉じる

    Make_animation("Result/" +
                   str(PSO.Multiprocessing_parameters["state_name"]) +
                   "all_particle_data_with_cost.npy", PSO)


if __name__ == "__main__":
    start = time.time()
    print('モジュール名：{}'.format(__name__))
    # Multiprocessingのコア数とハイパーパラメータの定義
    n_iterations_candidates = [20] * 16
    n_particles_candidates = [7] * 16
    w_particles_candidates = [0.6] * 16
    c1_particles_candidates = [0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5, 2.0, 2.0, 2.0, 2.0]
    c2_particles_candidates = [0.5, 1.0, 1.5, 2.0, 0.5, 1.0, 1.5, 2.0, 0.5, 1.0, 1.5, 2.0, 0.5, 1.0, 1.5, 2.0]
    core_number = 4
    p = Pool(core_number)
    p.map(Multifunc, range(len(n_iterations_candidates)))
    print("time:{}".format(time.time() - start))
