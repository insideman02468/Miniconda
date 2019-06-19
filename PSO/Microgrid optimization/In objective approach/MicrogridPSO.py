from MicrogridPSO_module import MicrogridPSO_initialize
from MicrogridPSO_module_PSO import iterations_PSO
import numpy as np

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

# 計算結果を実行
iterations_PSO(PSO)

# Result to CSV
df = PSO.best['table']
df.to_csv('PSO_result_no_income.csv', encoding="SHIFT-JIS")

# 計算結果テキストファイルの作成
f = open('PSO_result_parameters.txt', 'w')  # 書き込みモードで開く
f_content = 'LCOE=' + str(np.sum(PSO.best['SCL']) / np.sum(PSO.best['SEL'])) + ' global_best_position: ' + str(PSO.best['global_best_position']) + ' global_best_fitness_value: ' + str(
    PSO.best['global_best_fitness_value']) + str(PSO.variables) + str(PSO.initial_cost_parameters) + str(PSO.initial_cost_parameters)
f.write(f_content)  # 引数の文字列をファイルに書き込む
f.close()  # ファイルを閉じる
