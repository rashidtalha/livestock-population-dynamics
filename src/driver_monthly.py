import numpy as np
import matplotlib.pyplot as plt

import model

### Model Parameters
model.tau_m = 60
model.tau_f = 144
model.tau_start = 24
model.tau_end = 120
model.tau_preg = 7
model.tau_gap = 5
model.prob_start = 0.95
model.prob_end = 0.93
model.prob_female = 0.5
model.prob_preg = 0.9
model.prob_kids = [0.35, 0.45, 0.20]

### Simulation Parameters
simulation_duration = 12*5 # in months
initial_goats = 10 # in months
initial_age = 36 # in months

### Running the Simulation
s = model.Society(initial_goats, initial_age)
print(f"After {0:>2} months: {s.alive_females:3} ({s.dead_females:3}), {s.alive_males:3} ({s.dead_males:3}), {s.alive_females + s.alive_males:3} ({s.dead_females+s.dead_males:3}), {s.active_families:3} ({s.inactive_families:1})")

for m in range(simulation_duration):
    s.next_month()
    print(f"After {m+1:>2} months: {s.alive_females:3} ({s.dead_females:3}), {s.alive_males:3} ({s.dead_males:3}), {s.alive_females + s.alive_males:3} ({s.dead_females+s.dead_males:3}), {s.active_families:3} ({s.inactive_families:1})")
