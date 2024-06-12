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

### Simple output 1
s = model.Society(initial_goats, initial_age)
print(f"After {0:>2} months: {s.alive_females} ({s.dead_females}), {s.alive_males} ({s.dead_males}), {s.alive_females + s.alive_males} ({s.dead_females+s.dead_males}), {s.active_families} ({s.inactive_families})")

for m in range(simulation_duration):
    s.next_month()
    print(f"After {m+1:>2} months: {s.alive_females} ({s.dead_females}), {s.alive_males} ({s.dead_males}), {s.alive_females + s.alive_males} ({s.dead_females+s.dead_males}), {s.active_families} ({s.inactive_families})")


# ### Age Distribution
# s = model.Society(initial_goats, initial_age)
# print(f"After {0:>2} months: {s.alive_females}, {s.alive_males}, {s.alive_females + s.alive_males}, {s.active_families}")

# for m in range(simulation_duration):
#     s.next_month()
#     print(f"After {m+1:>2} months: {s.alive_females}, {s.alive_males}, {s.alive_females + s.alive_males}, {s.active_families}")

# data = s.age_distributions
# xf, yf = np.unique(data[0], return_counts=True)
# xm, ym = np.unique(data[1], return_counts=True)

# fig, ax = plt.subplots(1, 2, figsize=(12,5), constrained_layout=True)

# ax[0].bar(xf, yf)
# ax[0].set(xlim=(-5,144+5))
# ax[0].set_title("Age distribution of female goats")
# # ax[0].set_yticks([])

# ax[1].bar(xm, ym)
# ax[1].set(xlim=(-5,60+5))
# ax[1].set_title("Age distribution of male goats")
# # ax[1].set_yticks([])

# plt.show()



# ### Timeline output
# s = model.Society(initial_goats, initial_age)

# data = np.zeros((4,simulation_duration+1))
# data[0,0] = s.alive_goats[0]
# data[1,0] = s.alive_goats[1]
# data[2,0] = sum(s.alive_goats)
# data[3,0] = s.active_families
# for m in range(simulation_duration):
#     s.next_month()
#     data[0,m+1] = s.alive_goats[0]
#     data[1,m+1] = s.alive_goats[1]
#     data[2,m+1] = sum(s.alive_goats)
#     data[3,m+1] = s.active_families

# months = np.arange(simulation_duration+1)

# fig, ax = plt.subplots(1, 2, figsize=(9,5), constrained_layout=True)
# ax[0].plot(months, data[0], label="female goats alive")
# ax[0].plot(months, data[1], label="male goats alive")
# ax[0].plot(months, data[2], label="total goats alive")
# ax[0].set(xlim=(0,simulation_duration), ylim=(0,None))
# ax[0].set_xlabel("months")
# ax[0].set_title("Counts")
# ax[0].legend()

# ax[1].plot(months, data[3], label="total families active")
# ax[1].set(xlim=(0,simulation_duration), ylim=(max(0, initial_goats-5),None))
# ax[1].set_xlabel("months")
# ax[1].set_title("Total families active")

# plt.show()

# ### Distribution output
# runs = 500
# data = np.zeros((5,runs))

# for r in range(runs):
#     s = model.Society(initial_goats, initial_age)
#     s.next_month(simulation_duration)

#     data[0,r] = s.alive_goats[0]
#     data[1,r] = s.alive_goats[1]
#     data[2,r] = sum(s.alive_goats)
#     data[3,r] = s.active_families
#     data[4,r] = s.inactive_families

# norm_dist = lambda x, m, s: np.exp(-0.5 * ((x-m)/s)**2) / (s * np.sqrt(2*np.pi))
# x = np.linspace(0, 1.05*max(data[2]), 500)

# mu_0 = np.mean(data[0])
# si_0 = np.std(data[0])

# mu_1 = np.mean(data[1])
# si_1 = np.std(data[1])

# mu_2 = np.mean(data[2])
# si_2 = np.std(data[2])

# mu_3 = np.mean(data[3])
# si_3 = np.std(data[3])

# mu_4 = np.mean(data[4])
# si_4 = np.std(data[4])

# print(f"Initial goats {initial_goats}")
# print(f"Simulating for {simulation_duration} months. (Runs = {runs})")
# print(f"Alive female goats: Mean = {mu_0:.3f}, Std = {si_0:.3f}")
# print(f"Alive male goats: Mean = {mu_1:.3f}, Std = {si_1:.3f}")
# print(f"Alive total goats: Mean = {mu_2:.3f}, Std = {si_2:.3f}")
# print(f"Active families: Mean = {mu_3:.3f}, Std = {si_3:.3f}")
# print(f"Inactive families: Mean = {mu_4:.3f}, Std = {si_4:.3f}, Max = {np.max(data[4])}")

# fig, ax = plt.subplots(2, 2, figsize=(10,8), constrained_layout=True)
# ax[0,0].hist(data[0], density=True)
# ax[0,0].plot(x, norm_dist(x, mu_0, si_0))
# ax[0,0].axvline(mu_0, c="k")
# ax[0,0].set(xlim=( 0.95*min(data[0]), 1.05*max(data[0] )))
# ax[0,0].set_title("Female goats alive")
# ax[0,0].set_yticks([])

# ax[0,1].hist(data[1], density=True)
# ax[0,1].plot(x, norm_dist(x, mu_1, si_1))
# ax[0,1].axvline(mu_1, c="k")
# ax[0,1].set(xlim=( 0.95*min(data[1]), 1.05*max(data[1] )))
# ax[0,1].set_title("Male goats alive")
# ax[0,1].set_yticks([])

# ax[1,0].hist(data[2], density=True)
# ax[1,0].plot(x, norm_dist(x, mu_2, si_2))
# ax[1,0].axvline(mu_2, c="k")
# ax[1,0].set(xlim=( 0.95*min(data[2]), 1.05*max(data[2])))
# ax[1,0].set_title("All goats alive")
# ax[1,0].set_yticks([])

# ax[1,1].hist(data[3], density=True)
# ax[1,1].set_title("Families active")
# ax[1,1].set_yticks([])
# plt.show()