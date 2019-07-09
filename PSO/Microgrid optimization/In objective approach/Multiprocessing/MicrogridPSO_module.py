import pandas as pd
import datetime


class MicrogridPSO_initialize:

    def __init__(self, Target_input):

        # input CSV
        self.Target_input = pd.read_csv(
            Target_input, encoding="UTF-8").set_index(['Time'])

        # get CSV column length
        self.Target_input_len = len(self.Target_input)

        self.Multiprocessing_parameters = {
            "n_iterations": 1,
            "n_particles": 1,
            "w": 1,
            "c1": 1,
            "c2": 1,
            "state_name": "[1,1,1,1,1]" + str(datetime.datetime.now())
        }

        # initial_cost_parameters
        self.initial_cost_parameters = {
            "It_PV_1kW[yen/year]": [726383.3333, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Mt_PV_1kW[yen/year]": [4329] * 20,
            "Ft_PV_1kW[yen/year]": [0] * 20,
            "It_Wind_1kW[yen/year]":
                [302274.7826, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "Mt_Wind_1kW[yen/year]": [662.785213] * 20,
            "Ft_Wind_1kW[yen/year]": [0] * 20,
            "It_Diesel_1kW[yen/year]":
                [33611.11, 33611.11, 0, 33611.11, 33611.11,
                 0, 33611.11, 33611.11, 0, 33611.11, 33611.11,
                 0, 33611.11, 33611.11, 0, 33611.11, 33611.11,
                 0, 33611.11, 33611.11],
            "Mt_Diesel_1kW[yen/year]": [8.8] * 20,
            "Diesel_Pf": 129,
            "Diesel_Adg": 0.2461,
            "Diesel_Bdg": 0.081451,
            "It_Battery_1kW[yen/year]":
                [13540, 0, 0, 0, 13540, 0, 0, 0, 13540, 0,
                 0, 0, 13540, 0, 0, 0, 13540, 0, 0, 0],
            "Mt_Battery_1kW[yen/year]": [1100] * 20,
            "Ft_Battery_1kW[yen/year]": [0] * 20,
            "Sell_income_from_trashed[kWh/yen]": [20] * 20,
            "r[yen/year]": [0.0234375] * 20,
            "operation_year": list(range(1, 21))}

        # initial_input_values
        self.h = 0
        self.initial_input_values = {
            "number_demand": 0,
            "pv_capacity_per_unit": 0,
            "wind_capacity_per_unit": 0,
            "SOC_max[%]": 1,
            "SOC_min[%]": 0,
            "SOC_start[%]": 0.5}

        # initial fitness variable parameters
        self.pv_cap_max = 0  # W
        self.wind_cap_max = 0  # kWh
        self.battery_cap_max = 0  # kWh
        self.diesel_max = 0  # kWh
        self.fitness_variable_parameters = {
            "pv_cap_max": self.pv_cap_max,
            "wind_cap_max": self.wind_cap_max,
            "battery_cap_max": self.battery_cap_max,
            "diesel_max": self.diesel_max}

    # set Multiprocessing_parameters
    def set_Multiprocessing_parameters(self, n_iterations, n_particles, w, c1, c2):
        self.Multiprocessing_parameters["n_iterations"] = n_iterations
        self.Multiprocessing_parameters["n_particles"] = n_particles
        self.Multiprocessing_parameters["w"] = w
        self.Multiprocessing_parameters["c1"] = c1
        self.Multiprocessing_parameters["c2"] = c2
        self.Multiprocessing_parameters["state_name"] = "[" + str(
            n_iterations) + "," + str(n_particles) + "," + str(w) + "," + str(c1) + "," + str(c2) + "]"

    # set initial_cost_parameters like self.initial_cost_parameters
    def set_initial_cost_parameters(self, initial_cost_parameters):
        self.initial_cost_parameters = initial_cost_parameters

    # set initial_input_values like self.initial_input_values
    def set_initial_input_values(self, initial_input_values):
        self.initial_input_values = initial_input_values
        self.number_demand = initial_input_values["number_demand"]
        self.SOC_max = initial_input_values["SOC_max[%]"]
        self.SOC_min = initial_input_values["SOC_min[%]"]
        self.pv_capacity_per_unit = initial_input_values["pv_capacity_per_unit"]
        self.wind_capacity_per_unit = initial_input_values["wind_capacity_per_unit"]
        self.np_demand = self.number_demand * \
            self.Target_input['Demand[kWh]'].values
        self.np_PV_efficient = self.Target_input['PV[Wh/unit]'].values / 1000
        self.np_Wind_efficient = self.Target_input['Wind[kWh/unit]'].values

    # update fitness_variable_parameters
    def update_fitness_variable_parameters(self, fitness_variable_parameters):
        self.pv_cap_max = fitness_variable_parameters['pv_cap_max']
        self.wind_cap_max = fitness_variable_parameters['wind_cap_max']
        self.battery_cap_max = fitness_variable_parameters['battery_cap_max']
        self.diesel_max = fitness_variable_parameters['diesel_max']

        self.fitness_variable_parameters = {
            "pv_cap_max": self.pv_cap_max,
            "wind_cap_max": self.wind_cap_max,
            "battery_cap_max": self.battery_cap_max,
            "diesel_max": self.diesel_max
        }
