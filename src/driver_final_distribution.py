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
model.prob_kids = [0, 0.1, 0.9]

### Simulation Parameters
simulation_duration = 12*5 # in months
initial_goats = 20 # in months
initial_age = 36 # in months

### Distribution output
runs = 500
data = np.zeros((5,runs))

for r in range(runs):
    s = model.Society(initial_goats, initial_age)
    s.next_month(simulation_duration)

    data[0,r] = s.alive_females
    data[1,r] = s.alive_males
    data[2,r] = s.alive_females + s.alive_males
    data[3,r] = s.active_families
    data[4,r] = s.inactive_families

norm_dist = lambda x, m, s: np.exp(-0.5 * ((x-m)/s)**2) / (s * np.sqrt(2*np.pi))
x = np.linspace(0, 1.05*max(data[2]), 500)

mu_0 = np.mean(data[0])
si_0 = np.std(data[0])

mu_1 = np.mean(data[1])
si_1 = np.std(data[1])

mu_2 = np.mean(data[2])
si_2 = np.std(data[2])

mu_3 = np.mean(data[3])
si_3 = np.std(data[3])

inact_st, inact_ct = np.unique(data[4], return_counts=True)

print(f"Initial goats {initial_goats} (starting age: {initial_age})")
print(f"Simulating for {simulation_duration} months. (Runs = {runs})")
print(f"Alive female goats: Mean = {mu_0:.0f}, Std = {si_0:.2f}")
print(f"Alive male goats: Mean = {mu_1:.0f}, Std = {si_1:.2f}")
print(f"Alive total goats: Mean = {mu_2:.0f}, Std = {si_2:.2f}")
print(f"Active families: Mean = {mu_3:.0f}, Std = {si_3:.2f}")
print(f"Inactive families: {inact_st} with counts {inact_ct}")

fig, ax = plt.subplots(2, 2, figsize=(10,8), constrained_layout=True)
ax[0,0].hist(data[0], density=True)
ax[0,0].plot(x, norm_dist(x, mu_0, si_0))
ax[0,0].axvline(mu_0, c="k")
ax[0,0].set(xlim=( 0.95*min(data[0]), 1.05*max(data[0] )))
ax[0,0].set_title("Female goats alive")
ax[0,0].set_yticks([])

ax[0,1].hist(data[1], density=True)
ax[0,1].plot(x, norm_dist(x, mu_1, si_1))
ax[0,1].axvline(mu_1, c="k")
ax[0,1].set(xlim=( 0.95*min(data[1]), 1.05*max(data[1] )))
ax[0,1].set_title("Male goats alive")
ax[0,1].set_yticks([])

ax[1,0].hist(data[2], density=True)
ax[1,0].plot(x, norm_dist(x, mu_2, si_2))
ax[1,0].axvline(mu_2, c="k")
ax[1,0].set(xlim=( 0.95*min(data[2]), 1.05*max(data[2])))
ax[1,0].set_title("All goats alive")
ax[1,0].set_yticks([])

ax[1,1].hist(data[3], density=True)
ax[1,1].set_title("Families active")
ax[1,1].set_yticks([])
plt.show()