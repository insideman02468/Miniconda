import subprocess
import datetime
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import inspect
import random
from MicrogridPSO_module_flowchart import *

#Initialize particles & to input parameters
def intialize_PSO_parameters():
    #input initialize parametes
    n_iterations = int(input("Inform the number of iterations: "))
    n_particles = int(input("Inform the number of particles: "))
    w = float(input("Inform w: "))
    c1 = float(input("Inform c1: "))
    c2 = float(input("Inform c2: "))
    return n_iterations, n_particles, w, c1, c2

#粒子の数を引数にして初期の粒子を作成する。「3次元」
def intialize__PSO_particles(n_particles):
    """
    ランダムな整数のバクトルを作成
    """
    particle_position_vector = \
    np.array([np.array([random.random()*500000, random.random()*100, random.random()*100]) \
              for _ in range(n_particles)])
    pbest_position = particle_position_vector

    pbest_fitness_value = np.array([float('inf') for _ in range(n_particles)])
    gbest_fitness_value = float('inf')
    gbest_position = pbest_position

    velocity_vector = ([np.array([0, 0, 0]) for _ in range(n_particles)])
    previous_velocity_vector = ([np.array([0, 0, 0]) for _ in range(n_particles)])
    iteration = 0

    particle = {  "particle_position_vector": particle_position_vector,
                  "pbest_position": pbest_position,
                  "pbest_fitness_value" :pbest_fitness_value,
                  "gbest_fitness_value": gbest_fitness_value,
                  "gbest_position": gbest_position,
                  "velocity_vector": velocity_vector,
                  "previous_velocity_vector": previous_velocity_vector,
                  "iteration": iteration,
                    }

    return particle

def constrained(position):
    x=position[0]
    y=position[1]
    z=position[2]
    if 500000> x > 0 and 100>y>0 and 100 > z > 0:
        judge=True
    else:
        judge=False
    return judge



#Find optimized cost configurations.
def iterations_PSO(PSO):
    #initialized particle
    n_iterations, n_particles, w, c1, c2 = intialize_PSO_parameters()
    PSO.particle = intialize__PSO_particles(n_particles)

    print(PSO.fitness_variable_parameters, "\niterations:", n_iterations, "n_particles:" \
    ,n_particles, "w:", w,"c1:", c1,"c2:", c2,\
    "particle:",PSO.particle)

#PSO calc

    particle_position_vector=PSO.particle["particle_position_vector"]
    pbest_position=PSO.particle["pbest_position"]
    pbest_fitness_value=PSO.particle["pbest_fitness_value"]
    gbest_fitness_value=PSO.particle["gbest_fitness_value"]
    gbest_position=PSO.particle["gbest_position"]
    velocity_vector=PSO.particle["velocity_vector"]
    previous_velocity_vector=PSO.particle["previous_velocity_vector"]
    iteration=PSO.particle["iteration"]
    constrained_iteration = 0
    PSO.gbest_list=[]
    PSO.iteration_list=[]
    PSO.best_cost_list=[]

    while iteration < n_iterations:
        print('-------iteration','=',str(iteration),'-----------')
    #print("function cost =", fitness_function(gbest_position), "in iteration number ", iteration)
        for i in range(n_particles):
            #粒子を設備容量に格納する。
            PSO.update_fitness_variable_parameters(\
                {'pv_cap_max': particle_position_vector[i][0], \
                'battery_cap_max': particle_position_vector[i][1], \
                'diesel_max': particle_position_vector[i][2]})

            #毎回、容量が変わるのでバッテリーのリミットを更新
            PSO.set_battery_limit()

            #フローチャートをループで回して計算結果を取得
            df, total_check, variables, total_cost ,success_loops, failed_loops = loop_flowchart(PSO)

            #フローチャートもしくは、制約条件にエラーがある場合、粒子の位置をランダムにリセット
            while total_check == False or constrained(particle_position_vector[i]) == False:
                print('particle_position_vector is errored')
                particle_position_vector[i] = [random.random()*500000, random.random()*100, random.random()*100]
                #粒子を設備容量に格納する。
                PSO.update_fitness_variable_parameters(\
                    {'pv_cap_max': particle_position_vector[i][0], \
                    'battery_cap_max': particle_position_vector[i][1], \
                    'diesel_max': particle_position_vector[i][2]})

                #毎回、容量が変わるのでバッテリーのリミットを更新
                PSO.set_battery_limit()

                #フローチャートをループで回して計算結果を取得
                df, total_check, variables, total_cost ,success_loops, failed_loops = loop_flowchart(PSO)

            #フローチャートがエラーなく動く場合、PSOに進む。
            #かつ、制約条件をクリアしている時
            if total_check == True and constrained(particle_position_vector[i]) == True:
                fitness_cadidate = total_cost
                print('    particle_position[',str(i),'] ',fitness_cadidate, 'particle_vector[',str(i),'] ', particle_position_vector[i])

                if(pbest_fitness_value[i] > fitness_cadidate):
                    pbest_fitness_value[i] = fitness_cadidate
                    pbest_position[i] = particle_position_vector[i]

                if(gbest_fitness_value > fitness_cadidate):
                    gbest_fitness_value = fitness_cadidate
                    gbest_position = particle_position_vector[i]
                    PSO.best = {'iterations': iteration , \
                                'particle_number': i,\
                                'gbest_position': gbest_position,\
                                'gbest_fitness_value': gbest_fitness_value,\
                                'table': df
                                }

        for i in range(n_particles):
            if iteration == 0:
                previous_velocity_vector[i] = velocity_vector[i]
            new_velocity = (w*previous_velocity_vector[i]) + (c1*random.random()) * (pbest_position[i] - particle_position_vector[i]) + (c2*random.random()) * (gbest_position-particle_position_vector[i])
            new_position = new_velocity + particle_position_vector[i]
            particle_position_vector[i] = new_position
            previous_velocity_vector[i]=new_velocity

        #書くイテレーションの値をリストに保存
        PSO.gbest_list.append(gbest_position)
        PSO.iteration_list.append(iteration)
        PSO.best_cost_list.append(gbest_fitness_value)

        iteration = iteration + 1

    print("The best position is ", gbest_position,\
        " and gbest_fitness_value is", gbest_fitness_value, \
        " in iteration number ", iteration, "and ", n_particles, "particles.")
