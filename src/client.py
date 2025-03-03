import numpy as np
import pandas as pd

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
# model.p_sell_male = 0.95              # Probability of being sold (in a given month) for male goats over the age of t_sell_min_male
# model.p_sell_female = 0.95            # Probability of being sold (in a given month) for female goats over the age of t_sell_min_female

# model.expand_ownership = True        # Whether the number of owners will grow or not (according to the policy)

#####################################

# RUNTIME PARAMETERS:

iterations = 20                 # Number of iterations (to minimise dispersion due to probablistic effects)
show_graphs = False
df, unique_months, t_sim = model.read_data('data.csv', 'today')

#################################### For aggregated results

res_agg = pd.DataFrame({k : np.zeros(t_sim+1, dtype=int) for k in model.Society().stats.keys()})
for t in range(iterations):
    print(f'Iteration # {t+1:>2} (simulating {t_sim} months)')

    ha, hi, ma, md, fa, fd = model.iterate_history_full(df, t_sim, unique_months)
    res_agg['num_families'] += ha
    res_agg['inactive_familes'] += hi
    res_agg['num_male'] += ma
    res_agg['dead_male'] += md
    res_agg['num_female'] += fa
    res_agg['dead_female'] += fd

res_agg = np.ceil(res_agg / iterations).astype(int)

print(f'\nResults after {t_sim} months (average of {iterations} iterations):')
for k in res_agg:
    print(f'\t{k:<16} = {res_agg[k].iloc[-1]}')

# ##################################### For histogram-type results

# res_hist = pd.DataFrame({k : np.zeros(iterations, dtype=int) for k in model.Society().stats.keys()})
# for t in range(iterations):
#     print(f'Iteration # {t+1:>2} (simulating {t_sim} months)')
#     res_hist.iloc[t] = model.iterate_history_final(df, t_sim, unique_months)

# print(f'\nResults after {t_sim} months (average of {iterations} iterations):')
# for k in res_hist:
#     mu, std = np.mean(res_hist[k]), np.std(res_hist[k])
#     print(f'\t{k:<16} : mean = {mu:.2f} (std = {std:.2f})')

####################################

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
ax.plot(t, res_agg['num_male'], c='#0047ab', label="Male")
ax.plot(t, res_agg['num_female'], c='#ff2052', label="Female")
ax.plot(t, res_agg['num_male']+res_agg['num_female'], c='#7d7d7d', label="Total")
ax.legend()
ax.set(ylim=(0,None), xlim=(0,t_sim))
ax.set_title('Alive Goats')
ax.set_xlabel('Months')
plt.savefig("goats.png")
if show_graphs: plt.show()

fig, ax = plt.subplots()
ax.plot(t, res_agg['num_families'], c='#0047ab')
ax.set(ylim=(0,None), xlim=(0,t_sim))
ax.set_title('Active Families')
ax.set_xlabel('Months')
plt.savefig("families.png")
if show_graphs: plt.show()
