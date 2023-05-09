from Simulation import Simulation

params = {
    "rabbit_speed": 0.6,
    "fox_speed": 0.8,
    "rabbit_children": 4,
    "fox_children": 1,
    "rabbit_reproductive": 350,
    "rabbit_life": 550,
    "fox_reproductive": 1000,
    "fox_life": 900
}

# params = {
#     "rabbit_speed": 0.86,
#     "fox_speed": 0.79,
#     "rabbit_children": 4
# }

sim = Simulation(30, 4, True, params)
print(sim.run())