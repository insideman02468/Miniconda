from MicrogridPSO_module import *
from MicrogridPSO_module_flowchart import *
from MicrogridPSO_module_PSO import *

#CSVを読み込みインスタンスを作成。
PSO = MicrogridPSO_initialize("Target_input.csv")

#初期値を設定
PSO.set_initial_input_values({"number_demand": 10,
                              "pv_capacity_per_unit": 245,
                              "SOC_max[%]": 0.9,
                              "SOC_min[%]": 0.2,
                              "SOC_start[%]": 0.5
                              })
#初期値を設定
PSO.set_initial_cost_parameters({'PV_cost[yen/kWh]': 40,
                                 'battery_cost[yen/kWh]': 100,
                                 'diesel_cost[yen/kWh]': 140})

# PSOの中身を確認
# print(dir(PSO))
#print(vars(PSO))

iterations_PSO(PSO)

df=PSO.best['table']

best_cost_list=np.array(PSO.best_cost_list)
gbest_list=np.array(PSO.gbest_list)
iteration_list=np.array(PSO.iteration_list)
plot_list = pd.DataFrame({ 'iteration' : np.array(PSO.iteration_list),
                           'cost' :np.array(PSO.best_cost_list)})
print(max(best_cost_list), min(best_cost_list))

plt.figure(figsize=(18,15))
#subplot(3,3,1)
plt.subplot(3,1,1)
plt.bar(df["hour"],df["pv"],label="pv output")
plt.bar(df["hour"],df["diesel power"],bottom=df["pv"],label="diesel power")
plt.bar(df["hour"],df["battery_discharging_power"],bottom=df["pv"]+df["diesel power"],label="battery_discharge")
plt.plot(df["hour"],df["battery_charging_power"],label="battery_charge" ,lw=2, color="red")
plt.bar(df["hour"],df["trashed power"], bottom=df["pv"]+df["diesel power"]+df["battery_discharging_power"],label="trashed power")
plt.plot(df["hour"],df["demand"],label="demand", lw=3, color="gray")
plt.xlabel("hour[H]")
plt.ylabel("pv output[kWh]")
plt.title("pv output")
plt.legend(loc="upper left")

#subplot(3,3,2)
plt.subplot(3,1,2)
plt.bar(df["hour"],df["battery state[%]"],label="battery state[%]")
plt.xlabel("hour[H]")
plt.ylabel("battery state[%]")
plt.title("battery state[%]")
plt.legend(loc="upper right")

#subplot(3,3,3)
plt.subplot(3,1,3)
plt.bar(df["hour"],PSO.np_PV_efficient,label="pv output per unit",color="red")
plt.legend(loc="upper left")
plt.xlabel("hour[H]")
plt.title("pv output per unit")
plt.ylabel("pv output per unit[kWh]")
plt.show


plot_list

plot_list.plot(y="cost")

plt.show()