#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Making module
import subprocess
import datetime
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import inspect


# In[2]:


class MicrogridPSO_initialize:

    def __init__(self, Target_input):

        # input CSV
        self.Target_input = pd.read_csv(
            "Target_input.csv", encoding="UTF-8").set_index(['Time'])

        # get CSV column length
        self.Target_input_len = len(self.Target_input)

        # initial_cost_parameters
        self.initial_cost_parameters = {"It_PV_1kW[yen/year]": [726383.3333,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                       "Mt_PV_1kW[yen/year]":[4329] * 20,
                                       "Ft_PV_1kW[yen/year]":[0]*20,
                                       "It_Wind_1kW[yen/year]": [302274.7826,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                       "Mt_Wind_1kW[yen/year]":[662.785213] * 20,
                                       "Ft_Wind_1kW[yen/year]":[0]*20,
                                       "It_Diesel_1kW[yen/year]": [33611.11,33611.11,0,33611.11,33611.11,0,33611.11,33611.11,0,33611.11,\
                                                                   33611.11,0,33611.11,33611.11,0,33611.11,33611.11,0,33611.11,33611.11],
                                       "Mt_Diesel_1kW[yen/year]":[8.8] * 20,
                                        "Diesel_Pf":129,
                                        "Diesel_Adg":0.2461,
                                        "Diesel_Bdg":0.081451,
                                       "It_Battery_1kW[yen/year]": [13540,0,0,0,13540,0,0,0,13540,0,0,0,13540,0,0,0,13540,0,0,0],
                                       "Mt_Battery_1kW[yen/year]":[1100] * 20,
                                       "Ft_Battery_1kW[yen/year]":[0]*20,
                                       "r[yen/year]":[0.0234375]*20,
                                       "operation_year":list(range(1,21))
                                        }

        # initial_input_values
        self.h = 0
        self.initial_input_values = {"number_demand": 0,
                                     "pv_capacity_per_unit": 0,
                                     "wind_capacity_per_unit": 0,
                                     "SOC_max[%]": 1,
                                     "SOC_min[%]": 0,
                                     "SOC_start[%]":0.5
                                     }

        # initial fitness variable parameters
        self.pv_cap_max = 0  # W
        self.wind_cap_max = 0  # kWh
        self.battery_cap_max = 0  # kWh
        self.diesel_max = 0  # kWh
        self.fitness_variable_parameters = {"pv_cap_max": self.pv_cap_max,
                                            "wind_cap_max": self.wind_cap_max,
                                            "battery_cap_max": self.battery_cap_max,
                                            "diesel_max": self.diesel_max
                                            }

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
        self.np_demand = self.number_demand *             self.Target_input['Demand[kWh]'].values
        self.np_PV_efficient = self.Target_input['Forecast_PV[Wh/unit]'].values/1000
        self.np_Wind_efficient = self.Target_input['Forecast_Wind[kWh/unit]'].values

    # update fitness_variable_parameters
    def update_fitness_variable_parameters(self, fitness_variable_parameters):
        self.pv_cap_max = fitness_variable_parameters['pv_cap_max']
        self.wind_cap_max = fitness_variable_parameters['wind_cap_max']
        self.battery_cap_max = fitness_variable_parameters['battery_cap_max']
        self.diesel_max = fitness_variable_parameters['diesel_max']

        self.fitness_variable_parameters = {"pv_cap_max": self.pv_cap_max,
                                            "wind_cap_max": self.wind_cap_max,
                                            "battery_cap_max": self.battery_cap_max,
                                            "diesel_max": self.diesel_max
                                            }

    # batery limitation calc
    def set_battery_limit(self):
        self.battery_max = self.initial_input_values["SOC_max[%]"] *             self.battery_cap_max
        self.battery_min = self.initial_input_values["SOC_min[%]"] *             self.battery_cap_max
        self.p_battery=self.initial_input_values["SOC_start[%]"]*self.battery_max


# In[3]:


'''
###inspect functions
print(inspect.getmembers(MicrogridPSO_initialize, inspect.isfunction))

###inspect methods
print(inspect.getmembers(MicrogridPSO_initialize, inspect.ismethod))

###inspect object & methods
print(dir(MicrogridPSO_initialize))
'''


# In[4]:


''' How to initialize
###Class check
PSO = MicrogridPSO_initialize("Target_input.csv")

PSO.set_initial_cost_parameters({'PV_investment[yen/kWh]': 20,
 'battery_investment[yen/kWh]': 50,
 'diesel_investment[yen/kWh]': 70})

PSO.set_initial_input_values({ "number_demand": 1,
                                      "pv_capacity_per_unit": 245,
                                      "SOC_max[%]": 0.9,
                                      "SOC_min[%]": 0.2,
                                      "SOC_start[%]":0.5
                                          } )

PSO.update_fitness_variable_parameters({'pv_cap_max': 245, 'battery_cap_max': 1, 'diesel_max': 5})

#PSO.initial_input_values
'''


# In[5]:


#.ipynb convert to .py
subprocess.run(['jupyter','nbconvert', '--to','python','MicrogridPSO_module.ipynb'])

