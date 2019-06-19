import numpy as np
from MicrogridPSO_module_flowchart import loop_flowchart

# Initialize particles & to input parameters


def initialize_PSO_parameters():
    # input initialize parametes
    n_iterations = int(input("Inform the number of iterations: "))
    n_particles = int(input("Inform the number of particles: "))
    w = float(input("Inform w: "))
    c1 = float(input("Inform c1: "))
    c2 = float(input("Inform c2: "))
    return n_iterations, n_particles, w, c1, c2

# 粒子の数を引数にして初期の粒子を作成する。「3次元」


def initialize__PSO_particles(n_particles):
    """
    ランダムな整数のバクトルを作成
    """
    velocity_vector = ([np.array([0, 0, 0, 0]) for _ in range(n_particles)])
    previous_velocity_vector = ([np.array([0, 0, 0, 0])
                                 for _ in range(n_particles)])
    iteration = 0
    personal_best_fitness_value = np.array([float('inf') for _ in range(n_particles)])

    global_best_fitness_value = float('inf')
    range_vector = [3000, 12, 25, 13]
    particle_position_vector = \
        np.array([np.array([np.random.rand() * range_vector[0], np.random.rand() * range_vector[1],
                            np.random.rand() * range_vector[2], np.random.rand() * range_vector[3]])
                  for _ in range(n_particles)])
    personal_best_position = particle_position_vector
    global_best_position = personal_best_position

    particle = {"particle_position_vector": particle_position_vector,
                "personal_best_position": personal_best_position,
                "personal_best_fitness_value": personal_best_fitness_value,
                "global_best_fitness_value": global_best_fitness_value,
                "global_best_position": global_best_position,
                "velocity_vector": velocity_vector,
                "previous_velocity_vector": previous_velocity_vector,
                "iteration": iteration,
                "range_vector": range_vector
                }
    return particle


# 制約条件関数
def constrained(position):
    x = position[0]
    y = position[1]
    z = position[2]
    v = position[3]
    if 7000 > x > 0 and 15 > y > 0 and 40 > z > 0 and 15 > v > 0:
        judge = True
    else:
        judge = False
    return judge


# Find optimized cost configurations.
def iterations_PSO(PSO):
    # initialized particle
    n_iterations, n_particles, w, c1, c2 = initialize_PSO_parameters()
    PSO.particle = initialize__PSO_particles(n_particles)

    print(
        PSO.fitness_variable_parameters,
        "\niterations:",
        n_iterations,
        "n_particles:",
        n_particles,
        "w:",
        w,
        "c1:",
        c1,
        "c2:",
        c2,
        "particle:",
        PSO.particle)

