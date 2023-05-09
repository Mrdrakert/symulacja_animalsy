import random
from Simulation import Simulation
from threading import Thread

def GetStability(params, results_big):
    tries, cutoff_point = 10, 2000
    results = []

    for _ in range(tries):
        sim = Simulation(200, 8, False, params)
        results.append(sim.run())
    
    suma = 0
    for res in results:
        if (res > cutoff_point):
            suma += cutoff_point * 1.2
        else:
            suma += res
    result = suma / len(results)
    results_big.append([params, result])
    print("xded")

def get_random_params():
    params = {
        "rabbit_speed": random.uniform(0.5, 1.5),
        "fox_speed": random.uniform(0.5, 2),
        "rabbit_children": random.randint(1, 4)
    }
    return [params, -1]


amount = 20
generation = []

for i in range(amount):
    generation.append( get_random_params() )

threads = []
results = []

for i in range(amount):
    thread = Thread(target = GetStability, args = (generation[i][0], results))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


print(sorted(results, key=lambda x: x[1]))
