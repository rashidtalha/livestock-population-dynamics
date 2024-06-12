import numpy as np
import matplotlib.pyplot as plt

import model

# ### Model Parameters
# model.tau_m = 60
# model.tau_f = 144
# model.tau_start = 24
# model.tau_end = 120
# model.tau_preg = 7
# model.tau_gap = 5
# model.prob_start = 0.95
# model.prob_end = 0.93
# model.prob_female = 0.5
# model.prob_preg = 0.9
# model.prob_kids = [0.35, 0.45, 0.20]

### Simulation Parameters
simulation_duration = 12*4 # in months
initial_goats = 50 # in months
initial_age = 36 # in months

### Running the Simulation
s = model.Society(initial_goats, initial_age)
print(f"After {0:>2} months: {s.alive_females} ({s.dead_females}), {s.alive_males} ({s.dead_males}), {s.alive_females + s.alive_males} ({s.dead_females+s.dead_males}), {s.active_families} ({s.inactive_families})")

for m in range(simulation_duration):
    s.next_month()
    print(f"After {m+1:>2} months: {s.alive_females} ({s.dead_females}), {s.alive_males} ({s.dead_males}), {s.alive_females + s.alive_males} ({s.dead_females+s.dead_males}), {s.active_families} ({s.inactive_families})")
