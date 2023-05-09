from Simulation import Simulation

params = {
    "rabbit_speed": 0.9,
    "fox_speed": 1.1,
    "rabbit_children": 2,
    "fox_children": 1
}

# params = {
#     "rabbit_speed": 0.86,
#     "fox_speed": 0.79,
#     "rabbit_children": 4
# }

sim = Simulation(200, 1, True, params)
print(sim.run())