# PSO calc

    particle_position_vector = PSO.particle["particle_position_vector"]
    personal_best_position = PSO.particle["personal_best_position"]
    personal_best_fitness_value = PSO.particle["personal_best_fitness_value"]
    global_best_fitness_value = PSO.particle["global_best_fitness_value"]
    global_best_position = PSO.particle["global_best_position"]
    previous_velocity_vector = PSO.particle["previous_velocity_vector"]
    iteration = PSO.particle["iteration"]
    original_particle_position_vector = np.array([0, 0, 0, 0])
    original_previous_velocity_vector = np.array([0, 0, 0, 0])
    PSO.global_best_list = []
    PSO.iteration_list = []
    PSO.best_cost_list = []

    while iteration < n_iterations:
        print('-------iteration', '=', str(iteration), '-----------')
        print(str(particle_position_vector))
        for i in range(n_particles):
            # 粒子を設備容量に格納する。
            PSO.update_fitness_variable_parameters(
                {'pv_cap_max': particle_position_vector[i][0],
                 'wind_cap_max': particle_position_vector[i][1],
                 'battery_cap_max': particle_position_vector[i][2],
                 'diesel_max': particle_position_vector[i][3]})

            # total_checkのリセット
            total_check = True

            # フローチャートをループで回して計算結果を取得
            df, total_check, variables, total_cost, PSO.SCL, PSO.SEL, success_loops, failed_loops = loop_flowchart(
                PSO)

            # whileループの回数をリセット
            loop_number = 1
            # フローチャートもしくは、制約条件にエラーがある場合、粒子の位置をランダムにリセット
            while total_check is False or constrained(
                    particle_position_vector[i]) is False:

                print('      *particle_position_vector is error.loop=',
                      loop_number, particle_position_vector[i])

                '''
                particle_position_vector[i] = [np.random.rand()*PSO.particle["range_vector"][0], np.random.rand()*PSO.particle["range_vector"][1],\
                                               np.random.rand()*PSO.particle["range_vector"][2], np.random.rand()*PSO.particle["range_vector"][3]]
                '''

                if iteration == 0:
                    particle_position_vector[i] = [
                        np.random.rand() * PSO.particle["range_vector"][0],
                        np.random.rand() * PSO.particle["range_vector"][1],
                        np.random.rand() * PSO.particle["range_vector"][2],
                        np.random.rand() * PSO.particle["range_vector"][3]]
                    loop_number += 1
                else:
                    if loop_number == 1:
                        original_particle_position_vector = particle_position_vector[i]
                        original_previous_velocity_vector = previous_velocity_vector[i]
                        print(
                            '      *original_particle_position_vector',
                            original_particle_position_vector)
                        print(
                            '      *original_previous_velocity_vector',
                            original_previous_velocity_vector)
                    new_velocity = (
                        w * original_previous_velocity_vector) + (
                        c1 * np.random.rand()) * (
                        personal_best_position[i] - original_particle_position_vector) + (
                        c2 * np.random.rand()) * (
                        global_best_position - original_particle_position_vector)
                    particle_position_vector[i] = new_velocity + \
                        original_particle_position_vector
                    # ループが３回以上続く場合、ポジションをリセット
                    if loop_number >= 3:
                        particle_position_vector[i] = [
                            np.random.rand() * PSO.particle["range_vector"][0],
                            np.random.rand() * PSO.particle["range_vector"][1],
                            np.random.rand() * PSO.particle["range_vector"][2],
                            np.random.rand() * PSO.particle["range_vector"][3]]
                    print(
                        '      *loop=',
                        loop_number,
                        'new_velocity:',
                        new_velocity,
                        'original_particle_position_vector',
                        original_particle_position_vector)
                    loop_number += 1

                print(
                    '      *particle_position_vector is updated by error.',
                    particle_position_vector[i])

                # 粒子を設備容量に格納する。
                PSO.update_fitness_variable_parameters(
                    {'pv_cap_max': particle_position_vector[i][0],
                     'wind_cap_max': particle_position_vector[i][1],
                     'battery_cap_max': particle_position_vector[i][2],
                     'diesel_max': particle_position_vector[i][3]})

                # Total_checkのリセット
                total_check = True

                # フローチャートをループで回して計算結果を取得
                df, total_check, variables, total_cost, PSO.SCL, PSO.SEL, success_loops, failed_loops = loop_flowchart(
                    PSO)

            # フローチャートがエラーなく動く場合、PSOに進む。
            # かつ、制約条件をクリアしている時
            if total_check and constrained(particle_position_vector[i]):
                fitness_cadidate = total_cost
                print(
                    '-----particle_position[',
                    str(i),
                    '] ',
                    fitness_cadidate,
                    '[yen]. ',
                    particle_position_vector[i])

                if(personal_best_fitness_value[i] > fitness_cadidate):
                    personal_best_fitness_value[i] = fitness_cadidate
                    personal_best_position[i] = particle_position_vector[i]

                if(global_best_fitness_value > fitness_cadidate):
                    global_best_fitness_value = fitness_cadidate
                    global_best_position = particle_position_vector[i]
                    PSO.best = {'iterations': iteration,
                                'particle_number': i,
                                'global_best_position': global_best_position,
                                'global_best_fitness_value': global_best_fitness_value,
                                'table': df,
                                "variables": variables,
                                "SCL": PSO.SCL,
                                "SEL": PSO.SEL
                                }

            if iteration != 0:
                previous_velocity_vector[i] = new_velocity
            new_velocity = (w * previous_velocity_vector[i]) + (c1 * np.random.rand()) * (
                personal_best_position[i] - particle_position_vector[i]) + (c2 * np.random.rand()) * (global_best_position - particle_position_vector[i])
            new_position = new_velocity + particle_position_vector[i]
            particle_position_vector[i] = new_position
            print(
                '      *previous_velocity_vector[',
                i,
                ']',
                previous_velocity_vector[i],
                'new_velocity',
                new_velocity)
            previous_velocity_vector[i] = new_velocity
            print('      *particle_position_vector[',
                  str(i),
                  '] is updated. particle_position:',
                  str(particle_position_vector[i]))

        # 書くイテレーションの値をリストに保存
        PSO.global_best_list.append(global_best_position)
        PSO.iteration_list.append(iteration)
        PSO.best_cost_list.append(global_best_fitness_value)

        iteration = iteration + 1

    print(
        "The best position is ",
        global_best_position,
        " and global_best_fitness_value is",
        global_best_fitness_value,
        " in iteration number ",
        iteration,
        "and ",
        n_particles,
        "particles.")

    return PSO
