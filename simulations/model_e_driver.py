import numpy as np
import matplotlib.pyplot as plt

import model_e as model

# model.tau_m = 60
# model.tau_f = 144
# model.tau_start = 24
# model.tau_end = 120
# model.tau_preg = 5
# model.tau_gap = 2
# model.prob_start = 0.95
# model.prob_end = 0.93
# model.prob_female = 0.5
# model.prob_preg = 0.9
# model.prob_kids = [0.4, 0.3, 0.2, 0.1]

simulation_duration = 12*5 # in months
initial_goats = 10 # in months
initial_age = 24 # in months

# ### Simple output
# s = model.Society(initial_goats, initial_age)
# print(f"After {0:>2} months: {s.alive_goats}, {sum(s.alive_goats)}, {s.active_families}")

# for m in range(simulation_duration):
#     s.evolve_month()
#     print(f"After {m+1:>2} months: {s.alive_goats}, {sum(s.alive_goats)}, {s.active_families}")

# ### Timeline output
# s = model.Society(initial_goats, initial_age)

# data = np.zeros((4,simulation_duration+1))
# data[0,0] = s.alive_goats[0]
# data[1,0] = s.alive_goats[1]
# data[2,0] = sum(s.alive_goats)
# data[3,0] = s.active_families
# for m in range(simulation_duration):
#     s.evolve_month()
#     data[0,m+1] = s.alive_goats[0]
#     data[1,m+1] = s.alive_goats[1]
#     data[2,m+1] = sum(s.alive_goats)
#     data[3,m+1] = s.active_families

# months = np.arange(simulation_duration+1)

# fig, ax = plt.subplots()
# ax.plot(months, data[0], label="female goats alive")
# ax.plot(months, data[1], label="male goats alive")
# ax.plot(months, data[2], label="total goats alive")
# # ax.plot(months, data[3], label="total families active")

# ax.set(xlim=(0,simulation_duration), ylim=(0,None))
# ax.legend()
# plt.show()

### Distribution output
runs = 500
data = np.zeros((4,runs))

for r in range(runs):
    s = model.Society(initial_goats, initial_age)
    for _ in range(simulation_duration):
        s.evolve_month()

    data[0,r] = s.alive_goats[0]
    data[1,r] = s.alive_goats[1]
    data[2,r] = sum(s.alive_goats)
    data[3,r] = s.active_families


norm_dist = lambda x, m, s: np.exp(-0.5 * ((x-m)/s)**2) / (s * np.sqrt(2*np.pi))
x = np.linspace(0,max(data[0])*2,200)
# q = np.linspace(0,max(data[2])*2,200)

mu_0 = np.mean(data[0])
si_0 = np.std(data[0])

mu_1 = np.mean(data[1])
si_1 = np.std(data[1])

mu_2 = np.mean(data[2])
si_2 = np.std(data[2])

print(f"F: Mean = {mu_0:.3f}, Std = {si_0:.3f}")
print(f"M: Mean = {mu_1:.3f}, Std = {si_1:.3f}")
print(f"T: Mean = {mu_2:.3f}, Std = {si_2:.3f}")

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
ax[1,0].set(xlim=( 0.95*min(data[2]), 1.05*max(data[2] )))
ax[1,0].set_title("All goats alive")
ax[1,0].set_yticks([])

ax[1,1].hist(data[3], density=True)
ax[1,1].set_title("Families active")
ax[1,1].set_yticks([])
plt.show()