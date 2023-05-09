import random
from Simulation import Simulation
from threading import Thread

def GetStability(params, results_big):
    tries, cutoff_point = 10, 2000
    results = []

    for _ in range(tries):
        sim = Simulation(20, 4, False, params)
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

params = {
    "rabbit_speed": 0.9,
    "fox_speed": 1.1,
    "rabbit_children": 4,
    "fox_children": 1,
    "rabbit_reproductive": 400,
    "rabbit_life": 400,
    "fox_reproductive": 400,
    "fox_life": 800
}

def get_random_params():
    params = {
        "rabbit_speed": random.uniform(0.5, 1.5),
        "fox_speed": random.uniform(0.5, 2),
        "rabbit_children": random.randint(3, 6),
        "fox_children": 1,
        "rabbit_reproductive": random.randint(400, 800),
        "rabbit_life": random.randint(200, 1000),
        "fox_reproductive": random.randint(200, 1200),
        "fox_life": random.randint(600, 1200)
    }
    return [params, -1]


amount = 10
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
