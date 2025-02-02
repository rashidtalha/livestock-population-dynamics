import numpy as np
import matplotlib.pyplot as plt
import model

#####################################

# OVERWRITE THE DEFAULT VALUES:

# model.t_max_male = 144                # Maximum age of a male goat (in months)
# model.t_max_female = 144              # Maximum age of a female goat (in months)
# model.t_prod_start = 7                # Minimum age after which the female goat can become pregnant (in months)
# model.t_prod_end = 120                # Maximum age after which the female goat cannot become pregnant (in months)
# model.t_preg_duration = 6             # Duration of the pregnancy (in months)
# model.t_preg_gap = 2                  # Minimum gap between pregnancies (in months)
# model.t_sell_min_male = 12            # Minimum age after which a male goat can be sold (in months)
# model.t_sell_min_female = 120         # Minimum age after which a female goat can be sold (in months)

# model.p_prod_start = 0.90             # Probability that the female goat survives until t_prod_start
# model.p_prod_end = 0.85               # Probability that the female goat survives until t_prod_end
# model.p_female_kid = 0.50             # Probability that a new born kid is a female
# model.p_get_pregnant = 0.95           # Probability of getting pregnant in a given month (when all conditions are met)
# model.p_kids = [0.35, 0.45, 0.20]     # Probability distribution for giving birth to 1,2,3,... kids (extend by adding/removing values)
# model.p_sell_male = 0.95              # Probability of being sold (in a given month) for all eligible male goats
# model.p_sell_female = 0.95            # Probability of being sold (in a given month) for eligible female goats past the productive age

# model.expland_ownership = True        # Whether the number of owners will grow or not (according to the policy)

#####################################

# RUNTIME PARAMETERS:

f_interventions = 'data.csv'    # Record of manually adding new goats
t_sim = 60                      # Duration of the simulation
iterations = 50                 # Number of iterations (to minimise dispersion due to probablistic effects)
show_graphs = False

#####################################

# SETUP THE SOCIETY, LOAD EXTERNAL INTERVENTIONS & SIMULATE:

dt = np.loadtxt(f_interventions, delimiter=',', skiprows=1, dtype=int, ndmin=2)

res = {k : np.zeros(t_sim+1) for k in model.Society().stats}
for t in range(iterations):
    print(f'Iteration # {t+1:>2} (simulating {t_sim} months)')
    
    s = model.Society()
    for m in range(t_sim):
        for j in dt[dt[:,0] == m]:
            s.add_goats(True,  j[1], j[2])
            s.add_goats(False, j[3], j[4])
        
        for k in res.keys():
            res[k][m] += s.stats[k]

        s.next_month()
        if m == t_sim-1:
            for k in res.keys():
                res[k][m+1] += s.stats[k]

for k in res.keys():
    res[k] = np.ceil(res[k] / iterations).astype(int)

# DISPLAY THE RESULTS:

print(f'\nResults after {t_sim} months (average of {iterations} iterations):')
for k in res.keys():
    print(f'\t{k:<16} = {res[k][-1]}')

plt.rcParams.update({
    "lines.linewidth": 1.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "legend.framealpha": 1,
    "figure.constrained_layout.use": True,
    "savefig.dpi" : 600,
})

t = np.arange(t_sim+1)

fig, ax = plt.subplots()
ax.plot(t, res['num_male'], c='#0047ab', label="Male")
ax.plot(t, res['num_female'], c='#ff2052', label="Female")
ax.plot(t, res['num_male']+res['num_female'], c='#7d7d7d', label="Total")
ax.legend()
ax.set(ylim=(0,None), xlim=(0,t_sim))
ax.set_title('Alive Goats')
ax.set_xlabel('Months')
plt.savefig("goats.png")
if show_graphs: plt.show()

fig, ax = plt.subplots()
ax.plot(t, res['num_families'], c='#0047ab')
ax.set(ylim=(0,None), xlim=(0,t_sim))
ax.set_title('Active Families')
ax.set_xlabel('Months')
plt.savefig("families.png")
if show_graphs: plt.show()