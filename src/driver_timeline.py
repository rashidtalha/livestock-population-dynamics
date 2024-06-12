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

### Timeline output
s = model.Society(initial_goats, initial_age)

data = np.zeros((4,simulation_duration+1))
for m in range(simulation_duration+1):
    data[0,m] = s.alive_females
    data[1,m] = s.alive_males
    data[2,m] = s.alive_females + s.alive_males
    data[3,m] = s.active_families
    s.next_month()

months = np.arange(simulation_duration+1)

print(f"Initial goats {initial_goats} (starting age: {initial_age})")
print(f"Simulating for {simulation_duration} months. (single run)")
print(f"Female goats at the end: alive = {s.alive_females}, dead = {s.dead_females}")
print(f"Male goats at the end: alive = {s.alive_males}, dead = {s.dead_males}")
print(f"Families at the end: active = {s.active_families}, inactive = {s.inactive_families}")

fig, ax = plt.subplots(1, 2, figsize=(9,5), constrained_layout=True)
ax[0].plot(months, data[0], label="female goats alive")
ax[0].plot(months, data[1], label="male goats alive")
ax[0].plot(months, data[2], label="total goats alive")
ax[0].set(xlim=(0,simulation_duration), ylim=(0,None))
ax[0].set_xlabel("months")
ax[0].set_title("Counts")
ax[0].legend()

ax[1].plot(months, data[3], label="total families active")
ax[1].set(xlim=(0,simulation_duration), ylim=(max(0, initial_goats-5),None))
ax[1].set_xlabel("months")
ax[1].set_title("Total families active")

plt.show()
