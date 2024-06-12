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

### Age Distribution
s = model.Society(initial_goats, initial_age)
s.next_month(simulation_duration)

data = s.age_distributions
xf, yf = np.unique(data[0], return_counts=True)
xm, ym = np.unique(data[1], return_counts=True)

print(f"Initial goats {initial_goats} (starting age: {initial_age})")
print(f"Simulating for {simulation_duration} months.")
print(f"\nFemales:")
print(f"\tAges   : {xf}")
print(f"\tCounts : {yf}")
print(f"\nMales:")
print(f"\tAges   : {xm}")
print(f"\tCounts : {ym}")

fig, ax = plt.subplots(1, 2, figsize=(12,5), constrained_layout=True)

ax[0].bar(xf, yf)
ax[0].set(xlim=(-5,144+5))
ax[0].set_title("Age distribution of female goats")
# ax[0].set_yticks([])

ax[1].bar(xm, ym)
ax[1].set(xlim=(-5,60+5))
ax[1].set_title("Age distribution of male goats")
# ax[1].set_yticks([])

plt.show()
