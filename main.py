from Simulation import Simulation

params = {
    "rabbit_speed": 0.9,
    "fox_speed": 1.1,
    "rabbit_children": 4,
    "fox_children": 1,
    "rabbit_reproductive": 300,
    "rabbit_life": 400,
    "fox_reproductive": 400,
    "fox_life": 800
}

# params = {
#     "rabbit_speed": 0.86,
#     "fox_speed": 0.79,
#     "rabbit_children": 4
# }

sim = Simulation(20, 4, True, params)
print(sim.run())